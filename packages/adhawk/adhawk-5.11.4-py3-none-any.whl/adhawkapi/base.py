'''This module provides the base class as well as the common APIs for all
Adhawk's applications
'''

import collections
import enum
import logging
import struct
import os

from .error import Error, CommunicationError
from .packet import PacketType
from .packetizedcom import PacketizedCom
from . import defaults
from . import registers
from .remotediscovery import RemoteEyetrackerDiscovery
from .utils import unpack_response
from .version import SemanticVersion


ACTION_BANK = 0xff
SPEC_BANK = 0xfe
GENERAL_BANK = 0xfd
ISP_BANK = 0xfc


class RequestTimedOutError(CommunicationError):
    '''Request was never acknowledged by the embedded system'''


class RequestFailed(Error):
    '''Request indicated a failure in its response'''

    _error_code_strings = {
        1: 'Bad Argument',
        2: 'Busy',
        3: 'Timeout',
        10: 'Read-only register',
        11: 'Write-only register',
        13: 'Value out of range',
        34: 'Not supported',
        60: 'Flash error',
    }

    # pylint: disable=too-many-arguments
    def __init__(self, dest_id, bank, addr, errorcode, extra=None):

        error = RequestFailed._error_code_strings.get(errorcode, f'error code ({errorcode})')
        super().__init__(f'Request ({hex(bank)}, {hex(addr)}) to device {dest_id} '
                         f'failed: {error}')
        self._dest_id = dest_id
        self._bank = bank
        self._addr = addr
        self._errorcode = errorcode
        self._extra = extra

        self.error = error


class IncompatibleAPIVersion(Error):
    '''Version of embedded application is not fully compatible with this GUI'''

    def __init__(self, pyver, ucver):
        if pyver.minor > ucver.minor or pyver.major > ucver.major:
            comp = 'microcode'
        elif ucver.major > pyver.major:
            comp = 'Python API'
        super().__init__(f'Outdated {comp} (Python API: {pyver}, microcode: {ucver})')


class MinimumAPIVersion(Error):
    '''Version of embedded application is not able to program with this GUI'''
    pass


class InvalidDeviceId(Error):
    '''Requested device is not available on the selected port'''
    pass


class OutofRangeError(Error):
    '''Raised in response to arguments out of acceptable range'''

    def __str__(self):
        return 'Out of range value: ' + super().__str__()


class DeviceFileFault(Error):
    '''Raised by one or more trackers to indicate data corruption'''
    pass


class PhotodiodeIndex(enum.IntEnum):
    '''Specifies the photodiode Id'''
    PD1 = 0
    PD2 = 1
    PD3 = 2
    PD4 = 3
    PD5 = 4
    PD6 = 5
    PUPIL_PD1 = 6
    PUPIL_PD2 = 7
    NA_PD = 0x0F  # PD is not available or disabled


FirmwareInfo = collections.namedtuple('FirmwareInfo',
                                      'api_version, product_category, build_num, serial_num, num_devices,'
                                      'dev_id_offset, num_trackers, active_trackers, active_eyes, sim, safe_mode')
'''Helper container to cache Firmware related information'''


class BaseApi:
    '''Base API class to manage common communication and validation tasks'''

    _openports = {}
    _endpoints_by_port_devid = collections.defaultdict(dict)
    _endpoints_by_trackerid = {}

    supported_api_version = SemanticVersion(0, 21, 0)

    @classmethod
    def shutdown_all(cls):
        '''Shutdown all communication ports prior to exiting main application'''
        while cls._openports:
            _, openport = cls._openports.popitem()
            com, _fwinfo = openport
            com.shutdown()
        cls._endpoints_by_trackerid.clear()
        cls._endpoints_by_port_devid.clear()
        RemoteEyetrackerDiscovery.get_instance().shutdown()

    @classmethod
    def open_ports(cls):
        '''Returns the currently opened ports'''
        return cls._openports

    @classmethod
    def from_tracker_id(cls, tracker_id, **kwargs):
        '''Construct a new API given a pre-existing global tracker id'''
        portname, dest_id = cls._endpoints_by_trackerid[tracker_id]
        api = cls(portname, **kwargs)
        api.set_tracker_id(tracker_id, dest_id)
        return api

    def __init__(self, portname, **kwargs):
        if os.path.islink(portname):
            portname = os.path.realpath(portname)
        self._portname = portname
        self._readonly = kwargs.get('readonly', False)
        self._dest_id = 0
        if portname in self._openports:
            # reuse an existing port
            self._com, _ = self._openports[portname]
        else:
            # open a new port
            self._com = self._create_com(kwargs.get('fault_callback'))

            try:
                if 'firmware_info' in kwargs:
                    firmware_info = kwargs.get('firmware_info')
                else:
                    firmware_info = self._build_firmware_info()
                logging.debug(firmware_info)
            except Error:
                if portname in self._openports:
                    # in case this was a reused port, make sure to mark it as closed
                    del self._openports[portname]
                self._com.shutdown()
                raise
            else:
                self._openports[portname] = (self._com, firmware_info)
            logging.info(f'Opened port {portname} ({firmware_info.serial_num})')

    def stats(self):
        '''Returns the number of received / dropped packets'''
        return self._com.stats()

    @property
    def portname(self):
        '''Returns portname this API instance is using to communicate to firmware'''
        return self._portname

    @property
    def firmware_info(self):
        '''Returns identification information retrieved from the firmware'''
        try:
            return self._openports[self.portname][1]
        except KeyError:
            raise CommunicationError()

    def add_fault_callback(self, func):
        '''Add callback for critical communication related failures'''
        self._com.add_fault_callback(func)

    def remove_callback(self, func):
        '''Remove a callback from the underlying com layer'''
        self._com.remove_callback(func)

    def shutdown(self):
        '''Shutsdown the communication to microcontroller and closes the port'''
        logging.debug(f'Shutting down {self.__class__.__name__} on port {self._portname}')
        self._com.shutdown()

        if self._portname in self._openports:
            for tracker_id in self._endpoints_by_port_devid[self._portname].values():
                del self._endpoints_by_trackerid[tracker_id]
            del self._endpoints_by_port_devid[self._portname]
            del self._openports[self._portname]

    @property
    def dest_id(self):
        '''Returns the currently selected device id for communication'''
        return self._dest_id

    @property
    def tracker_id(self):
        '''Returns the current selected tracker id for the currently selected device id'''
        return self._get_tracker_id(self.dest_id)

    @dest_id.setter
    def dest_id(self, dest_id):
        '''Adjust the device id to communicate for subsequent commands'''
        # logging.debug(f'Setting Device id to ({dest_id})')
        min_id = self.firmware_info.dev_id_offset
        max_id = min_id + self.firmware_info.num_devices
        if dest_id < min_id:
            raise InvalidDeviceId(f'Device {dest_id + 1} is not available from this connection.')
        if dest_id >= max_id:
            raise InvalidDeviceId(f'Device {dest_id + 1} is not configured.')
        self._dest_id = dest_id

    def _get_tracker_id(self, dest_id):
        return self._endpoints_by_port_devid[self._portname].get(dest_id, dest_id)

    def set_tracker_id(self, tracker_id, dest_id=None):
        '''Adjust the device id to communicate for subsequent commands'''
        min_id = self.firmware_info.dev_id_offset
        max_id = min_id + self.firmware_info.num_trackers
        dest_id = tracker_id if dest_id is None else dest_id
        if dest_id < min_id:
            raise InvalidDeviceId(f'Tracker {tracker_id + 1} is not available from this connection.')
        if dest_id >= max_id:
            raise InvalidDeviceId(f'Tracker {tracker_id + 1} is not configured.')
        self._dest_id = dest_id
        self._endpoints_by_port_devid[self._portname][dest_id] = tracker_id
        self._endpoints_by_trackerid[tracker_id] = (self.portname, dest_id)

    def _check_tros_version(self):
        """Attempts to talk to TROS and check its version"""
        try:
            apiver = self._get_tros_version(control=True)
        except CommunicationError as excp:
            raise CommunicationError(f'Could not retrieve API version: {excp}')
        else:
            logging.info(f'Python API Version: {self.supported_api_version}, Firmware API Version: {apiver}')
            if not self.supported_api_version.check_compatibility(apiver):
                raise IncompatibleAPIVersion(pyver=self.supported_api_version, ucver=apiver)
            return apiver

    @staticmethod
    def _get_active_eyes_and_trackers(ocular_mode):
        '''Helper function to get active eyes and active trackers from ocular mode'''
        active_eyes = []
        for eye in range(defaults.MAX_EYES):
            if ocular_mode.value & 1 << eye:
                active_eyes.append(eye)

        active_trackers = []
        for tracker_id in range(defaults.MAX_SCANNERS):
            # In the future, check the capability of each tracker to determine
            # which eye they belong to
            if ocular_mode.value & 1 << (tracker_id % defaults.MAX_EYES):
                active_trackers.append(tracker_id)
        return active_eyes, active_trackers

    def _build_firmware_info(self):
        # always start with API version to confirm a compatible endpoint
        # before issuing any other commands
        apiver = self._check_tros_version()

        num_devices, dev_id_offset, num_trackers = self._get_multidevice_config()
        # number of devices couldn't be zero, at least we are talking to a device now
        # this fixes the fully erased device programming
        num_devices = max(1, num_devices)
        product_category = self._get_product_category(control=True)

        if SemanticVersion.compare(apiver, SemanticVersion(0, 49, 0)) >= 0:
            active_eyes, active_trackers = self._get_active_eyes_and_trackers(self._get_ocular_mode(control=True))
        else:
            active_eyes, active_trackers = list(range(defaults.MAX_EYES)), list(range(defaults.MAX_SCANNERS))

        if SemanticVersion.compare(apiver, SemanticVersion(0, 5, 0)) >= 0:
            build_num = self._get_build_number(control=True)
            serial_num = self._get_serial_number(control=True)
        else:
            build_num = 'unknown'
            serial_num = 'unknown'
        logging.info(f'Firmware Version: {build_num}')

        if SemanticVersion.compare(apiver, SemanticVersion(0, 92, 0)) >= 0 and self._check_safe_mode():
            safe_mode = True
            serial_num = 'unknown - safe mode' if serial_num == '' else serial_num
        else:
            safe_mode = False

        return FirmwareInfo(apiver, product_category, build_num, serial_num,
                            num_devices, dev_id_offset, num_trackers,
                            tuple(active_trackers), tuple(active_eyes), False, safe_mode)

    def toggle_tros_to_bootloader(self, num_devices, starting_dev_id):
        '''Toggles the in-memory bootloader flag and resets the board from TROS to bootloader'''
        logging.debug(f'toggle_tros_to_bootloader({num_devices}, {starting_dev_id})')
        val = bytes([num_devices, starting_dev_id])
        payload = int.from_bytes(val, byteorder='big', signed=False)
        self._request(ACTION_BANK, 0, payload, ack=False, control=True)

    def _get_tros_version(self, control=False, timeout=2):
        """Attempts to talk to TROS and check its version"""
        logging.debug('get_tros_version()')
        response = self._request(GENERAL_BANK, 0, control=control, timeout=timeout)
        minor, major = unpack_response('<HH', response)
        logging.debug(f'tros version response {response}')
        return SemanticVersion(major, minor, 0)  # TROS API Versions don't use "patch", setting it to 0

    def _check_safe_mode(self):
        "Gets the safe mode flag status"
        logging.debug('check_safe_mode()')
        response = self._request(ISP_BANK, 12, control=True)
        return unpack_response('I', response)[0] == 1

    def _get_multidevice_config(self):
        '''Gets the number of trackers controlled over the same port'''
        logging.debug('get_multidevice_config()')
        response = self._request(GENERAL_BANK, 1, control=True)
        return unpack_response('<BBBB', response)[0:3]

    def _get_product_category(self, control=False):
        '''Gets the product id of the connected device'''
        logging.debug('get_product_category()')
        response = self._request(SPEC_BANK, 0, control=control)
        try:
            return registers.SpecProductCategory(unpack_response('<I', response)[0])
        except ValueError:
            return registers.SpecProductCategory.OTHER

    def _get_ocular_mode(self, control=False):
        '''Gets the tracker mapping of the connected device'''
        try:
            response = self._request(SPEC_BANK, 49, control=control)
            return registers.SpecOcularMode(unpack_response('<I', response)[0])
        except (RequestFailed, ValueError):
            return registers.SpecOcularMode.BINOCULAR

    def _get_build_number(self, control=False):
        '''Retrieves the build number of the embedded application'''
        logging.debug('get_build_number()')
        return self._request_str(SPEC_BANK, 10, 8, control=control)

    def _get_serial_number(self, control=False):
        '''Retrieves the serial number associated with the connected device'''
        logging.debug('get_serial_number()')
        return self._request_str(SPEC_BANK, 20, 8, control=control)

    def _create_com(self, fault_callback=None):
        return PacketizedCom(self._portname, fault_callback)

    def _request(self, bank, addr, val=None, **kwargs):
        '''Construct and send a packet over the underlying comm object
        Args:
            bank: The register bank to write or read from
            addr: The register address to write or read from
            val: The value to write, or None for read
            kwargs: Options [ack, timeout, retries, check_res_ids]
        Returns:
            Payload of the request received over the comm, or
            None if the no response was expected (ack=False) or API is in read-only mode
        '''
        if kwargs.get('control', False):
            dest_id = defaults.CONTROL_DEV_ID
        else:
            dest_id = self._dest_id

        if val is None:
            packet_type = int(kwargs.get('packettype', PacketType.READ))
            pkt = self._com.make_packet(packet_type, dest_id, struct.pack('<BB', bank, addr))
        else:
            fmt_map = {'int': 'i', 'uint': 'I', 'float': 'f', 'str': '4s'}
            if 'datatype' in kwargs and kwargs['datatype'] == 'str':
                assert len(val) == 4  # must be same size as int32
            if 'datatype' in kwargs:
                fmt = fmt_map.get(kwargs['datatype'], 'i')
            else:
                fmt = 'i'
            # we default data type to int32 for convenience (covers most setters)
            payload = struct.pack(f'<BB{fmt}', bank, addr, val)
            packet_type = int(kwargs.get('packettype', PacketType.WRITE))
            pkt = self._com.make_packet(packet_type, dest_id, payload)

        response = self.send_request(pkt, **kwargs)
        if response and response.metadata.error:
            raise RequestFailed(dest_id, bank, addr, response.payload[0])
        return response.payload if response else None

    def send_request(self, pkt, **kwargs):
        '''Send a packet over the underlying comm object
        Args:
            pkt: Packet constructed by the underlying comm object
            kwargs: Options [ack, timeout, retries]
        Returns:
            Response packet received over the comm, or
            None if the no response was expected (ack=False) or API is in read-only mode
        '''
        if pkt.metadata.write and self._readonly:
            logging.warning('API is in read-only mode')
            return None

        dest_id = pkt.metadata.dst_id
        expecting_ack = kwargs.get('ack', True)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 0)
        for retry in range(retries + 1):
            try:
                response = self._com.request(pkt, expecting_ack=expecting_ack, timeout=timeout)
            except Error:
                if retry >= retries:
                    raise
                logging.warning(f'Failed to send request ({pkt.header})'
                                f' to device {dest_id + 1} attempt {retry}')
            else:
                break
        return response

    @staticmethod
    def _expected_responders(dest_id):
        if dest_id == defaults.CONTROL_DEV_ID:
            return [0]
        return [dest_id]

    def _request_str(self, bank, addr, num_addrs, val=None, **kwargs):
        if val is None:
            reassembledval = b''
            for offset in range(num_addrs):
                reassembledval += (self._request(bank, addr + offset, **kwargs))
            if 'encode' in kwargs and kwargs['encode'] is False:
                return reassembledval
            return reassembledval.decode(errors='ignore').rstrip('\0')

        paddedval = f'{val:\0<{num_addrs*4}}'
        for offset in range(num_addrs):
            self._request(bank, addr + offset, paddedval[offset * 4:offset * 4 + 4].encode(),
                          datatype='str', **kwargs)
        return None
