'''General API and Base application api'''

import ctypes
import logging

from . import base
from . import defaults
from . import register_api
from . import registers

from .utils import unpack_response, unpack_stream
from .version import SemanticVersion


class GeneralApi(register_api.RegisterApi):
    '''Provides the API to configure general attributes for all applications'''
    # This API will be deprecated in favor of the RegisterApi() which provides:
    # 1. getters and setters for each register
    # 2. easier integration with UI applications
    # 3. the ability to dump the full register set

    # This API now inherits from RegisterApi and has access to the get_register() and set_register() functions
    # Any new registers just need to be added to the yaml definitions. See adhawkapi/register_api.md

    # pylint: disable=too-many-public-methods

    def get_capability(self, control=False):
        '''Retrieves the capabilities of the specified endpoint'''
        logging.debug('get_capability()')
        response = self._request(base.SPEC_BANK, 1, control=control)
        capbits = unpack_response('<I', response)[0]
        return [cap for cap in registers.SpecCapability
                if capbits & (1 << cap.value)]

    def get_camera_type(self, control=False):
        '''Retrieves the ID of the camera mounted on the device'''
        logging.debug('get_camera_type()')
        response = self._request(base.SPEC_BANK, 2, control=control)
        try:
            return registers.SpecCamera(unpack_response('<I', response)[0])
        except ValueError:
            return registers.SpecCamera.NOT_AVAILABLE

    def get_max_vcsel_current(self):
        '''Get the max vcsel current'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 17, 0)) < 0:
            return defaults.LIMIT_MAX_LASER_CURRENT / defaults.LIMIT_MAX_LASER_CURRENT_SCALE * 4095
        logging.debug('get_max_vcsel_current()')
        response = self._request(base.SPEC_BANK, 35)
        max_vcsel_current = unpack_response('<I', response)[0]
        logging.debug(f'max_vcsel_current: {max_vcsel_current}')
        return max_vcsel_current

    def set_vcsel_current(self, val):
        '''Adjust the laser current'''
        logging.debug(f'set_vcsel_current({val})')
        max_vcsel_current = self.get_max_vcsel_current()
        intval = int(float(val) / defaults.LIMIT_MAX_LASER_CURRENT_SCALE * 4095)
        if intval < 0 or intval > max_vcsel_current:
            raise base.OutofRangeError(f'Laser current: Range[0.0, {max_vcsel_current}]')
        self._request(base.GENERAL_BANK, 10, intval)

    def set_vcsel_frequency(self, val):
        '''Adjust the modulation frequency (range: [1.0 to 10.0], units:[MHz])'''
        logging.debug(f'set_vcsel_frequency({val})')
        if float(val) < defaults.LIMIT_MIN_MODULATION_FREQ or float(val) > defaults.LIMIT_MAX_MODULATION_FREQ:
            raise base.OutofRangeError('Vcsel Modulation Frequency')
        intval = int(float(val) * 1000000)
        self._request(base.GENERAL_BANK, 24, intval)

    def get_max_duty_cycle(self):
        '''Get the max duty cycle'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 17, 0)) < 0:
            return defaults.LIMIT_MAX_DUTYCYCLE
        logging.debug('get_max_duty_cycle()')
        response = self._request(base.SPEC_BANK, 36)
        max_duty_cycle = unpack_response('<I', response)[0]
        logging.debug(f'max_duty_cycle: {max_duty_cycle}')
        return max_duty_cycle

    def set_vcsel_dutycycle(self, val):
        '''Adjust the modulation duty cycle (units:[%])'''
        logging.debug(f'set_vcsel_dutycycle({val})')
        max_duty_cycle = self.get_max_duty_cycle()
        if int(val) < 0 or int(val) > max_duty_cycle:
            raise base.OutofRangeError(f'Vcsel Modulation Duty Cycle: Range[0, {max_duty_cycle}]')
        self._request(base.GENERAL_BANK, 25, val)

    def set_resonance_frequency(self, val):
        '''Adjust the resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        logging.debug(f'set_resonance_frequency({val})')
        if int(val) < defaults.LIMIT_MIN_FREQ or int(val) > defaults.LIMIT_MAX_FREQ:
            raise base.OutofRangeError('Resonant frequency')
        self._request(base.GENERAL_BANK, 12, int(val))

    def get_configured_x_frequency(self):
        '''Get the configured resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        logging.debug('get_conf_resonance_frequency()')
        response = self._request(base.GENERAL_BANK, 12)
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 19, 0)) < 0:
            val = unpack_response('f', response)[0]
        else:
            val = unpack_response('I', response)[0]
        return val

    def get_operational_x_frequency(self):
        '''Get the operational resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 19, 0)) < 0:
            raise base.IncompatibleAPIVersion(pyver=SemanticVersion(0, 19, 0), ucver=self.firmware_info.api_version)
        response = self._request(base.GENERAL_BANK, 48)
        val = unpack_response('f', response)[0]
        return val

    def set_y_resonance_frequency(self, val):
        '''Adjust the y resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        logging.debug(f'set_y_resonance_frequency({val})')
        if int(val) < defaults.LIMIT_MIN_FREQ or int(val) > defaults.LIMIT_MAX_FREQ:
            raise base.OutofRangeError('Y Resonant frequency')
        self._request(base.GENERAL_BANK, 27, int(val))

    def get_configured_y_frequency(self):
        '''Get the configured y resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        logging.debug('get_conf_y_resonance_frequency()')
        response = self._request(base.GENERAL_BANK, 27)
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 19, 0)) < 0:
            val = unpack_response('f', response)[0]
        else:
            val = unpack_response('I', response)[0]
        return val

    def get_operational_y_frequency(self):
        '''Get the operational y resonant frequency (Hz) of the scanner (range: [1000, 10000])'''
        logging.debug('get_op_y_resonance_frequency()')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 19, 0)) < 0:
            raise base.IncompatibleAPIVersion(pyver=SemanticVersion(0, 19, 0), ucver=self.firmware_info.api_version)
        response = self._request(base.GENERAL_BANK, 49)
        val = unpack_response('f', response)[0]
        return val

    def set_threshold(self, val):
        '''Adjust the trigger threshold to the specified value (range: [0.0, 3.3])'''
        logging.debug(f'set_threshold({val})')
        if float(val) < 0.0 or float(val) > defaults.LIMIT_MAX_THRESHOLD:
            raise base.OutofRangeError('Threshold')
        intval = int(float(val) / defaults.LIMIT_MAX_THRESHOLD * 4095)
        self._request(base.GENERAL_BANK, 13, intval)

    def set_threshold2(self, val):
        '''Adjust the trigger threshold 2 to the specified value (range: [0.0, 3.3])'''
        logging.debug(f'set_threshold2({val})')
        if float(val) < 0.0 or float(val) > defaults.LIMIT_MAX_THRESHOLD:
            raise base.OutofRangeError('Threshold 2')
        intval = int(float(val) / defaults.LIMIT_MAX_THRESHOLD * 4095)
        self._request(base.GENERAL_BANK, 16, intval)

    def set_report_data_direction(self, val):
        '''Sets the direction of the reported tracking data (range: [0, 1])'''
        logging.debug(f'set_tracking_data_orientation({val})')
        if int(val) < 0 or int(val) > 3:
            raise base.OutofRangeError('Orientation')
        self._request(base.GENERAL_BANK, 14, int(val))

    def set_comparator_threshold(self, val):
        '''Sets the the comparator threshold for peak detect'''
        logging.debug(f'set_comparator_threshold({val})')
        if float(val) < 0.0 or float(val) > 3.3:
            raise base.OutofRangeError('Comparator threshold')
        intval = int(float(val) / 3.3 * 4095)
        self._request(base.GENERAL_BANK, 15, intval)

    def set_tracking_control(self, phase_lock, peak_lock):
        '''Configures low-level tracking controls'''
        logging.debug(f'set_tracking_control({phase_lock}, {peak_lock})')
        intval = (0x1 if phase_lock else 0x0) \
            | (0x2 if peak_lock else 0x0)
        self._request(base.GENERAL_BANK, 26, intval)

    def set_rampdown_us_per_step(self, val):
        '''Sets the ramp down delay taken per step until default position is reached'''
        logging.debug(f'set_rampdown_us_per_step({val})')
        self._request(base.GENERAL_BANK, 28, int(val))

    def set_rampup_us_per_step(self, val):
        '''Sets the ramp up delay taken per step until default position is reached'''
        logging.debug(f'set_rampup_us_per_step({val})')
        self._request(base.GENERAL_BANK, 29, int(val))

    def set_x_phase(self, val):
        '''Sets the X Phase to be used for eyetracking'''
        logging.debug(f'set_x_phase({val})')
        val = round(val * 4095 / 180)
        self._request(base.GENERAL_BANK, 30, int(val))

    def set_y_phase(self, val):
        '''Sets the Y Phase to be used for eyetracking'''
        logging.debug(f'set_y_phase({val})')
        val = round(val * 4095 / 180)
        self._request(base.GENERAL_BANK, 31, int(val))

    def set_photodiode_selection(self, val):
        '''Sets the photodiodes to be used when detecting glint pulses'''
        logging.debug(f'set_photodiode_selection({val})')
        self._request(base.GENERAL_BANK, 32, ctypes.c_int(val).value)

    def set_photodiode_gain(self, pdindex, val):
        '''Sets the gain for the specified photodiode'''
        logging.debug(f'set_photodiode_gain({pdindex}, {val})')
        if pdindex >= 6:
            raise base.OutofRangeError('Photodiode index')
        self._request(base.GENERAL_BANK, 33 + pdindex, val)

    def set_photodiode_gain_boost(self, val):
        '''Sets the gain boost option for the photodiodes'''
        logging.debug(f'set_photodiode_gain_boost({val})')
        self._request(base.GENERAL_BANK, 41, val)

    def set_glint_pw_max_threshold(self, val):
        '''Sets the tros tracking glint pulse width filter max threshold'''
        logging.debug(f'set_glint_pw_max_threshold({val})')
        self._request(base.GENERAL_BANK, 39, int(val))

    def set_glint_pw_min_threshold(self, val):
        '''Sets the tros tracking glint pulse width filter min threshold'''
        logging.debug(f'set_glint_pw_min_threshold({val})')
        self._request(base.GENERAL_BANK, 40, int(val))

    def set_pd_burst_rate_threshold(self, val):
        '''Sets the tros tracking per PD max data rate threshold'''
        logging.debug(f'set_pd_burst_rate_threshold({val})')
        self._request(base.GENERAL_BANK, 42, int(val))

    def set_total_rate_threshold(self, val):
        '''Sets the tros tracking total pulse rate threshold'''
        logging.debug(f'set_total_rate_threshold({val})')
        self._request(base.GENERAL_BANK, 43, int(val))

    def set_pupil_offset(self, val):
        '''Sets the pupil offset'''
        logging.debug(f'set_pupil_offset({val})')
        self._request(base.GENERAL_BANK, 45, val, datatype='float')

    def set_pupil_detector_selection(self, val):
        '''Sets the photodiodes to be used when detecting pupil pulses'''
        logging.debug(f'set_pupil_detector_selection({val})')
        self._request(base.GENERAL_BANK, 50, ctypes.c_int(val).value)

    def set_pupil_detector_gain(self, pdindex, val, boost):
        '''Sets the gain for the specified pupil photodiode'''
        logging.debug(f'set_pupil_detector_gain({pdindex}, {val}, {boost})')
        if pdindex >= defaults.MAX_PUPIL_DETECTORS:
            raise base.OutofRangeError('Photodiode index')
        self._request(base.GENERAL_BANK, 51 + pdindex, (boost << 16) | val)

    def set_pupil_pw_max_threshold(self, val):
        '''Sets the tros tracking pupil pulse width filter max threshold'''
        logging.debug(f'set_pupil_pw_max_threshold({val})')
        self._request(base.GENERAL_BANK, 46, int(val))

    def set_pupil_pw_min_threshold(self, val):
        '''Sets the tros tracking pupil pulse width filter min threshold'''
        logging.debug(f'set_pupil_pw_min_threshold({val})')
        self._request(base.GENERAL_BANK, 47, int(val))

    def set_x_dead_time(self, val):
        '''Sets the tros tracking x dead time'''
        logging.debug(f'set_x_dead_time({val})')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 23, 0)) < 0:
            logging.warning('This tracker does not support dead time API')
            return
        self._request(base.GENERAL_BANK, 53, int(val))

    def set_y_dead_time(self, val):
        '''Sets the tros tracking y dead time'''
        logging.debug(f'set_y_dead_time({val})')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 23, 0)) < 0:
            logging.warning('This tracker does not support dead time API')
            return
        self._request(base.GENERAL_BANK, 54, int(val))

    def set_dead_time_mode(self, val):
        '''Sets the tros tracking dead time mode'''
        logging.debug(f'set_dead_time_mode({val})')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 25, 0)) < 0:
            logging.warning('This tracker does not support dead time mode selection API')
            return
        self._request(base.GENERAL_BANK, 55, int(val))

    def get_device_geometry(self):
        '''Gets the kit geometry ID'''
        logging.debug('_get_device_geometry()')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 24, 0)) < 0:
            logging.warning('This tracker does not support get_geometry API')
            return 0
        response = self._request(base.SPEC_BANK, 38)
        val = unpack_response('<I', response)[0]
        return val

    def wipe_persistent_settings(self):
        '''Wipes the non-volatile settings saved by TROS'''
        logging.debug('wipe_persistent_settings()')
        self._request(base.ACTION_BANK, 3, 1, control=True)

    def flush_persistent_settings(self):
        '''Commits any uncommitted (cached) settings to TROS non-volatile memory'''
        logging.debug('flush_persistent_settings()')
        self._request(base.ACTION_BANK, 4, 1, control=True)


class BaseAppApi(GeneralApi):
    '''Common API for all applications'''

    # Currently there is no way to read the current running app from embedded,
    # so this is backends impression of what is running based on app api start/stop calls
    # Mostly used for logging purposes
    _current_app_by_trackerid = {}

    @classmethod
    def __init_subclass__(cls, app_id, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._app_id = app_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._started = False

    @property
    def started(self):
        '''Returns true if the application has been started through this api'''
        return self._started

    def add_error_callback(self, func):
        '''Add callback for critical communication related failures'''
        self._com.add_callback(lambda pkt: func(self._get_tracker_id(pkt.metadata.src_id),
                                                *unpack_stream('<BB', pkt.payload)),
                               0x100 | self._app_id,
                               key=func)

    def start(self):
        '''Start an application'''
        logging.debug(f'Starting app id: {self._app_id} on tracker {self.tracker_id + 1}')
        self._com.start_stream()
        if not self._readonly:
            if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 18, 0)) < 0:
                logging.warning('This tracker does not support reload configs')
            else:
                self._request(base.ACTION_BANK, 5, self._dest_id)
        try:
            self._request(base.ACTION_BANK, 1, int(self._app_id))
        except base.RequestFailed as excp:
            # Since tros can respond to the app_start api with RequestFailed error when the requested app or
            # channel in analogApp is not supported, and it could happen on normal usages, it's better to
            # hide the extra info in the error (bank and id) from the end-user.
            raise base.Error(excp.error)
        self._started = True
        self._current_app_by_trackerid[self.tracker_id] = self._app_id

    def stop(self):
        '''Stop the currently running application, if applicable'''
        logging.debug(f'Stopping app on tracker {self.tracker_id + 1}')
        self._com.stop_stream()
        if not self._readonly:
            self._request(base.ACTION_BANK, 2, 1, timeout=5)
        self._started = False
        self._current_app_by_trackerid[self.tracker_id] = None

    def _get_config(self, conf_id):
        '''Retrieves an application specific configuration parameter'''
        logging.debug(f'get_config({self._app_id}, {conf_id})')
        # note that no signedness should be assumed for a generalized config setter
        response = self._request(int(self._app_id), int(conf_id))
        return unpack_response('I', response)[0]

    def _config_app(self, conf_id, new_val):
        '''Adjust an application specific configuration parameter'''
        logging.debug(f'config_app({self._app_id}, {conf_id}, {new_val})')
        # print(f'[{self._dev_id}, {self._app_id}, {int(conf_id)}, {int(new_val)}]')
        # note that no signedness should be assumed for a generalized config setter
        self._request(int(self._app_id), int(conf_id), int(new_val))
