'''This module provides a base class and common APIs for interacting
with a device in the safe mode
'''

import enum
import logging
import struct
from collections import namedtuple

from . import base
from . import register_api
from . import registers
from . import publicapiproxy
from .version import SemanticVersion

# fault info packet_v1 data structure
FaultPacketV1 = namedtuple('FaultPacketV1', 'pkt_ver board_type fault_type build_version ecc_counter \
                                             ecc_addr assert_counter assert_addr r0 r1 r2 r3 r12 lr ret_addr xpsr')
# fault info packet_v2 data structure
FaultPacketV2 = namedtuple('FaultPacketV2', 'pkt_ver board_type fault_type build_version ecc_counter \
                                             ecc_addr assert_counter assert_addr r0 r1 r2 r3 r12 lr ret_addr xpsr \
                                             fileId pageId')


class RecoveryActions(enum.IntEnum):
    '''Available choices for safe mode recovery'''

    RESET_FLAG = 0
    FIRMWARE_UPDATE = 1
    ERASE_FILE = 2
    REBUILD_RECORDS_TABLE = 3


class SafeModeFaultTypes(enum.IntEnum):
    '''Safe mode fault types'''
    HARDFAULT = 1
    MEMFAULT = 2
    BUSFAULT = 3
    USAGEFAULT = 4
    FILEFAULT = 5


class SafeModeAPI(register_api.RegisterApi):
    '''Provides the API to communicate with a device in safe mode'''

    supported_api_version = SemanticVersion(0, 92, 0)

    def __init__(self, portname, **kwargs):
        super().__init__(portname, **kwargs)
        self._pubapi = publicapiproxy.PublicApiProxy(portname)

    def get_safe_mode_flag_status(self):
        '''Reads the safe mode flag status'''
        logging.debug('get_safe_mode_flag_status()')
        safe_mode = self.get_register(registers.ISP_SAFE_MODE, control=True)
        return bool(safe_mode)

    def set_safe_mode_flag_status(self, status):
        '''Reads the safe mode flag status'''
        logging.debug(f'set_safe_mode_flag_status({status})')
        self.set_register(registers.ISP_SAFE_MODE, status, control=True)

    def reset_mcu(self):
        '''Sends a command to reset the MCU'''
        logging.debug('reset_mcu()')
        self.set_register(registers.ISP_RESET_MCU, 1, control=True, ack=False)

    def read_fault_log(self):
        '''Reads the latest fault log from MCU'''
        logging.debug('read_fault_log()')
        err, fault_data = self._pubapi.read_fault_info()
        pkt = None
        if not err:
            if fault_data[0] == 0:
                logging.info('no fault log available')
                return None
            if fault_data[0] == 1:
                pkt = FaultPacketV1._asdict(FaultPacketV1._make(struct.unpack_from('<III32s12I', fault_data)))
            elif fault_data[0] == 2:
                pkt = FaultPacketV2._asdict(FaultPacketV2._make(struct.unpack_from('<III32s12Ibb', fault_data)))
            else:
                logging.info(f'fault log version is not supported, ver: {fault_data[0]}')

        # remove trailing zeros from build_version
        pkt['build_version'] = str(pkt['build_version'].decode("utf-8")).strip('\x00')
        return pkt

    def erase_file(self, file_id):
        '''Erases a file from MCU flash'''
        logging.debug(f'erase_file({file_id})')
        self.set_register(registers.GENERAL2_ERASE_FILE, file_id, control=True)

    def rebuild_record_table(self):
        '''Sends a command to tros to rebuild the file records table'''
        logging.debug('rebuild_record_table()')
        self.set_register(registers.GENERAL2_REBUILD_RECORDS_TABLE, 1, control=True)


def print_safe_mode_log(portname):
    '''Reads the latest fault log and prints it'''
    api = SafeModeAPI(portname)
    log = api.read_fault_log()
    logging.error(str(log))
    api.shutdown()


def recover(portname):
    '''recover from safe mode'''
    api = SafeModeAPI(portname)
    log = api.read_fault_log()
    logging.error(str(log))
    api.shutdown()
    if log['fault_type'] == SafeModeFaultTypes.FILEFAULT:
        logging.error('File corruption detected, Please contact AdHawk support for additional assistance')
        return False
    reset_flag(portname)
    return True


def reset_flag(portname):
    '''recover from safe mode by just resetting the flag'''
    api = SafeModeAPI(portname)
    api.set_safe_mode_flag_status(False)
    logging.warning("Safe Mode recovery complete. Please contact AdHawk support if this issue persists")
    try:
        api.reset_mcu()
    except base.MinimumAPIVersion:
        logging.warning("Firmware version is outdated, power cycle the board manually")
    api.shutdown()


def erase_file(portname, file_id):
    '''Recovers the kit by erasing the given file in tros'''
    api = SafeModeAPI(portname)
    try:
        api.erase_file(file_id)
        api.set_safe_mode_flag_status(False)
        logging.warning("Safe Mode recovery complete. Please contact AdHawk support if this issue persists")
    except base.MinimumAPIVersion:
        logging.error("Firmware version is outdated, update the firmware and try again")
    try:
        api.reset_mcu()
    except base.MinimumAPIVersion:
        logging.warning("Firmware version is outdated, power cycle the board manually")
    api.shutdown()


def rebuild_records_table(portname):
    '''Recovers the kit by erasing the given file in tros'''
    api = SafeModeAPI(portname)
    try:
        api.rebuild_record_table()
        api.set_safe_mode_flag_status(False)
        logging.warning("Safe Mode recovery complete. Please contact AdHawk support if this issue persists")
    except base.MinimumAPIVersion:
        logging.error("Firmware version is outdated, update the firmware and try again")
    try:
        api.reset_mcu()
    except base.MinimumAPIVersion:
        logging.warning("Firmware version is outdated, power cycle the board manually")
    api.shutdown()
