''' Api for communicating with a simulated mega lissajous tracker '''
import collections
import enum
import importlib
import logging
import math
import os
import struct
import subprocess
import sys
import threading
import time

import numpy as np

from adhawktools import datalog, notification, recorder, recordingdata

from . import com, defaults, registers
from .base import FirmwareInfo, MinimumAPIVersion
from .version import SemanticVersion


SIMULATOR_DIR = "tracker-sim"
MAX_DATARATE = 10000
# map from sim geometry name to product name
PERSONALIZATION_SOURCE = {
    'EVK3.4': 'evk3p4',
    'AHSM2': 'ahsm2',
    'AHSM3A1': 'ahsm3a1',
    'AHSM3A2': 'ahsm3a2',
    'GTK': 'gannet'
}


class SimApi:
    ''' Simulated base api '''
    # pylint: disable=too-many-public-methods

    # device configs
    xfreqs = collections.defaultdict(lambda: 3050)
    yfreqs = collections.defaultdict(lambda: 2350)
    xmins = collections.defaultdict(lambda: 0)
    xmaxs = collections.defaultdict(lambda: 1024)
    ymins = collections.defaultdict(lambda: 0)
    ymaxs = collections.defaultdict(lambda: 1024)
    pw_ranges = collections.defaultdict(lambda: [0, 4095])
    pd_sel = collections.defaultdict(lambda: 0xFFFFFFFF)
    axis_conf = {
        'swapxy': [False, False],
        'flipx': [False, False],
        'flipy': [False, False]
    }
    product_defs = None
    spec_blobs = {}
    serial_num = 'EVK3.4'
    error_notifier = notification.StandaloneNotification()

    _endpoints_by_trackerid = {}

    def __init__(self):
        self.trid = 0
        self._dest_id = 0

    @classmethod
    def set_serial_num(cls, serial_num):
        ''' set the sim device type for all SimApis '''
        cls.serial_num = serial_num
        cls._load_personalization()

    @classmethod
    def _load_personalization(cls):
        ''' load personalization constants if they exist '''
        if cls.serial_num in PERSONALIZATION_SOURCE:
            # load the product definition file
            cls.product_defs = importlib.import_module(
                f'adhawkapi.product_defs.{PERSONALIZATION_SOURCE[cls.serial_num]}')
            # convert axis flipping and swapping to local meaning
            for trid, orientation_flags in enumerate(cls.product_defs.SCANNER_ORIENTATION):
                if registers.SpecScannerOrientation.FLIPPEDX not in orientation_flags:
                    cls.axis_conf['flipx'][trid] = True
                if registers.SpecScannerOrientation.FLIPPEDY not in orientation_flags:
                    cls.axis_conf['flipy'][trid] = True
                if registers.SpecScannerOrientation.SWAPPEDXY in orientation_flags:
                    cls.axis_conf['swapxy'][trid] = True
                    cls.axis_conf['flipx'][trid], cls.axis_conf['flipy'][trid] = \
                        cls.axis_conf['flipy'][trid], cls.axis_conf['flipx'][trid]
            # load spec blobs
            cls.spec_blobs = {}
            try:
                cls.spec_blobs['dynamic_fusion'] = cls.product_defs.FUSION_CONSTS
                cls.spec_blobs['model_et'] = cls.product_defs.MODEL_ET
                cls.spec_blobs['model_priors'] = cls.product_defs.MODEL_PRIORS
                cls.spec_blobs['geometry'] = cls.product_defs.GEOMETRY
            except AttributeError as excp:
                logging.warning(f"geometry constants not found: {excp}")
        else:
            logging.warning('SimApi could not find matching product definition')

    @property
    def firmware_info(self):
        '''Returns simulated identification information retrieved from the firmware'''
        return FirmwareInfo(api_version=SemanticVersion(0, 32, 0),
                            product_category=registers.SpecProductCategory.HMD,
                            build_num='',
                            serial_num=f'Sim_{self.serial_num}X',
                            num_devices=defaults.MAX_SCANNERS + 1,
                            dev_id_offset=0,
                            num_trackers=defaults.MAX_SCANNERS,
                            active_trackers=list(range(defaults.MAX_SCANNERS)),
                            active_eyes=list(range(defaults.MAX_EYES)),
                            sim=True)

    def get_register(self, name, *_args, **_kwargs):
        ''' Get the value of a register '''
        if name == registers.ISP_BOARD_TYPE:
            return [self.product_defs.BOARD_TYPE]
        if name == registers.SPEC_PRODUCT_ID:
            return [self.product_defs.PRODUCT_ID]
        raise MinimumAPIVersion(f'{name} is not supported in SimApi')

    @property
    def portname(self):
        '''Returns portname of simulated API'''
        return 'virtualport'

    def get_capability(self, control=False):
        '''Retrieves the capabilities of the specified endpoint'''
        del control
        capbits = [1027, 1029, 13312, 21504, 1024][self._dest_id]
        return [cap for cap in registers.SpecCapability
                if capbits & (1 << cap.value)]

    @classmethod
    def sync_configs(cls, configs):
        ''' load the configs from a SystemConfigs object and load personalization into the configs '''
        try:
            for trackerid in range(defaults.MAX_SCANNERS):
                tracker = configs[f'tracker{trackerid}']
                # scan
                cls.xfreqs[trackerid] = tracker.frequency
                cls.yfreqs[trackerid] = tracker.yfrequency
                cls.xmins[trackerid] = tracker.xmean - tracker.width / 2
                cls.xmaxs[trackerid] = tracker.xmean + tracker.width / 2
                cls.ymins[trackerid] = tracker.ymean - tracker.height / 2
                cls.ymaxs[trackerid] = tracker.ymean + tracker.height / 2
                # glint
                cls.pw_ranges[trackerid] = [tracker.glintpwfilterthreshold.min, tracker.glintpwfilterthreshold.max]
                cls.pd_sel[trackerid] = 0
                for i in range(defaults.N_PHOTODIODES):
                    cls.pd_sel[trackerid] |= (tracker[f'pd{i}'].enable) << i
                # pupil
                ppid = trackerid + defaults.MAX_SCANNERS
                cls.pw_ranges[ppid] = [tracker.pupilpwfilterthreshold.min, tracker.pupilpwfilterthreshold.max]
                cls.pd_sel[ppid] = 0
                for i in range(defaults.MAX_PUPIL_DETECTORS):
                    cls.pd_sel[ppid] |= (tracker[f'pupilpd{i}'].enable) << i
            if cls.product_defs is not None:
                # populate static modulecal
                configs.update_recursive({
                    'blob': {
                        'tuning': {
                            'module_cal': {
                                'scan_to_angles': [cls._generate_module_cal(trid)
                                                   for trid in range(defaults.MAX_SCANNERS)]
                            }
                        }
                    }
                })
            if 'multiglintcal' in configs.tracker0:
                # migrate multiglint to new location
                configs.update_recursive({
                    'blob': {
                        'tuning': {
                            'multiglint': [configs[f'tracker{trid}'].multiglintcal
                                           for trid in range(defaults.MAX_SCANNERS)]
                        }
                    }
                })
        except KeyError as excp:
            logging.warning(f"SimApi could not find config key: {excp}")

    @classmethod
    def _generate_module_cal(cls, trid):
        '''Get the module cal transform for the sim for the selected geometry and trackerid'''
        xmin = cls.xmins[trid]
        xmax = cls.xmaxs[trid]
        ymin = cls.ymins[trid]
        ymax = cls.ymaxs[trid]
        xmean = (xmax + xmin) / 2
        ymean = (ymax + ymin) / 2
        width = xmax - xmin
        height = ymax - ymin
        # The sim maps the scan space from [0, 4095] to [-22.5, 22.5] degrees linearly
        # s contains the ratio required to transform scan space coordinates to angular coordinates
        scan_2_angle = np.deg2rad(45) / 4095
        feature_vector = np.array([xmean,
                                   ymean,
                                   width,
                                   height,
                                   xmean * width,
                                   ymean * height,
                                   xmean * height,
                                   ymean * width,
                                   1])
        base_transform = np.array([
            [0, 0, scan_2_angle * 0.5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [scan_2_angle, 0, 0, 0, 0, 0, 0, 0, scan_2_angle * -2048],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, scan_2_angle * 0.5, 0, 0, 0, 0, 0],
            [0, scan_2_angle, 0, 0, 0, 0, 0, 0, scan_2_angle * -2048]
        ])
        # Check if geometry swaps x/y axis, as this needs to be accounted for in module cal
        # by swapping the rows in our final transform, so the base_transform needs to be adjusted
        # accordingly
        if cls.axis_conf['swapxy'][trid]:
            base_transform = np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, scan_2_angle * 0.5, 0, 0, 0, 0, 0],
                [0, scan_2_angle, 0, 0, 0, 0, 0, 0, scan_2_angle * -2048],
                [0, 0, scan_2_angle * 0.5, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [scan_2_angle, 0, 0, 0, 0, 0, 0, 0, scan_2_angle * -2048]])
        # Check if geometry requires a flip in the x-axis
        if cls.axis_conf['flipx'][trid]:
            if cls.axis_conf['swapxy'][trid]:
                base_transform[5, :] = -1 * base_transform[5, :]
                base_transform[2, :] = -1 * base_transform[2, :]
            else:
                base_transform[2, :] = -1 * base_transform[2, :]
                base_transform[0, :] = -1 * base_transform[0, :]
        if cls.axis_conf['flipy'][trid]:
            if cls.axis_conf['swapxy'][trid]:
                base_transform[2, :] = -1 * base_transform[2, :]
                base_transform[1, :] = -1 * base_transform[1, :]
            else:
                base_transform[5, :] = -1 * base_transform[5, :]
                base_transform[4, :] = -1 * base_transform[4, :]
        return (base_transform @ feature_vector).reshape((2, 3))

    @classmethod
    def add_fault_callback(cls, func):
        '''Add callback for critical communication related failures'''
        cls.error_notifier.add_callback(func)

    @classmethod
    def from_tracker_id(cls, tracker_id, **kwargs):
        '''Construct a new API given a pre-existing global tracker id'''
        dest_id = cls._endpoints_by_trackerid[tracker_id]
        api = cls(**kwargs)
        api.set_tracker_id(tracker_id, dest_id)
        return api

    def set_tracker_id(self, tracker_id, dest_id=None):
        '''Adjust the device id to communicate for subsequent commands'''
        self.trid = tracker_id
        self._endpoints_by_trackerid[tracker_id] = dest_id

    @property
    def dest_id(self):
        '''Returns the currently selected device id for communication'''
        return self._dest_id

    @dest_id.setter
    def dest_id(self, dest_id):
        '''Returns the current selected tracker id for the currently selected device id'''
        self._dest_id = dest_id

    def set_threshold(self, val):
        '''Adjust the trigger threshold to the specified value (range: [0.0, 3.3])'''
        pass

    def set_threshold2(self, val):
        '''Adjust the trigger threshold 2 to the specified value (range: [0.0, 3.3])'''
        pass

    def set_vcsel_current(self, val):
        '''Adjust the laser current (range: [0.0, 7.5])'''
        pass

    def set_resonance_frequency(self, val):
        '''Adjust the resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        self.xfreqs[self.trid] = val

    def get_resonance_frequency(self):
        '''Get the resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        return self.xfreqs[self.trid]

    def set_y_resonance_frequency(self, val):
        '''Adjust the y resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        self.yfreqs[self.trid] = val

    def get_y_resonance_frequency(self):
        '''Get the y resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        return self.yfreqs[self.trid]

    def set_comparator_threshold(self, val):
        '''Sets the the comparator threshold for peak detect'''
        pass

    def set_glint_pw_max_threshold(self, val):
        '''Sets the tros tracking pulse width filter max threshold'''
        self.pw_ranges[self.trid % defaults.MAX_SCANNERS][1] = val

    def set_glint_pw_min_threshold(self, val):
        '''Sets the tros tracking pulse width filter min threshold'''
        self.pw_ranges[self.trid % defaults.MAX_SCANNERS][0] = val

    def set_photodiode_gain(self, pdindex, val):
        '''Sets the gain for the specified photodiode (digital)'''
        pass

    def set_photodiode_selection(self, val):
        '''Sets the photodiodes to be used when detecting glint pulses'''
        self.pd_sel[self.trid % defaults.MAX_SCANNERS] = val

    def set_photodiode_gain_boost(self, val):
        '''Sets the gain boost option for the photodiodes'''
        pass

    def set_pupil_detector_selection(self, val):
        '''Sets the photodiodes to be used when detecting pupil pulses'''
        self.pd_sel[self.trid % defaults.MAX_SCANNERS + defaults.MAX_SCANNERS] = val

    def set_pupil_detector_gain(self, pdindex, val, boost):
        '''Sets the gain for the specified pupil photodiode'''
        pass

    def set_pupil_pw_max_threshold(self, val):
        '''Sets the tros tracking pupil pulse width filter max threshold'''
        self.pw_ranges[self.trid % defaults.MAX_SCANNERS + defaults.MAX_SCANNERS][1] = val

    def set_pupil_pw_min_threshold(self, val):
        '''Sets the tros tracking pupil pulse width filter min threshold'''
        self.pw_ranges[self.trid % defaults.MAX_SCANNERS + defaults.MAX_SCANNERS][0] = val

    def set_x_range(self, xmin, xmax):
        '''Adjust the maximum / minimum x position of the scanner in resonant mode (range: [0, 1023])'''
        self.xmins[self.trid] = xmin
        self.xmaxs[self.trid] = xmax

    def set_y_range(self, ymin, ymax):
        '''Adjust the maximum / minimum y position of the scanner in resonant mode (range: [0, 1023])'''
        self.ymins[self.trid] = ymin
        self.ymaxs[self.trid] = ymax

    def set_y_max(self, val):
        '''Sets the maximum y position to track'''
        self.ymaxs[self.trid] = val

    def set_y_min(self, val):
        '''Sets the minimum y position to track'''
        self.ymins[self.trid] = val

    def __getattr__(self, attribute):
        ''' provide dummy handlers for everything that's not accounted for '''
        def do_nothing(*args, **kwargs):
            argstr = str(list(args))[1:-1] if args else ''
            kwargstr = ', '.join((f'{key}={value}' for key, value in kwargs.items()))
            sep = ', ' if argstr and kwargstr else ''
            logging.debug(f'Simapi ignored {self.__class__.__name__}.{attribute}({argstr}{sep}{kwargstr})')
        return do_nothing


class DummySimAutotune(SimApi):
    ''' Dummy autotune API '''

    def __init__(self, *args, **kwargs):
        super().__init__()
        argstr = str(list(args))[1:-1] if args else ''
        kwargstr = ', '.join((f'{key}={value}' for key, value in kwargs.items()))
        sep = ', ' if argstr and kwargstr else ''
        logging.debug(f'ignored SimAutotune({argstr}{sep}{kwargstr})')


class SimAutotune(SimApi):
    '''Class wrapping SimApi used to execute autotune line sweep'''
    _readthread = None
    _proc = None
    _handler = None

    PROCESS_STARTED_ECHO = 'process_started'
    SCAN_STARTED_ECHO = 'scan_started'
    SCAN_STOPPED_ECHO = 'scan_stopped'

    PROCESS_STARTED_RESPONSE = '- comment process_started'
    SCAN_STARTED_RESPONSE = '- comment scan_started'
    SCAN_STOPPED_RESPONSE = '- comment scan_stopped'

    dwell = collections.defaultdict(lambda: 3200)
    line_thickness = collections.defaultdict(lambda: 5)
    line_width = collections.defaultdict(lambda: 400)
    line_height = collections.defaultdict(lambda: 400)
    autotune_xmaxs = collections.defaultdict(lambda: 1024)
    autotune_xmins = collections.defaultdict(lambda: 0)
    autotune_xsteps = collections.defaultdict(lambda: 20)
    autotune_ymaxs = collections.defaultdict(lambda: 1024)
    autotune_ymins = collections.defaultdict(lambda: 0)
    autotune_ysteps = collections.defaultdict(lambda: 20)
    x_eye_offsets = collections.defaultdict(lambda: 0)
    y_eye_offsets = collections.defaultdict(lambda: 0)
    z_eye_offsets = collections.defaultdict(lambda: 0)

    class DataType(enum.IntEnum):
        '''Various data types streamed by the autotune application'''
        RANGE_RESULT = 0
        JITTER_DATA = 1
        TUNING_RESULT = 3
        PULSE_DATA = 10
        ERROR_DATA = 14

    def __init__(self):
        self._diag_data = None
        self._session = None
        self._xindex = {}
        self._yindex = {}
        self._num_steps = [{'x': 0, 'y': 0}, {'x': 0, 'y': 0}]
        self._scan_finished_signal = threading.Event()
        super().__init__()

    def _create_proc(self):
        my_env = os.environ.copy()
        cwd = os.path.abspath(SIMULATOR_DIR)
        if self.serial_num not in PERSONALIZATION_SOURCE:
            logging.warning("Chosen serial number is not supported for sim autotune")
        SimAutotune._proc = subprocess.Popen([sys.executable, 'adhawksim.py', self.serial_num],
                                             stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                             stderr=subprocess.PIPE, env=my_env, cwd=cwd, encoding='utf8')
        SimAutotune._proc.stdin.write(f"- sim echo {SimAutotune.PROCESS_STARTED_ECHO}\n")
        SimAutotune._proc.stdin.flush()
        started = False
        while not started:
            for line in SimAutotune._proc.stdout:
                if line.strip() == SimAutotune.PROCESS_STARTED_RESPONSE:
                    started = True
                    break

    def _generate_configs(self, simultaneous):
        configs = {}
        configs['general'] = {'serialnum': f'Sim_{self.serial_num}X',
                              'firmwareversion': "Sim",
                              'clientnum': f"SIM_{self.serial_num}",
                              'apiversion': '0.15.0',
                              'numtrackers': defaults.MAX_SCANNERS}
        if simultaneous:
            start_trid = 0
            end_trid = defaults.MAX_SCANNERS
        else:
            start_trid = self.trid
            end_trid = self.trid + 1

        for trid in range(start_trid, end_trid):
            configs[f'tracker{trid}'] = {}
            configs[f'tracker{trid}']['frequency'] = self.xfreqs[trid]
            configs[f'tracker{trid}']['yfrequency'] = self.yfreqs[trid]
            configs[f'tracker{trid}']['autotune'] = {'xrange': {'min': self.autotune_xmins[trid],
                                                                'max': self.autotune_xmaxs[trid],
                                                                'step': self.autotune_xsteps[trid]},
                                                     'yrange': {'min': self.autotune_ymins[trid],
                                                                'max': self.autotune_ymaxs[trid],
                                                                'step': self.autotune_ysteps[trid]},
                                                     'width': self.xmaxs[trid] - self.xmins[trid],
                                                     'height': self.ymaxs[trid] - self.ymins[trid],
                                                     'algorithm': 3}
        return configs

    def record_pulse(self, tstamp, trid, pd_id, xpos, ypos, pulsewidth):
        '''Record autotune pulse for db recorder'''
        pd_id = int(pd_id << 12)
        xindex = self._yindex[trid] if self.axis_conf['swapxy'][trid] else self._xindex[trid]
        yindex = self._xindex[trid] if self.axis_conf['swapxy'][trid] else self._yindex[trid]
        xindex = self._num_steps[trid]['x'] - xindex if self.axis_conf['flipx'][trid] and xindex > 0 else xindex
        yindex = self._num_steps[trid]['y'] - yindex if self.axis_conf['flipy'][trid] and yindex > 0 else yindex
        if self._diag_data is not None:
            data = struct.pack('<BBBBHHHHH',
                               xindex,
                               yindex,
                               0,
                               0,
                               tstamp,
                               xpos,
                               ypos,
                               pulsewidth,
                               pd_id)
            self._diag_data['data'][str(trid)].append(
                info_type=SimAutotune.DataType.PULSE_DATA.value, info=list(data))
        else:
            print(f"{tstamp} {trid} {pd_id} {xpos} {ypos} {pulsewidth}")

    def _update_sweep_index(self, index, scan_axis, trid):
        if scan_axis:
            self._xindex[trid] = index
            self._yindex[trid] = 0
        else:
            self._xindex[trid] = 0
            self._yindex[trid] = index
        print(f"Currently processing XIndex: {self._xindex[trid]} YIndex: {self._yindex[trid]}")

    def _log_stderr(self):
        for line in self._proc.stderr:
            sys.stderr.write(line)

    def autotune(self, simultaneous=False):  # pylint: disable=too-many-statements,too-many-branches
        '''Execute simulated autotune line sweep'''
        configs = self._generate_configs(simultaneous)
        if self._session is None:
            self._session = datalog.create_session(configs, user_defined_tags=["Simulated_Autotune"])

        self._diag_data = recordingdata.RecordingData(configs=configs)
        self._diag_data['session'] = self._session

        if self._proc is None:
            self._create_proc()

        if simultaneous:
            start_trid = 0
            end_trid = defaults.MAX_SCANNERS
            for trid in range(defaults.MAX_SCANNERS):
                self._update_configs(trid)
        else:
            if self.trid < defaults.MAX_SCANNERS:
                self._update_configs(self.trid)
                start_trid = self.trid
                end_trid = self.trid + 1
            else:
                return
        self._proc.stdin.flush()

        line_sweep_configs = {}
        for trid in range(defaults.MAX_SCANNERS):
            self._xindex[trid] = 0
            self._yindex[trid] = 0
            x_sweep_pos = np.array(list(range(int(self.autotune_xmins[trid] + (self.autotune_xsteps[trid] / 2)),
                                              self.autotune_xmaxs[trid] + self.autotune_xsteps[trid],
                                              self.autotune_xsteps[trid])))
            x_sweep_megalisa = [(pos - self.line_thickness[trid],
                                 pos + self.line_thickness[trid]) for pos in x_sweep_pos]
            self._num_steps[trid]['x'] = len(x_sweep_pos)
            y_sweep_pos = np.array(list(range(int(self.autotune_ymins[trid] + (self.autotune_ysteps[trid] / 2)),
                                              self.autotune_ymaxs[trid] + self.autotune_ysteps[trid],
                                              self.autotune_ysteps[trid])))
            y_sweep_megalisa = [(pos - self.line_thickness[trid],
                                 pos + self.line_thickness[trid]) for pos in y_sweep_pos]
            self._num_steps[trid]['y'] = len(y_sweep_pos)
            line_sweep_configs[trid] = [{'sweep_configs': y_sweep_megalisa,
                                         'scan_configs': self.line_width[trid]},
                                        {'sweep_configs': x_sweep_megalisa,
                                         'scan_configs': self.line_height[trid]}]
        read_thread = threading.Thread(target=self._run, daemon=True, name='SimApiRead')
        read_thread.start()
        threading.Thread(target=self._log_stderr, daemon=True, name='SimApiLog').start()
        for scan_axis in range(2):
            sweep_index = [0 for trid in range(defaults.MAX_SCANNERS)]
            trackers_done = set()
            while len(trackers_done) < (end_trid - start_trid):
                for trid in range(start_trid, end_trid):
                    self._proc.stdin.write(f'- sim stop {trid}\n')
                    if trid in trackers_done:
                        continue
                    box = line_sweep_configs[trid][scan_axis]['sweep_configs'][sweep_index[trid]]
                    sweep_config, scan_config = self._generate_line_configs(scan_axis, box, trid)
                    self._proc.stdin.write(sweep_config)
                    self._proc.stdin.write(scan_config)
                    self._proc.stdin.write(f'- sim start {trid}\n')
                    self._proc.stdin.flush()
                    self._update_sweep_index(sweep_index[trid], scan_axis, trid)
                    sweep_index[trid] += 1
                    if sweep_index[trid] >= len(line_sweep_configs[trid][scan_axis]['sweep_configs']):
                        trackers_done.add(trid)
                self._proc.stdin.write(f'- sim echo {self.SCAN_STARTED_ECHO}\n')
                self._proc.stdin.flush()
                self._scan_finished_signal.wait()
                time.sleep(self.dwell[self.trid] * (1 / self.xfreqs[self.trid]))
                self._proc.stdin.write(f'- sim echo {self.SCAN_STOPPED_ECHO}\n')
                self._proc.stdin.flush()
        self._proc.stdin.write('- sim shutdown\n')
        self._proc.stdin.flush()
        read_thread.join()
        self._proc.wait()
        SimAutotune._proc = None
        recorder.dump(self._diag_data, 'autotune')

    def _run(self):
        graceful_exit = False
        scanning = False
        while not graceful_exit:
            # graceful_termination = False
            for line in SimAutotune._proc.stdout:
                if line.strip() == 'closing':
                    graceful_exit = True
                    break
                if line.strip() == self.SCAN_STARTED_RESPONSE:
                    self._scan_finished_signal.set()
                    scanning = True
                elif line.strip() == self.SCAN_STOPPED_RESPONSE:
                    self._scan_finished_signal.clear()
                    scanning = False
                if scanning:
                    parts = line.strip().split(' ')
                    if len(parts) != 8 or parts[1] != 'pulse':
                        print(line)
                        graceful_exit = True
                        continue
                    tstamp = float(parts[0])
                    trid = int(parts[2])
                    pd_id = int(parts[3])
                    xpos = int(float(parts[4]) * 4095 / math.pi)
                    ypos = int(float(parts[5]) * 4095 / math.pi)
                    if self.axis_conf['swapxy'][trid]:
                        xpos, ypos = ypos, xpos
                    pulsewidth = int(float(parts[6]) * self.xfreqs[trid] * 2e-6 * 4095)
                    self.record_pulse(int(tstamp), trid, pd_id, xpos, ypos, pulsewidth)

    def _generate_line_configs(self, scan_axis, box, trid):  # pylint: disable=no-self-use
        sweep_range_config = 'scan_xrange' if scan_axis == 1 else 'scan_yrange'
        scan_range_config = 'scan_yrange' if scan_axis == 1 else 'scan_xrange'
        sweep_config = f'- config {sweep_range_config} {trid} {box[0]} {box[1]}\n'
        scan_config = f'- config {scan_range_config} {trid} {0} {1023}\n'
        return sweep_config, scan_config

    def _update_configs(self, trid):
        if self._proc is not None:
            stdin = self._proc.stdin
            if self.axis_conf['swapxy'][trid]:
                stdin.write(f'- config scan_freq {trid} {self.yfreqs[trid]} {self.xfreqs[trid]}\n')
                stdin.write(f'- config scan_xrange {trid} {self.ymins[trid]} {self.ymaxs[trid]}\n')
                stdin.write(f'- config scan_yrange {trid} {self.xmins[trid]} {self.xmaxs[trid]}\n')
            else:
                stdin.write(f'- config scan_freq {trid} {self.xfreqs[trid]} {self.yfreqs[trid]}\n')
                stdin.write(f'- config scan_xrange {trid} {self.xmins[trid]} {self.xmaxs[trid]}\n')
                stdin.write(f'- config scan_yrange {trid} {self.ymins[trid]} {self.ymaxs[trid]}\n')
            stdin.write(f'- config scan_freq {trid} {self.xfreqs[trid]} {self.yfreqs[trid]}\n')
            stdin.write(f'- config scan_xrange {trid} {self.xmins[trid]} {self.xmaxs[trid]}\n')
            stdin.write(f'- config scan_yrange {trid} {self.ymins[trid]} {self.ymaxs[trid]}\n')
            stdin.write(f'- config pd_sel {trid} {self.pd_sel[trid]}\n')
            stdin.write(f'- config pw_min {trid} {self.pw_ranges[trid][0] * math.pi / 4095}\n')
            stdin.write(f'- config pw_max {trid} {self.pw_ranges[trid][1] * math.pi / 4095}\n')
            ppid = trid + defaults.MAX_SCANNERS
            stdin.write(f'- config pd_sel {trid} {self.pd_sel[ppid]} True\n')
            stdin.write(f'- config pw_min {trid} {self.pw_ranges[ppid][0] * math.pi / 4095} True\n')
            stdin.write(f'- config pw_max {trid} {self.pw_ranges[ppid][1] * math.pi / 4095} True\n')
            stdin.write(f'- config pw_max {trid} {self.pw_ranges[ppid][1] * math.pi / 4095} True\n')
            stdin.write((f'- config eye_offset '
                         f'{trid} '
                         f'{self.x_eye_offsets[trid]} '
                         f'{self.y_eye_offsets[trid]} '
                         f'{self.z_eye_offsets[trid]}\n'))
            stdin.flush()

    def set_dwell_config(self, dwell):
        '''Set amount of time line should dwell for during line sweep'''
        self.dwell[self.trid] = dwell

    def set_line_thickness(self, thickness):
        '''Set line thickness in sweep axis during line sweep'''
        self.line_thickness[self.trid] = thickness

    def set_line_width(self, width):
        '''Set line width in scan axis during line sweep'''
        self.line_width[self.trid] = width

    def set_line_height(self, height):
        '''Set line height in scan axis during line sweep'''
        self.line_height[self.trid] = height

    def set_autotune_x_range(self, xmin, xmax, step):
        '''Set autotune x line sweep range and step size'''
        self.autotune_xmaxs[self.trid] = xmax
        self.autotune_xmins[self.trid] = xmin
        self.autotune_xsteps[self.trid] = step

    def set_autotune_y_range(self, ymin, ymax, step):
        '''Set autotune y line sweep range and step size'''
        self.autotune_ymaxs[self.trid] = ymax
        self.autotune_ymins[self.trid] = ymin
        self.autotune_ysteps[self.trid] = step

    def set_eye_offset(self, x_offset, y_offset, z_offset):
        '''Set an offset in mm from the nominal eye-position'''
        self.x_eye_offsets[self.trid] = x_offset
        self.y_eye_offsets[self.trid] = y_offset
        self.z_eye_offsets[self.trid] = z_offset


class SimCustomerStream(SimApi):
    ''' Dummy customer stream API '''

    def __init__(self, *args, **kwargs):
        super().__init__()
        argstr = str(list(args))[1:-1] if args else ''
        kwargstr = ', '.join((f'{key}={value}' for key, value in kwargs.items()))
        sep = ', ' if argstr and kwargstr else ''
        print(f'ignored SimCustomerStream({argstr}{sep}{kwargstr})')


class SimMegaLissajous(SimApi):
    '''Python frontend for simulated lissajous-based tracking API'''
    _readthread = None
    _proc = None
    _handler = None
    COMMAND_EXEC_SENT = "command_executed"
    COMMAND_EXEC_RECV = '- comment command_executed'
    _command_sync = threading.Event()

    @classmethod
    def add_callback_lissajous_data(cls, func):
        '''Add callback to retrieve time_ref, x, y, amplitude, and pulse width'''
        cls._handler = func

    def start(self):
        '''Start an application'''
        if self._proc is None:
            self._create_proc()
        if self.trid < defaults.MAX_SCANNERS:
            self._update_configs(self.trid)
            self._proc.stdin.write(f'- sim start {self.trid}\n')
        else:
            self._proc.stdin.write(f'- config enable_pupil {self.trid % defaults.MAX_SCANNERS} True\n')
        self._proc.stdin.flush()
        if self._readthread is None:
            SimMegaLissajous._readthread = threading.Thread(target=self._run, daemon=True, name='SimApiRead')
            SimMegaLissajous._readthread.start()
            threading.Thread(target=self._log_stderr, daemon=True, name='SimApiLog').start()

    def stop(self):
        '''Stop the currently running application, if applicable'''
        if self._proc is not None:
            if self.trid < defaults.MAX_SCANNERS:
                self._proc.stdin.write(f'- sim stop {self.trid}\n')
            else:
                self._proc.stdin.write(f'- config enable_pupil {self.trid % defaults.MAX_SCANNERS} False\n')
            self._proc.stdin.flush()

    def sim_send_command(self, *args):
        '''
        Send a message to the simulator

        Usage:
            sim COMMAND [...]

        Examples:
            sim help
            sim help config eye_offset
            sim config eye_offset 0 0 0 -10
        '''
        if self._proc is not None:
            stdin = self._proc.stdin
            stdin.write(f"- {' '.join(args)}\n")
            stdin.flush()
            # Synchronize simulator process with main process after command execution
            self.sync()
        else:
            logging.error('Simulator is not ready')

    def sync(self):
        '''Synchronize with the simulator process'''
        stdin = self._proc.stdin
        stdin.write(f'- sim start {self.trid}\n')
        self._command_sync.clear()
        stdin.write(f'- sim echo {self.COMMAND_EXEC_SENT}\n')
        stdin.flush()
        self._command_sync.wait()

    def _update_configs(self, trid):
        if self._proc is not None:
            stdin = self._proc.stdin
            if self.axis_conf['swapxy'][trid]:
                stdin.write(f'- config scan_freq {self.trid} {self.yfreqs[trid]} {self.xfreqs[trid]}\n')
                stdin.write(f'- config scan_xrange {self.trid} {self.ymins[trid]} {self.ymaxs[trid]}\n')
                stdin.write(f'- config scan_yrange {self.trid} {self.xmins[trid]} {self.xmaxs[trid]}\n')
            else:
                stdin.write(f'- config scan_freq {self.trid} {self.xfreqs[trid]} {self.yfreqs[trid]}\n')
                stdin.write(f'- config scan_xrange {self.trid} {self.xmins[trid]} {self.xmaxs[trid]}\n')
                stdin.write(f'- config scan_yrange {self.trid} {self.ymins[trid]} {self.ymaxs[trid]}\n')
            stdin.write(f'- config pd_sel {self.trid} {self.pd_sel[trid]}\n')
            stdin.write(f'- config pw_min {self.trid} {self.pw_ranges[trid][0] * math.pi / 4095}\n')
            stdin.write(f'- config pw_max {self.trid} {self.pw_ranges[trid][1] * math.pi / 4095}\n')
            ppid = trid + defaults.MAX_SCANNERS
            stdin.write(f'- config pd_sel {self.trid} {self.pd_sel[ppid]} True\n')
            stdin.write(f'- config pw_min {self.trid} {self.pw_ranges[ppid][0] * math.pi / 4095} True\n')
            stdin.write(f'- config pw_max {self.trid} {self.pw_ranges[ppid][1] * math.pi / 4095} True\n')
            stdin.write(f'- config enable_pupil {self.trid}\n')
            stdin.flush()

    @staticmethod
    def _ratelimit(iterator, max_rate, sleeptime=0.002):
        # limit the rate of an iterator by sleeping on an interval to schedule other tasks
        datacount = 0
        sleeprate = int(max_rate / (1 / sleeptime))
        for item in iterator:
            yield item
            datacount += 1
            if datacount >= sleeprate:
                time.sleep(sleeptime)
                datacount = 0

    def _create_proc(self):
        my_env = os.environ.copy()
        cwd = os.path.abspath(SIMULATOR_DIR)
        SimMegaLissajous._proc = subprocess.Popen([sys.executable, 'adhawksim.py', self.serial_num],
                                                  stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                                  stderr=subprocess.PIPE, env=my_env, cwd=cwd, encoding='utf8')

    def _run(self):
        graceful_termination = False
        for line in self._ratelimit(SimMegaLissajous._proc.stdout, MAX_DATARATE):
            if line.strip() == 'closing':
                graceful_termination = True
                break
            parts = line.strip().split(' ')
            if len(parts) != 8 or parts[1] != 'pulse':
                if line.strip() == self.COMMAND_EXEC_RECV:
                    self._command_sync.set()
                continue
            tstamp = float(parts[0])
            trid = int(parts[2])
            pd_id = int(parts[3])
            xpos = int(float(parts[4]) * 4095 / math.pi)
            ypos = int(float(parts[5]) * 4095 / math.pi)
            if self.axis_conf['swapxy'][trid]:
                xpos, ypos = ypos, xpos
            pulsewidth = int(float(parts[6]) * self.xfreqs[trid] * 2e-6 * 4095)
            if self._handler is not None:
                # pylint is drunk
                # pylint: disable=not-callable
                self._handler(trid, tstamp, xpos, ypos, 1.0, pulsewidth, pd_id)
        SimMegaLissajous._readthread = None
        SimMegaLissajous._proc = None
        logging.info("sim closed")
        if not graceful_termination:
            # subprocess terminated on its own
            try:
                raise com.PortClosedError()
            except com.PortClosedError as excp:
                self.error_notifier.notify_callbacks(excp)

    def _log_stderr(self):
        for line in self._proc.stderr:
            sys.stderr.write(line)

    def shutdown(self):
        ''' Close all open subprocesses '''
        if self._proc is not None:
            proc = self._proc
            proc.stdin.write('- sim shutdown\n')
            proc.stdin.flush()
            try:
                proc.wait(0.5)
            except subprocess.TimeoutExpired:
                logging.warning('Killing simulation subprocess')
                proc.kill()
