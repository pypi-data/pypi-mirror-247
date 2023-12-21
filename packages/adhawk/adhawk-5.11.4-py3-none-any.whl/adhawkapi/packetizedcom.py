'''This module provides the tools and routines for packetized communication
with Adhawk's embedded devices.'''

import ctypes
import logging
import adhawktools as tools
from . import com, internal
from .capi.py import librequest as _request
from .capi.py.util import buffer2ctypes
from .error import CommunicationError
from .packet import PacketV3Factory
from .publicapi import AckCodes


MESSENGER_FAULT_EVENTTYPE = 0xdeadbeef


class PacketizedCom(tools.MultiNotification):
    '''Packetized communication over serial port'''

    def __init__(self, portname, fault_callback=None):
        super().__init__()
        self._streamstarted = False
        self._packet_factory = PacketV3Factory

        logging.info('Using C Com layer')
        self._basecom = com.CCom(portname, self._handle_packet, self._handle_fault)
        _request.init()

        if fault_callback:
            self.add_fault_callback(fault_callback)

        logging.debug(f'Opened packetized port {portname}')

    def stats(self):
        '''Returns the number of received / dropped packets'''
        if getattr(self, '_basecom', None) is not None:
            return self._basecom.stats()

        return 0, 0

    def add_fault_callback(self, func):
        '''Add callback for critical communication related failures'''
        self.add_callback(func, MESSENGER_FAULT_EVENTTYPE, mask=0xffffffff)

    def shutdown(self):
        '''Shutsdown the communication to microcontroller and closes the port'''
        logging.debug('Shutting down packetized port')

        _request.deinit()

        if getattr(self, '_basecom', None) is not None:
            self._basecom.shutdown()
            self._basecom = None

    def make_packet(self, *args, **kwargs):
        '''Create a this instance's custom packet using the information provided'''
        return self._packet_factory.construct(*args, **kwargs)

    def request(self, request_pkt, expecting_ack=True, timeout=1):
        '''Sends a request to microcontroller and waits for the response

        Args:
            request_pkt (adhawkapi.Packet): Packet containing the request
            expecting_ack (bool): Is a response (ack) expected or not?
            timeout (int): Timeout in seconds

        Returns:
            adhawkapi.Packet: the packet received in response to our request

        Raises:
            CommunicationError: If communication to the microcontroller is
                                unsuccessful

        '''
        if not self._basecom:
            raise com.PortClosedError()

        if self._basecom.get_fault():
            raise self._basecom.get_fault()

        self._packet_factory.validate(request_pkt)

        # print(f'Request: {request_pkt.packet_data}')

        if not expecting_ack:
            # Not expecting an ACK, skip the request logic and just write the data to the device
            self._basecom.write(request_pkt.packet_data)
            return None

        request_type = request_pkt.packet_data[0]
        response_data_p = ctypes.c_void_p()
        response_len = ctypes.c_uint(0)

        # Blocks until a response is received or a timeout occurs
        request_result = _request.send_request(buffer2ctypes(request_pkt.packet_data),
                                               len(request_pkt.packet_data),
                                               ctypes.byref(response_data_p), ctypes.byref(response_len),
                                               int(timeout * 1000))
        if request_result == AckCodes.REQUEST_TIMEOUT:
            raise CommunicationError('Request timeout')
        if request_result == AckCodes.COMMUNICATION_ERROR:
            raise CommunicationError('Failed to send request')

        response = bytes([request_type])
        if request_type != internal.PacketType.V2:
            response += bytes([request_result])

        if response_len.value > 0:
            response_data = ctypes.cast(response_data_p, ctypes.POINTER(ctypes.c_ubyte * response_len.value)).contents
            response += bytes(response_data)
        # print(f'Response: {response}')
        pkt = self._packet_factory.construct_from_raw(response)
        return pkt

    def start_stream(self):
        '''Starts sending stream packets to upper layers
        This is used to prevent flooding when tapping into an ongoing stream'''
        self._streamstarted = True

    def stop_stream(self):
        '''Stops sending stream packets to upper layers
        This prevents flooding in case the stream is left uninterrupted'''
        self._streamstarted = False

    def _handle_packet(self, packet_data):
        '''Helper routine invoked by the messenger to handle received packets'''

        try:
            pkt = self._packet_factory.construct_from_raw(packet_data)
        except NotImplementedError:
            return

        if pkt.metadata.stream:
            # if pkt.metadata.high_priority:
            #     print('high priority stream: ', *[hex(itr) for itr in list(pkt.packet_data)])
            # else:
            #     print('stream: ', *[hex(itr) for itr in list(pkt.packet_data)])
            if self._streamstarted:
                enc_app_id = ord(pkt.header) | pkt.metadata.error << 8
                self._notify_callbacks(enc_app_id, pkt)
        else:
            _request.handle_response(buffer2ctypes(packet_data), len(packet_data))

    def _handle_fault(self, excp):
        '''Helper routine invoked by messenger to handle exceptions'''
        self._notify_callbacks(MESSENGER_FAULT_EVENTTYPE, excp)
