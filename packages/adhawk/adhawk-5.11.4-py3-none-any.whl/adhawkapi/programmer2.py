'''This module provides a base class and common APIs for interacting
with the bootloader
'''
# pylint:disable=too-many-lines

import collections
import logging
import os
import struct
import time
import typing

from . import base
from . import board_defs
from . import com
from . import comportdiscovery
from . import error
from . import programmertools
from . import publicapiproxy
from . import register_api
from . import registers
from .packet import PacketType
from .utils import BadResponseError, unpack_response
from .version import SemanticVersion


FIRMWARE_PREFIX = 'firmware/'
CHUNK_SIZE = 4
ISP_BANK = 0xfc
PROGRAM_BOOTLOADER_MAGIC_NUMBER = 0x25
CHECKSUM_CHECK_STEPS = 256

IspFeatures = collections.namedtuple('IspFeatures', 'required_btl max_image_size encryption_supported required_fw')

ISP_CAPABILITIES = {
    0: IspFeatures(0.0, 0x20000, False, "0.0"),
    1: IspFeatures(1.0, 0x30000, False, "5.1"),
    2: IspFeatures(1.0, 0x30000, True, "5.5.1"),
}


class ProgrammerError(error.Error):
    '''General exception type for all programmer related errors'''
    pass


class ProgrammerFileError(ProgrammerError):
    '''General exception type for all programmer file related errors'''
    pass


class ProgrammerNotReady(ProgrammerError):
    '''Indicates that the device is not ready for programming
    In this case, set_programming_mode should be retried'''
    pass


class ProgrammerAPI2(register_api.RegisterApi):
    '''Provides the API to update and program the devices'''

    supported_api_version = SemanticVersion(0, 21, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # programmer should always communicate with the hub
        self._dest_id = max(0, self.firmware_info.num_devices - 1)

    def set_programming_mode(self, enable, bootloader=False):
        '''Enable/disable programming mode'''
        logging.debug(f'set_programming_mode({enable}, {bootloader})')
        val = int(enable)
        if bootloader:
            val |= PROGRAM_BOOTLOADER_MAGIC_NUMBER << 8
        self._request(ISP_BANK, 0, val, ack=False)

    def get_programming_mode(self, timeout):
        '''checks the status of programming mode'''
        logging.debug(f'get_programming_mode(timeout={timeout})')
        response = self._request(ISP_BANK, 0, timeout=timeout)
        enable = (response[0] & 0x1) == 0x1
        bootloader = bool(response[1] == PROGRAM_BOOTLOADER_MAGIC_NUMBER)
        return enable, bootloader

    def get_programmer_version(self):
        '''Gets the bootloader version'''
        logging.debug('get_programmer_version()')
        response = self._request(ISP_BANK, 1)
        # old TROS versions return 'API_version' in response
        minor, major = unpack_response('<HH', response)
        # The assumption here is, ISP version never catches the API version
        # in future since we used the following logic to find the old ISP.
        if SemanticVersion.compare(SemanticVersion(major, minor, 0),
                                   self.firmware_info.api_version) == 0:
            return 0
        return unpack_response('I', response)[0]

    def get_board_type(self):
        '''Gets the board type id'''
        logging.debug('get_board_type()')
        response = self._request(ISP_BANK, 2)
        return registers.IspBoardType(unpack_response('I', response)[0])

    def get_checksum(self):
        '''Gets the checksum of the given page'''
        response = self._request(ISP_BANK, 3)
        return unpack_response('I', response)[0]

    def read_isp_status(self):
        '''Reads the saved status of the tros ISP'''
        logging.debug('read_isp_status()')
        return self.get_register(registers.ISP_STATUS)

    def read_isp_error(self):
        '''Reads the ISP error register'''
        return self.get_register(registers.ISP_READ_ERROR)

    def get_inactive_image_id(self):
        '''Gets inactive image id that can be programmed'''
        logging.debug('get_inactive_image_id()')
        response = self._request(ISP_BANK, 4)
        return unpack_response('I', response)[0]

    def get_mcu_clock(self):
        '''Gets mcu running clock'''
        logging.debug('get_mcu_clock()')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 42, 0)) < 0:
            return 0
        response = self._request(base.GENERAL_BANK, 69)
        return unpack_response('I', response)[0]

    def get_faults(self):
        '''Collect all trackers' faults (if any) and return a dictionary'''
        faults = {}
        prev_dest_id = self._dest_id
        for trackerid in self.firmware_info.active_trackers:
            self.dest_id = trackerid
            try:
                status = self.get_register(registers.GENERAL2_TRACKER_STATUS)
                if len(status) != 0:
                    faults[trackerid] = status
            except base.MinimumAPIVersion:
                # tracker status not supported, no fault to collect
                pass
        self._dest_id = prev_dest_id
        logging.debug(f'Fault states per tracker ={faults}')
        return faults

    def is_image_stable(self):
        '''Gets whether the running image is stable'''
        logging.debug('is_image_stable()')
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 15, 0)) < 0:
            return True
        response = self._request(ISP_BANK, 5)
        return unpack_response('I', response)[0] == 1

    def set_image_as_stable(self):
        '''Sets the running image as stable'''
        logging.debug('set_image_as_stable()')
        self._request(ISP_BANK, 5, 1)

    def get_bootloader_version(self):
        '''Gets the bootloader version'''
        logging.debug('get_bootloader_version()')
        try:
            return self.get_register(registers.ISP_BOOTLOADER_VERSION)
        except base.MinimumAPIVersion:
            # this assumption is not always true but overall it's safer to assume that the btl is old
            return 0

    def write_to_flash(self, addr, data):
        '''Write to value to the device flash'''
        # logging.debug(f'write_to_flash({addr} , {data})')
        val = struct.unpack('<i', data)[0]
        _, _, bank, reg = struct.pack('>I', addr)
        _ = self._request(bank, reg, val, packettype=PacketType.ISP_WRITE, ack=False)

    def read_from_flash(self, addr):
        '''Read from the device flash memory'''
        logging.debug('read_from_flash()')
        bank, reg = unpack_response('<BB', addr)
        response = self._request(bank, reg, packettype=PacketType.ISP_READ)
        return unpack_response('I', response)[0]

    def write_setting(self, bankid, keyid, value, **kwargs):
        '''Sets any setting on any bank/key'''
        logging.info(f'write_setting Bank:{bankid} Key:{keyid} Value:{value}')
        self._request(bankid, keyid, value, **kwargs)

    def read_setting(self, bankid, keyid):
        '''Reads any setting on any bank/key'''
        logging.info(f'read_setting Bank:{bankid} Key:{keyid}')
        response = self._request(bankid, keyid)
        return unpack_response('<i', response)

    def stop_embedded_et(self):
        '''Stop the embedded_et'''
        logging.debug('Stopping Embedded_ET')
        pubapi = publicapiproxy.PublicApiProxy(self.portname)
        pubapi.disable_embedded_et()


DriveInfo = collections.namedtuple('DriveInfo', 'scan_mode, timer_clock')


class ProgrammingInfo(typing.NamedTuple):
    '''Contains the information used to program a board'''
    type: registers.IspBoardType
    category: board_defs.BoardCategory
    image_name: str
    image_version: str


class Programmer:
    '''Controller class for interacting with the bootloader and reporting progress'''

    def __init__(self, portname, **kwargs):

        self._info = kwargs.get('info_cb', logging.info)
        self._debug = kwargs.get('debug_cb', logging.debug)
        self._progress = kwargs.get('progress_cb', lambda _cur, _max: None)

        self._fault_ok = False
        self._faulted = False

        self._portname = portname
        self._progapi = ProgrammerAPI2(portname, fault_callback=self._handle_fault)
        self._progopts = []
        self._load()

    @property
    def available_options(self):
        '''Returns the set of programming options for the selected port'''
        return self._progopts

    def get_tros_build_number(self):
        ''' returns tros current build number'''
        return self._progapi.firmware_info.build_num

    def get_bootloader_version(self):
        ''' returns tros current bootloader version'''
        return self._progapi.get_bootloader_version()

    @property
    def safe_mode(self):
        ''' returns the device safe mode flag status'''
        return self._progapi.firmware_info.safe_mode

    def download_binary(self, opt):
        '''download a complete binary file '''
        try:
            self._print_isp_status()
            self._download_binary(f'{FIRMWARE_PREFIX}{opt.image_name}',
                                  opt.category == board_defs.BoardCategory.BOOTLOADER)
        finally:
            self._print_isp_status()

    def shutdown(self):
        '''Shuts down the programmer and any open APIs'''
        self._progapi.shutdown()
        self._progapi = None

    @staticmethod
    def _get_image_info(origpath):
        '''reads the TROS header from the given hex file '''
        # check the older firmware availability
        paths = [origpath, origpath.replace("_release.hex", "_combined.hex")]
        for path in paths:
            try:
                return path, programmertools.read_header_from_hex_file(FIRMWARE_PREFIX + path)
            except IOError:
                pass

        raise ProgrammerFileError('Unable to find a suitable firmware file')

    def _load(self):
        board_type = self._progapi.get_board_type()
        programmers_configs = board_defs.BOARD_PROGRAMMER_CONFIGS[board_type]
        for category, image_name, _ in programmers_configs:
            actual_name, header = self._get_image_info(image_name)
            if category == board_defs.BoardCategory.BOOTLOADER:
                image_version = header['bootloader_version']
            else:
                image_version = header["build_version"].strip('"')
            prginfo = ProgrammingInfo(board_type, category, actual_name, image_version)
            self._progopts.append(prginfo)

    @staticmethod
    def _get_minimum_supported_isp(sector_size, new_image_encryption):
        '''Returns the minimum ISP version required for supporting the new image size and encryption method'''
        for version, isp in ISP_CAPABILITIES.items():
            if int(isp.max_image_size) >= sector_size and \
               new_image_encryption == isp.encryption_supported:
                return version, isp.required_btl, isp.required_fw
        raise ProgrammerError('Firmware not supported')

    @staticmethod
    def _get_image_boundaries(header, board_type, sector_id, program_btl):
        '''returns the target image start and end addresses'''
        mcu_type = board_defs.BOARD_PROGRAMMER_CONFIGS[board_type][0][2]
        start_addr = board_defs.MCU_SECTOR_MAPPING[mcu_type][sector_id][0]
        end_addr = board_defs.MCU_SECTOR_MAPPING[mcu_type][sector_id][1]
        if header and not program_btl:
            try:
                start_addr = int(header[f'image{sector_id}_address'], 0)
                end_addr = start_addr + int(header['max_image_size'], 0)
            except KeyError as excp:
                raise ProgrammerFileError(f'Could not find {excp} key in the hex header file')
        return start_addr, end_addr

    def _verify_isp_compatibility(self, target_build_id, sec_start_addr, sec_end_addr, encrypted):
        '''Checks the new image compatibility with running ISP and sends encryption handshakes'''
        current_isp_version = self._progapi.get_programmer_version()
        min_isp, min_btl, min_fw = self._get_minimum_supported_isp(sec_end_addr - sec_start_addr, encrypted)
        if current_isp_version < min_isp:
            raise ProgrammerError(f'Current ISP version is too old, update firmware to v{min_fw} and try again')

        btl_version = self._progapi.get_bootloader_version()
        if btl_version < min_btl:
            raise ProgrammerError('Bootloader update is required, update the bootloader and try again')

        if encrypted:
            self._progapi.set_register(registers.ISP_TARGET_ISP_VERSION, min_isp)
            self._progapi.set_register(registers.ISP_TARGET_BUILD_ID, target_build_id)

    def _print_isp_status(self):
        '''prints the latest isp status code (only in debug logging mode)'''
        if SemanticVersion.compare(self._progapi.firmware_info.api_version, SemanticVersion(0, 90, 0)) >= 0:
            logging.debug(f"ISP status code: {hex(self._progapi.read_isp_status())}")

    def _download_binary(self, path, program_btl=False):
        '''download a complete binary file '''
        self._info('Retrieving programming information')
        # this fixes the fully erased board programming issue

        board_type = self._progapi.get_board_type()

        if not os.path.exists(path):
            raise ProgrammerFileError(f'Did not find firmware file: {path}')

        # Stop the embedded et before start updating firmware to
        # reduce MCU utilization while writing to the flash
        self._progapi.stop_embedded_et()

        self._info('Activating the programmer...')
        try:
            self._set_programming_mode(True, program_btl)
        except ProgrammerNotReady:
            # Retry once to allow the device to reset into a stable image
            self._set_programming_mode(True, program_btl)
        self._info('Programmer ready.')

        try:
            image_id = self._progapi.get_inactive_image_id()
        except BadResponseError:
            # retry if the MCU is still busy on set_programming_mode
            image_id = self._progapi.get_inactive_image_id()

        sector_id = 0 if program_btl else image_id + 1
        self._info('Reading binary...')
        header = programmertools.read_header_from_hex_file(path)
        start_addr, end_addr = self._get_image_boundaries(header, board_type, sector_id, program_btl)
        target_build_id = sum(str.encode(header['build_version'].strip('"')))
        self._verify_isp_compatibility(target_build_id, start_addr, end_addr, "release" in path)
        chunks = programmertools.read_and_format_hex_file(path, start_addr, end_addr, CHUNK_SIZE)
        if not chunks:
            raise ProgrammerFileError(f'Invalid/corrupt firmware file: {path}')

        self._info('Downloading binary...')
        self._write_chunks(chunks)
        self._info('Download complete.')

        self._info('Starting new program...')
        fault = None
        try:
            self._set_programming_mode(False)
        except base.DeviceFileFault as excp:
            # we can tolerate a file fault if there are no other issues during fwup
            fault = excp

        if board_type != self._progapi.get_board_type():
            raise ProgrammerError('Failed to validate new program:'
                                  f' expected: {board_type}, got: {self._progapi.get_board_type()}')

        if header and not program_btl and header['build_version'].strip('"') != self._progapi.firmware_info.build_num:
            raise ProgrammerError('Update Failed, reverted to previous firmware')

        self._progapi.set_image_as_stable()

        final_msg = 'Firmware update completed'
        final_msg += ' successfully' if not fault else ' with and error'

        self._info(final_msg)

        if fault:
            raise fault

    def _get_new_api(self, port, serial_num):
        '''Find the com port for the device (it could have changed) and connect to it'''
        retries = 20
        for retry in range(retries + 1):
            try:
                api = ProgrammerAPI2(port, fault_callback=self._handle_fault)
                if api.firmware_info.serial_num == serial_num:
                    return api
                api.shutdown()
            except com.CommunicationError:
                pass

            if retry < retries:  # don't sleep on the last cycle
                time.sleep(0.5)

        # in case the port changed
        available_ports = comportdiscovery.compatible_ports()
        for newport in available_ports:
            try:
                api = ProgrammerAPI2(newport, fault_callback=self._handle_fault)
                if api.firmware_info.serial_num == serial_num:
                    return api
                api.shutdown()
            except com.CommunicationError:
                pass

        raise ProgrammerError('Failed to enable programming')

    def _set_programming_mode(self, enable, program_bootloader=False):
        '''Enable/disable the programming mode on the mcu'''

        stable = self._progapi.is_image_stable()
        port = self._progapi.portname
        firmware_info = self._progapi.firmware_info
        self._progapi.set_programming_mode(enable, program_bootloader)
        self._progapi.shutdown()

        self._fault_ok = True
        self._progapi = self._get_new_api(port, firmware_info.serial_num)
        self._fault_ok = False

        # Changing the programming mode (above) can perform a flash erase (slow) on the other sector
        # Wait longer for the following response to let the flash erase finish
        enable_result, bootloader_result = self._progapi.get_programming_mode(timeout=10.0)

        # check all trackers' status
        # certain faults (file corruption) must raise an error to be dealt with
        file_faulted = False
        for trackerid, fault in self._progapi.get_faults().items():
            if registers.General2TrackerStatus.FILE_CORRUPTION_FAULT.value in fault:
                logging.error(f'Tracker {trackerid + 1} has raised a file fault')
                file_faulted = True

        if enable_result != enable or bootloader_result != program_bootloader:
            if stable:
                isp_error = self._progapi.read_isp_error()
                raise ProgrammerError(f'Firmware did not accept programming mode, error code: {isp_error}')
            raise ProgrammerNotReady('Current image is not stable. Please retry')

        # do this check last so we may catch any other errors that gives us a lead into what happened
        if file_faulted:
            raise base.DeviceFileFault(
                'A hardware fault occurred. Please disconnect and reconnect your device. '
                'Contact AdHawk support if the issue persists.')

    def _write_chunks(self, chunks):
        try:
            total_checksum = 0
            total_chunks = len(chunks)
            starting_chunk = 0
            retries = 0
            while starting_chunk < total_chunks:
                for current_chunk in range(starting_chunk, min(total_chunks, starting_chunk + CHECKSUM_CHECK_STEPS)):
                    self._progapi.write_to_flash(current_chunk, chunks[current_chunk])
                    for i in range(CHUNK_SIZE):
                        total_checksum += chunks[current_chunk][i]
                    self._progress(current_chunk + 1, total_chunks)  # 1-indexed
                # use the old ISP logic for backward compatibility if tros firmware is old
                if SemanticVersion.compare(self._progapi.firmware_info.api_version, SemanticVersion(0, 51, 0)) < 0:
                    if self._progapi.get_checksum() != total_checksum & 0xffffffff:
                        raise ProgrammerError('Checksum error')
                else:
                    # Send the flush command with the current checksum
                    self._progapi.set_register(registers.ISP_FLUSH_BUFFER, total_checksum & 0xffffffff)
                    isp_error = self._progapi.read_isp_error()
                    if isp_error:
                        if retries < 3:
                            retries += 1
                            continue
                        raise ProgrammerError(f'ISP write failed with error code : {isp_error}')
                starting_chunk += CHECKSUM_CHECK_STEPS
                retries = 0
        except ProgrammerError:
            self._progapi.shutdown()
            self._progapi = None
            raise

    def _handle_fault(self, _excp):
        self._faulted = True
        if self._fault_ok:
            self._info("Got fault but it's okay")
            self._progapi.shutdown()
        else:
            logging.error('Tracker disconnected')
