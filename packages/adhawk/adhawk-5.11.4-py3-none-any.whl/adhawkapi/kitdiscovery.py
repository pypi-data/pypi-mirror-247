'''This module provides the ability to discover and connect to AdHawk devices'''

import dataclasses
import enum
import functools
import logging
import typing

from adhawktools import version as appversion

from . import SystemInfo, base, comportdiscovery, register_api, registers, simapi, version


# We always assign the eye trackers first, starting with right eye
_ENDPOINTS = {
    registers.SpecCapability.RIGHT_EYE: [0],
    registers.SpecCapability.LEFT_EYE: [1],
    registers.SpecCapability.EYE_TRACKER: [0, 1],
    registers.SpecCapability.PUPIL_TRACKER: [0, 1],
    registers.SpecCapability.EMBEDDED_ET: [2],
}

_APP_VERSION = appversion.AppVersion.get_version()


class KitStatusValue(enum.Enum):
    '''Indicates the current status of a kit'''
    READY = 0  # the kit is fully operational, and ready for use
    LOST = 1  # the kit is no longer detected
    COM_ERROR = 2  # encountered a communication failure while in operation
    UNRESPONSIVE = 3  # unable to communicate to device entirely
    SAFE_MODE = 4  # kit is up but is in safe mode due to an error


@dataclasses.dataclass
class KitStatus:
    '''Helper class for tracking the status of a kit'''
    val: KitStatusValue = KitStatusValue.READY


class Kit(typing.NamedTuple):
    '''Contains information regarding an eye tracking kit'''
    port: str
    serial_num: str
    active_eyes: tuple
    active_trackers: tuple
    api_version: version.SemanticVersion
    firmware_version: str
    product_id: registers.SpecProductId
    camera_type: registers.SpecCamera
    status: KitStatus

    @property
    def faulted(self):
        '''Returns whether this kit has encountered an error and needs to be reset'''
        return self.status.val == KitStatusValue.COM_ERROR

    @faulted.setter
    def faulted(self, val):
        '''Marks this kit as faulted'''
        # the user is only allowed to set faulted, and we automatically clear
        # when a kit is unplugged and plugged back in.
        assert val
        self.status.val = KitStatusValue.COM_ERROR

    @property
    def lost(self):
        '''Returns wether this kit has been disconnected'''
        return self.status.val == KitStatusValue.LOST

    @lost.setter
    def lost(self, val):
        '''Indicate that this kit has been disconnected'''
        assert val
        self.status.val = KitStatusValue.LOST

    @property
    def ready(self):
        '''Returns whether this Kit is ready to use'''
        return self.status.val == KitStatusValue.READY

    @property
    def in_safe_mode(self):
        '''Returns true if this kit is in safe mode'''
        return self.status.val == KitStatusValue.SAFE_MODE

    @property
    def sys_info(self):
        '''Returns the system information associated with this kit'''
        return {
            SystemInfo.CAMERA_TYPE: self.camera_type,
            SystemInfo.DEVICE_SERIAL: self.serial_num,
            SystemInfo.FIRMWARE_API: self.api_version,
            SystemInfo.FIRMWARE_VERSION: self.firmware_version,
            SystemInfo.EYE_MASK: functools.reduce(lambda m, t: 1 << t | m, self.active_eyes, 0),
            SystemInfo.PRODUCT_ID: self.product_id,
            SystemInfo.BACKEND_VERSION: _APP_VERSION,
        }

    def get_endpoints(self, cap):
        '''Returns the set endpoints with the specified capability'''
        devids = set(_ENDPOINTS[cap]) & set([*self.active_eyes, 2])
        return [(self.port, devid) for devid in devids]


class DeviceList:
    '''Automatically detects AdHawk's Eyetrackers by monitoring the list of ports'''

    def __init__(self):
        self._port2kit = {}

    def shutdown(self):
        '''Terminate the discovery process'''
        pass

    def reset(self):
        '''Shutdown all ports and clean up the references to them'''
        self._port2kit = {}

    @property
    def kits(self):
        '''Returns all valid kits'''
        return list(self._port2kit.values())

    def check_for_devices(self):
        '''Check for new devices'''
        available_ports = comportdiscovery.compatible_ports()

        # We trigger a disconnect/reconnect for faulted devices in cases where
        # the api/services were momentarily interrupted, and we can possibly
        # recover with a reinitialization
        faultedports = [port
                        for port, kit in self._port2kit.items()
                        if kit is not None and kit.faulted]
        deletedports = [port for port in self._port2kit if port not in available_ports]

        for port in set(deletedports + faultedports):
            logging.info(f'Deleting port {port}')
            kit = self._port2kit[port]
            kit.lost = True
            del self._port2kit[port]
            logging.info(f'Kit {kit.serial_num} is no longer available!')

        newports = [port for port in available_ports if port not in self._port2kit]
        for port in newports:
            logging.info(f'New port {port}')
            kit = self._kit_from_port(port)
            self._port2kit[port] = kit
            logging.info(f'Kit {kit.serial_num} is available!')

    @staticmethod
    def _kit_from_port(port):
        try:
            api = register_api.RegisterApi(port)
        except base.Error as excp:
            logging.warning(f'Failed to connect to port {port}: {excp}')
            # port is blacklisted at this point, and won't try it again
            return Kit(port, 'Unknown',
                       (), (),
                       version.SemanticVersion(0, 0, 0),
                       'unknown',
                       registers.SpecProductId.UNKNOWN,
                       registers.SpecCamera.NOT_AVAILABLE,
                       KitStatus(KitStatusValue.UNRESPONSIVE))

        kit_status = KitStatusValue.READY
        if api.firmware_info.safe_mode:
            kit_status = KitStatusValue.SAFE_MODE

        try:
            product_id = api.get_register(registers.SPEC_PRODUCT_ID, control=True)
            camera_type = api.get_register(registers.SPEC_CAMERA, control=True)
        except base.CommunicationError:
            product_id = registers.SpecProductId.UNKNOWN
            camera_type = registers.SpecCamera.NOT_AVAILABLE
            kit_status = KitStatusValue.COM_ERROR

        kit = Kit(port,
                  api.firmware_info.serial_num,
                  api.firmware_info.active_eyes,
                  api.firmware_info.active_trackers,
                  api.firmware_info.api_version,
                  api.firmware_info.build_num,
                  product_id,
                  camera_type,
                  KitStatus(kit_status))
        api.shutdown()
        return kit


class SimDeviceList:
    '''Virtual device list providing the sim kit'''

    def __init__(self, serial_num):
        self._api = None
        self._kit = None
        simapi.SimApi.set_serial_num(serial_num)

    def shutdown(self):
        '''Terminate the discovery process'''
        logging.info('Shutting down port discovery')
        self._api.shutdown()

    def reset(self):
        '''Shutdown all ports and clean up the references to them'''
        pass

    @property
    def kits(self):
        '''Returns all valid kits'''
        return [] if self._kit is None else [self._kit]

    def check_for_devices(self):
        '''Check for new devices'''
        if self._api is not None:
            return

        self._api = simapi.SimApi()
        product_id = self._api.get_register(registers.SPEC_PRODUCT_ID, control=True)
        self._kit = Kit('virtualport',
                        self._api.firmware_info.serial_num,
                        self._api.firmware_info.active_eyes,
                        self._api.firmware_info.active_trackers,
                        self._api.firmware_info.api_version,
                        self._api.firmware_info.build_num,
                        product_id,
                        registers.SpecCamera.NOT_AVAILABLE,
                        KitStatus(KitStatusValue.READY))
