'''This module provides Autotune related APIs

Autotune application is responsible for handling the initial tuning of
laser current, frequency, scan range, etc. to handle both variation in
devices and in people (and maybe in operating conditions)

'''

import enum
import struct

from adhawktools import model, recordingdata

from . import configs, publicapi, publicapiproxy, trackermodel
from .capi.py import libdatalogging as _cdatalogging
from .capi.py.util import buffer2ctypes
from .internal import PacketType


ERROR_MAP = {
    0: 'Glint not found',
    1: 'Invalid frequency setting',
    2: 'Glint not found: laser power may be too high',
    3: 'Glint not found: laser power may be too low',
    4: 'Attempting to take too many steps during line sweep in X axis',
    5: 'Attempting to take too many steps during line sweep in Y axis',
    6: 'Selected algorithm is not supported',
    8: 'Autophase not ready, please ensure you are looking straight ahead while auto-tuning',
    9: 'Pupil feature not detected, please ensure you are looking straight ahead while auto-tuning',
    10: 'Glint feature not detected, please ensure you are looking straight ahead while auto-tuning',
    11: 'Failed to solve for the desired scan range',
    12: 'Failed to solve for the eye position',
    13: 'Autotune result was out of bounds'
}


def autotune_message(errorcode):
    '''map autotune errorcode to error message'''
    return ERROR_MAP[errorcode]


class DataType(enum.IntEnum):
    '''Various data types streamed by the autotune application'''
    END_OF_TUNE = 0
    ERROR_DATA = 14


class Algorithm(enum.IntEnum):
    '''Available autotune algorithms'''
    NO_OP = 0
    LINESWEEP = 1
    GLINT_BASED_BOX_SIZING = 2
    PHYSMODEL = 3
    LASER = 4


class AutoTune:
    '''This class provides the ability to execute the autotune application in
    the microcode and retrieve the result

    Args:
        port (str): portname of the eye tracking hardware
        configmodel (ConfigModel): configuration model for tracker if available
        log_cb (callback(data)): callback to handle result and data logging

    '''

    def __init__(self, port, configmodel=None, log_cb=None):
        self._configmodel = configmodel
        self._log_cb = log_cb
        self._trackers_awaiting_results = None
        self._diag_data = None
        self._pubapi = publicapiproxy.PublicApiProxy(port)
        self._pubapi.register_analytics(self._handle_diag_info)

    def trigger(self, trackers, recording_configs, data=None):
        '''Start the autotune process'''

        self._trackers_awaiting_results = set(trackers)
        # Reinitialize diag_data because its cleared on finalize
        self._diag_data = recordingdata.RecordingData(configs=recording_configs)

        self._pubapi.start()

        result = self._pubapi.trigger_autotune(data)

        if result == publicapi.AckCodes.SUCCESS:
            if self._configmodel is not None:
                paths = []
                for trid in trackers:
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_XMEAN_PCT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_YMEAN_PCT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_WIDTH_PCT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_HEIGHT_PCT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_XMEAN))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_YMEAN))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_WIDTH))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_HEIGHT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_LASERCURRENT))
                    paths.append(trackermodel.construct_path(trid, configs.TRACKER_LASERCURRENTPCT))
                paths.append(configs.BLOB_TUNING_MULTIGLINT)

                self._configmodel.load(model.Subsystem.HARDWARE, paths)
                updated_configs = self._configmodel.paths_to_dict(paths)
                return result, updated_configs

        return result, None

    def _finalize(self):
        if self._log_cb is not None:
            self._log_cb(self._diag_data)
        self._trackers_awaiting_results = None
        self._diag_data = None

    def _handle_diag_info(self, data):
        if self._diag_data is None or data[0] != 1:
            return

        # Accumulating here is a bit ugly since the user of this module might not be using C datalogging
        # If a C dataloggins session isn't running this won't do anything
        packet = struct.pack('<B', PacketType.ANALYTICS) + data
        _cdatalogging.handle_device_data(buffer2ctypes(packet), len(packet))

        trackerid = data[1]
        info_type = data[2]
        self._diag_data['data'][str(trackerid)].append(
            info_type=info_type, info=list(data[3:]))
        if info_type in (DataType.END_OF_TUNE, DataType.ERROR_DATA):
            self._trackers_awaiting_results.remove(trackerid)
            if not self._trackers_awaiting_results:
                self._finalize()
