'''This module provides Customer Stream related APIs'''

import enum
from . import baseapp


class CustomerStream(baseapp.BaseAppApi, app_id=10):
    '''Implements the Python frontend for Adhawk's CustomerStream API'''

    class DataType(enum.IntEnum):
        '''Customer stream common data types'''
        RAW_DATA = 0

    def add_callback_customer_data(self, func):
        '''Add callback to retrieve customer data'''
        self._com.add_callback(lambda pkt: func(pkt.payload),
                               self.DataType.RAW_DATA << 4 | self._app_id,
                               key=func)
