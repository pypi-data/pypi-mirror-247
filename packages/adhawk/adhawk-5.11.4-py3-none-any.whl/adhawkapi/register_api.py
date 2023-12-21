'''This module defines the API to access the hardware registers'''
import collections
import logging
import struct

from . import register_specs
from .base import BaseApi, MinimumAPIVersion
from .version import SemanticVersion


class RegisterApi(BaseApi):
    '''Hardware Register API'''

    _reg_specs = collections.OrderedDict()
    '''Internal data structure that holds the register specification'''

    def __init__(self, portname, **kwargs):
        super().__init__(portname, **kwargs)
        if not self._reg_specs:
            self._load_reg_spec()

    def dump(self):
        '''Dump all the registers and return it as a generator'''
        for bank_key, bank in self._reg_specs.items():
            for reg_key, reg_spec in bank['registers'].items():
                if not reg_spec.read_access:
                    continue
                try:
                    value = self.get_register((bank_key, reg_key))
                except MinimumAPIVersion as exc:
                    logging.warning(exc)
                    continue
                yield f'{(bank_key, reg_key)}: {value}'

    def set_register(self, name, value, control=False, ack=True):
        '''Set the value of a register
        Args:
            name: constant from registers.py
            value: the value to set
            control: (bool) Whether to send the request to the control device
            ack: (bool) defines that this API has any response or not
        Returns:
            Response from the device
        Raises:
            ValueError if the value is not valid
            MinimumAPIVersion if this register is not supported by the firmware
        '''
        reg_spec = register_specs.get_reg_spec(self._reg_specs, *name)
        self._check_compatibility(reg_spec)
        reg_value = reg_spec.transform(value)
        if reg_spec.type == 'str' or reg_spec.type == 'bytes':
            self._request_str(
                reg_spec.bank, reg_spec.register, reg_spec.size, reg_value, control=control, ack=ack,
                encode=(reg_spec.type == 'str'))
            return 0  # default to success since _request_str doesn't tell us the response
        # logging.debug(f'{name}: user value {value}, reg value {reg_value}')
        res = self._request(reg_spec.bank, reg_spec.register, reg_value, datatype=reg_spec.type,
                            control=control, ack=ack)
        return struct.unpack('<I', res) if ack else None

    def get_register(self, name, control=False):
        '''Get the value of a register
        Args:
            name: constant from registers.py
            value: the value to set
            control: (bool) Whether to send the request to the control device
        Returns:
            The value of the register
        Raises:
            MinimumAPIVersion if this register is not supported by the firmware
        '''
        reg_spec = register_specs.get_reg_spec(self._reg_specs, *name)
        self._check_compatibility(reg_spec)
        if reg_spec.type == 'str':
            reg_value = self._request_str(reg_spec.bank, reg_spec.register, reg_spec.size, retries=3,
                                          control=control, encode=True)
            reg_value.strip(' \0')
        elif reg_spec.type == 'bytes':
            reg_value = self._request_str(reg_spec.bank, reg_spec.register, reg_spec.size, retries=3,
                                          control=control, encode=False)
        else:
            response = self._request(reg_spec.bank, reg_spec.register, control=control)
            reg_value = reg_spec.unpack(response)
        # print(f'{name}: reg value {reg_value}')
        value = reg_spec.invert(reg_value)
        if isinstance(value, float):
            value = round(value, 2)
        # print(f'{name}: user value {value}')
        return value

    def _check_compatibility(self, reg_spec):
        major, minor, patch = reg_spec.version.split('.')
        reg_version = SemanticVersion(major, minor, patch)
        if SemanticVersion.compare(self.firmware_info.api_version, reg_version) < 0:
            raise MinimumAPIVersion(f'{reg_spec.name} is not supported in firmware {self.firmware_info.api_version}')

    @classmethod
    def _load_reg_spec(cls):
        '''Read and load the register specification
        '''
        if cls._reg_specs:
            # Previously loaded by another instance
            return
        cls._reg_specs = register_specs.load_reg_spec()
