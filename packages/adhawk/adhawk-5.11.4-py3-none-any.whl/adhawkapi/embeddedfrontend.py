
'''This module provides a pseudo API for an embedded frontend application'''

import logging
from . import base
from . import registers


class EmbeddedFrontend:
    '''Provides the necessary information used in port discovery for an
       embedded frontend application'''

    def __init__(self, portname):
        self._portname = portname
        self._firmware_info = base.FirmwareInfo(1, registers.SpecProductCategory.HMD,
                                                'unknown', 'frontend', 1, 0, 0, (), (), False)

    @property
    def portname(self):
        '''Returns portname this API instance is using to communicate to firmware'''
        return self._portname

    @property
    def firmware_info(self):
        '''Returns identification information retrieved from the firmware'''
        return self._firmware_info

    def shutdown(self):
        '''Shutsdown the communication to microcontroller and closes the port'''
        logging.debug(f'Shutting down {self.__class__.__name__} on port {self._portname}')
        pass

    def get_capability(self, control=False):
        '''Retrieves the capabilities of the specified endpoint'''
        logging.debug(f'get_capability() {control} for {self.__class__.__name__} on port {self._portname}')
        return [registers.SpecCapability.EMBEDDED_FRONTEND]
