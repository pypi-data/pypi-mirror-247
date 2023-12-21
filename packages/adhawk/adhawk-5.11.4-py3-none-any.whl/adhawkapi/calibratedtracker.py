'''This module provides calibrated tracker related APIs'''

import enum
from . import baseapp
from . import utils


class DataType(enum.IntEnum):
    '''Various data types used in calibrated tracker API'''
    GAZE_POINT = 0


class CalibratedTracker(baseapp.BaseAppApi, app_id=0xf):
    '''Python frontend for AdHawk's calibrated tracker API'''

    def add_callback_calibrated_data(self, func):
        '''Add callback to retrieve calibrated x and y positions'''
        self._com.add_callback(lambda pkt: func(*utils.unpack_stream('<HHH', pkt.payload)),
                               DataType.GAZE_POINT << 4 | self._app_id,
                               key=func)
