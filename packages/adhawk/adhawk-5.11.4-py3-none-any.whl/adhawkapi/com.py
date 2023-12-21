'''This module provides the low-level routines for communicating with Adhawk's
embedded devices. All application APIs is built on top of this layer.'''

import abc
import collections
import ctypes
import logging
import os
import time
import socket

import serial

from .error import CommunicationError, RecoverableCommunicationError
from .capi.py import libtracker_com as _ccom
from .capi.py.util import buffer2ctypes


WAIT_FOREVER = -1
RECEIVE_BUFFER_LENGTH = 16384


# Workaround pyserial exception with STM32 MCU (TRSW-165)
if os.name == 'nt':
    # pylint: disable=protected-access
    from serial.serialwin32 import Serial
    Serial._original_reconfigure_port = Serial._reconfigure_port

    def reconfigure_port_patch(inst):
        ''' patched Serial._reconfigure_port that doesn't raise exception '''
        try:
            Serial._original_reconfigure_port(inst)
        except serial.serialutil.SerialException:
            pass
    Serial._reconfigure_port = reconfigure_port_patch


class InvalidPortError(CommunicationError):
    '''Communication can not be established using specified port'''
    pass


class ReadTimedOutError(CommunicationError):
    '''Custom exception raised when the read operation is interrupted'''

    def __init__(self, expected_bytes, actual_bytes):
        super().__init__(f'Read timed out while expecting {expected_bytes} bytes,'
                         f' but got {actual_bytes} bytes')


class PortClosedError(CommunicationError):
    '''Communication has been seized in order to shutdown'''

    def __init__(self):
        super().__init__('Port is already closed or shutting down')


class InvalidLengthError(RecoverableCommunicationError):
    '''Received packet length did not match the length in the header'''
    pass


class BaseCom(abc.ABC):
    '''Base class for communication between devices'''

    @property
    def codec(self):
        '''The codec used over the comm if any'''
        return None

    def write(self, data):
        '''Writes one or more bytes to the microcontroller
        Args:
            data (bytes): list of bytes to send to the microcontroller
        '''
        if self.codec:
            data = self.codec.encode(data)
        return self._write(data)

    def read(self, numbytes, timeout=WAIT_FOREVER):
        '''Reads one or more bytes from the microcontroller
        Args:
            numbytes (int): Number of bytes to read
        '''
        data = self._read(numbytes, timeout)
        if self.codec:
            data = self.codec.decode(data)
        return data

    def read_chunk(self, timeout=WAIT_FOREVER):
        '''Read a logical chunk of data'''
        data, is_high_priority = self._read_chunk(timeout)
        if self.codec:
            data = self.codec.decode(data)
        return data, is_high_priority

    @abc.abstractmethod
    def shutdown(self):
        '''Shuts down the communication to microcontroller and closes the port'''
        pass

    @abc.abstractmethod
    def _write(self, data):
        pass

    @abc.abstractmethod
    def _read(self, numbytes, timeout=WAIT_FOREVER):
        pass

    @abc.abstractmethod
    def _read_chunk(self, timeout=WAIT_FOREVER):
        pass

    @property
    def transfer_time_offset(self):
        '''The additional time it would take for data transfer'''
        return 0.0


class SimpleCom(BaseCom):
    '''Simple communication class to handle serial port'''

    def __init__(self, portname):
        if not portname:
            raise InvalidPortError('Communication port not specified')

        actualportname = portname.partition(' ')[0]
        try:
            # we cannot operate the serial port in blocking mode, because
            # we have multi-operation commands which require locking to ensure
            # that one operation is complete before starting another

            self._comport = serial.Serial(actualportname, 650195, timeout=1, write_timeout=1)
        except serial.SerialException as excp:
            raise InvalidPortError(f'{excp}')

        self._shuttingdown = False
        logging.debug(f'Opened port {portname}')
        self._receive_buffer = collections.deque(maxlen=RECEIVE_BUFFER_LENGTH)
        self._receive_buffer_len = 0

    def shutdown(self):
        logging.debug('Closing port')
        self._shuttingdown = True
        self._comport.close()
        self._comport = None

    def _write(self, data):
        '''Writes one or more bytes to the microcontroller

        Args:
            data (list[bytes]): list of bytes to send to the microcontroller

        Returns:
            True if it was successful in sending all bytes in the given data

        Raises:
            CommunicationError: If communication to the microcontroller is
                                unsuccessful
            PortClosedError: If attempting to read after port has shut down

        '''
        if self._comport:
            try:
                return self._comport.write(data) == len(data)
            except serial.serialutil.SerialException as excp:
                raise CommunicationError(f'{excp}')
        else:
            raise PortClosedError()

    def _handle_overflow(self):
        '''Handles the receive buffer overflow'''
        # it copies the first and last unfinished packets to the new buffer
        # to prevent any packet corruption in the upper layers and erase the rest
        tmp_buffer = collections.deque(maxlen=RECEIVE_BUFFER_LENGTH)
        self._receive_buffer_len = 0
        left_over_packet = [self._receive_buffer.popleft()
                            for _ in range(self._receive_buffer.index(0) + 1)]
        if left_over_packet:
            tmp_buffer.extend(left_over_packet)
            self._receive_buffer_len += len(left_over_packet)

        self._receive_buffer.reverse()

        rightmost_incomplete_packet = [self._receive_buffer.popleft()
                                       for _ in range(self._receive_buffer.index(0))]
        if rightmost_incomplete_packet:
            tmp_buffer.extend(reversed(rightmost_incomplete_packet))
            self._receive_buffer_len += len(rightmost_incomplete_packet)

        self._receive_buffer = tmp_buffer

    def _read(self, numbytes, timeout=WAIT_FOREVER):
        '''Reads one or more bytes from the microcontroller

        Args:
            numbytes (int): Number of bytes to read
            timeout (int): Timeout in seconds
                           -1 will block until numbytes is received

        Returns:
            list[byte]: list of bytes received from the microcontroller

        '''

        waitedcycles = 1
        while not self._shuttingdown:
            try:
                toreadbytes = max(numbytes - self._receive_buffer_len, self._comport.in_waiting)
                if toreadbytes > 0:
                    res = self._comport.read(toreadbytes)
                    if self._receive_buffer_len + len(res) > RECEIVE_BUFFER_LENGTH:
                        self._handle_overflow()
                    self._receive_buffer.extend(res)
                    self._receive_buffer_len += len(res)
            except Exception as excp:  # pylint: disable=broad-except
                # messing with _comport can cause all sorts of exceptions from pyserial. We'll
                # eat them all here if the cause was us shutting down in the middle of a read.
                if not self._shuttingdown:
                    raise CommunicationError(f'{excp}')
                break
            else:
                if self._receive_buffer_len >= numbytes:
                    result = [self._receive_buffer.popleft() for _ in range(numbytes)]
                    self._receive_buffer_len -= numbytes
                    return bytes(result)
                if timeout != WAIT_FOREVER and waitedcycles >= timeout:
                    raise ReadTimedOutError(numbytes, len(res))

            waitedcycles += 1

        raise PortClosedError()

    def _read_chunk(self, timeout=WAIT_FOREVER):
        raise NotImplementedError


class SimpleDelimitedCom(BaseCom):
    '''Simple communication class to handle serial port'''

    def __init__(self, portname, rxbuffer, delimiter=b'\x00', codec=None):
        if not portname:
            raise InvalidPortError('Communication port not specified')

        self._codec = codec
        actualportname = portname.partition(' ')[0]
        try:
            # we cannot operate the serial port in blocking mode, because
            # we have multi-operation commands which require locking to ensure
            # that one operation is complete before starting another

            self._comport = serial.Serial(actualportname, 650195, timeout=1, write_timeout=1)
        except serial.SerialException as excp:
            raise InvalidPortError(f'{excp}')

        self._shuttingdown = False
        logging.debug(f'Opened port {portname}')
        self._rxbuffer = rxbuffer
        self._delimiter = delimiter
        self._incomplete_packet = b''

    def shutdown(self):
        logging.debug('Closing port')
        self._shuttingdown = True
        self._comport.close()
        self._comport = None

    @property
    def codec(self):
        return self._codec

    def _write(self, data):
        '''Writes one or more bytes to the microcontroller

        Args:
            data (list[bytes]): list of bytes to send to the microcontroller

        Returns:
            True if it was successful in sending all bytes in the given data

        Raises:
            CommunicationError: If communication to the microcontroller is
                                unsuccessful
            PortClosedError: If attempting to read after port has shut down

        '''
        if self._comport:
            try:
                writelen = self._comport.write(data)
                self._comport.flush()
                return writelen == len(data)
            except serial.serialutil.SerialException as excp:
                raise CommunicationError(f'{excp}')
        else:
            raise PortClosedError()

    def _read(self, numbytes, timeout=WAIT_FOREVER):
        '''Reads one or more bytes from the microcontroller

        Args:
            numbytes (int): Number of bytes to read

        '''
        raise NotImplementedError

    def _read_chunk(self, timeout=WAIT_FOREVER):
        '''Reads one chunk from the microcontroller

        Args:
            timeout (int): Timeout in seconds
                           -1 will block until numbytes is received

        Returns:
            bytes: bytes received from the microcontroller
        '''

        waitedcycles = 1
        while not self._shuttingdown:
            if self._comport.in_waiting:
                try:
                    res = self._comport.read(self._comport.in_waiting)
                except Exception as excp:  # pylint: disable=broad-except
                    # messing with _comport can cause all sorts of exceptions from pyserial. We'll
                    # eat them all here if the cause was us shutting down in the middle of a read.
                    if not self._shuttingdown:
                        raise CommunicationError(f'{excp}')
                    break
                else:
                    self._append_data(res)

            if self._rxbuffer:
                return self._rxbuffer.popleft()
            if timeout != WAIT_FOREVER and waitedcycles >= timeout:
                raise ReadTimedOutError(1, 0)

            waitedcycles += 1

        raise PortClosedError()

    def _append_data(self, data):
        chunks = data.split(self._delimiter)
        chunks[0] = self._incomplete_packet + chunks[0]
        self._incomplete_packet = chunks[-1]
        if len(chunks) > 1:
            for chunk in chunks[:-1]:
                # don't interpret extra zeros transmitted at the end as packets
                if not chunk:
                    continue
                self._rxbuffer.append(chunk)


class CCom(BaseCom):
    '''Wrapper for the C com layer'''

    def __init__(self, portname, packet_cb, fault_cb):
        def fault_cb_wrapper():
            self._fault = CommunicationError('Tracker Disconnected')
            self._fault_cb(self._fault)

        def packet_cb_wrapper(packet_data, packet_len):
            self._packets_received += 1
            self._packet_cb(bytes(packet_data[:packet_len]))

        self._fault_cb = fault_cb
        self._packet_cb = packet_cb
        self._fault = None
        self._packets_received = 0

        if not portname:
            raise InvalidPortError('Tracker not found')

        actualportname = portname.partition(' ')[0].encode('utf-8')

        self.fault_cb_wrapper = _ccom.FAULT_CB(fault_cb_wrapper)
        self.packet_cb_wrapper = _ccom.PACKET_CB(packet_cb_wrapper)

        if 'spi' in actualportname.decode('utf-8'):
            params = _ccom.ComParams(type=_ccom.COM_TYPE_SPI)
            params.data.spi.devicePath = actualportname
            params.data.spi.devicePoll_us = (ctypes.c_uint)(1000)
            params.data.spi.spiClock_hz = (ctypes.c_uint)(20000000)
            params.data.spi.chipSelect_pin = (ctypes.c_uint)(24)
        else:
            params = _ccom.ComParams(type=_ccom.COM_TYPE_USB)
            params.data.usb.port_name = actualportname

        if not _ccom.init(ctypes.byref(params), self.packet_cb_wrapper, self.fault_cb_wrapper):
            raise InvalidPortError(f'Unable to open port {portname}')

    def _write(self, data):
        if self._fault is not None:
            raise self._fault  # pylint: disable=raising-bad-type
        return _ccom.write(buffer2ctypes(data), len(data))

    def _read(self, numbytes, timeout=WAIT_FOREVER):
        raise NotImplementedError

    def _read_chunk(self, timeout=WAIT_FOREVER):
        raise NotImplementedError

    def stats(self):
        '''Gets the received / dropped stats'''
        return self._packets_received, _ccom.dropped()

    def get_fault(self):
        '''Gets the current fault if any'''
        return self._fault

    def shutdown(self):
        '''Close the port'''
        _ccom.deinit()


class UdpCom(BaseCom):
    '''Handles UDP communication to the device'''

    def __init__(self, destinationAddress, destport, rxbuffer=None):
        super().__init__()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('127.0.0.1', 0))
        self._destination_address = destinationAddress
        self._destport = destport
        self._rxbuffer = rxbuffer if rxbuffer else collections.deque()
        self._shuttingdown = False

    def shutdown(self):
        self._shuttingdown = True
        # Make sure that last response received before closing the soket
        time.sleep(1.0)
        self._sock.close()

    def _write(self, data):
        try:
            self._sock.sendto(bytearray(data), (self._destination_address, self._destport))
        except OSError as excp:
            if not self._shuttingdown:
                raise CommunicationError(f'{excp}')
            raise PortClosedError

    def _read(self, numbytes=1, timeout=WAIT_FOREVER):
        raise NotImplementedError

    def _read_chunk(self, timeout=WAIT_FOREVER):
        self._sock.settimeout(self.transfer_time_offset if timeout == WAIT_FOREVER else timeout)
        while True:
            try:
                data, _addr = self._sock.recvfrom(1024)
                self._rxbuffer.append(data)
                break
            except socket.timeout:
                if timeout == WAIT_FOREVER:
                    continue
                raise PortClosedError
            except OSError:
                raise PortClosedError

        return self._rxbuffer.popleft()

    @property
    def transfer_time_offset(self):
        return 4.0
