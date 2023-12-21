'''This module provides lissajous-based tracking related APIs'''

import enum
from .publicapi import PacketType
from . import base
from . import baseapp
from . import defaults
from . import registers


class MegaLissajous(baseapp.BaseAppApi, app_id=5):
    '''Python frontend for AdHawk's lissajous-based tracking API'''

    class ConfId(enum.IntEnum):
        '''List of internal configuration commands for the tracker'''
        Y_MAX = 0
        Y_MIN = 1
        X_MAX = 2
        X_MIN = 3

    class DataType(enum.IntEnum):
        '''Tracker common data types'''
        LISSAJOUS_DATA = 0

    def set_y_max(self, val):
        '''Sets the maximum y position to track'''
        if int(val) < defaults.LIMIT_Y_MIN or int(val) > defaults.LIMIT_Y_MAX:
            raise base.OutofRangeError('Maximum y position to track')
        self.set_register(registers.MEGALISA_Y_MAX, val)

    def set_y_min(self, val):
        '''Sets the minimum y position to track'''
        if int(val) < defaults.LIMIT_Y_MIN or int(val) > defaults.LIMIT_Y_MAX:
            raise base.OutofRangeError('Minimum y position to track')
        self.set_register(registers.MEGALISA_Y_MIN, val)

    def set_x_range(self, xmin, xmax):
        '''Adjust the maximum x position of the scanner in resonant mode (range: [1, 1023])'''
        if int(xmin) < defaults.LIMIT_X_MIN:
            raise base.OutofRangeError('Minimum X position is lower than minimum allowed position')
        if int(xmax) > defaults.LIMIT_X_MAX:
            raise base.OutofRangeError('Maximum X position is greater than maximum allowed position')
        if int(xmin) > int(xmax):
            raise base.OutofRangeError('Maximum X position is lower than its minimum')
        self.set_register(registers.MEGALISA_X_MIN, xmin)
        self.set_register(registers.MEGALISA_X_MAX, xmax)

    def set_y_range(self, ymin, ymax):
        '''Adjust the maximum and minimum y position of the scanner in resonant mode (range:[1, 1023])'''
        if int(ymin) < defaults.LIMIT_X_MIN:
            raise base.OutofRangeError('Minimum y position is lower than minimum allowed position')
        if int(ymax) > defaults.LIMIT_X_MAX:
            raise base.OutofRangeError('Maximum y position is greater than maximum allowed position')
        if int(ymin) > int(ymax):
            raise base.OutofRangeError('Maximum y position is lower than its minimum')
        self.set_register(registers.MEGALISA_Y_MIN, ymin)
        self.set_register(registers.MEGALISA_Y_MAX, ymax)

    def set_stream_enable(self, enable):
        '''Enable/disable megalisa stream'''
        # ensure in-flight packets are stopped when the stream is stopped
        if enable:
            self._com.start_stream()
        else:
            self._com.stop_stream()
        self.set_register(registers.MEGALISA_STREAM_ENABLE, int(enable))

    def add_callback_lissajous_data(self, func):
        '''Add callback to retrieve time_ref, x, y, amplitude, and pulse width'''
        self._com.add_callback(lambda pkt: func(self._get_tracker_id(pkt.metadata.src_id),
                                                *pkt.unpack_payload('<HHHHHH')),
                               self.DataType.LISSAJOUS_DATA << 4 | self._app_id,
                               key=func)

    def remove_callback_lissajous_data(self, func):
        '''Remove a callback slotted to recieve lissajous data'''
        self._com.remove_callback(func)

    def add_tracker_status_callback(self, report_stream_cb):
        '''Add callback to retrieve tracker status'''
        self._com.add_callback(lambda pkt: report_stream_cb(*pkt.unpack_payload('<B')),
                               PacketType.TRACKER_STATUS, key=report_stream_cb)
