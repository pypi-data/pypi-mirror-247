'''Contains handlers for frontend requests and responses'''

import collections
import logging
import threading

from . import backendcom
from .decoders import decode
from .encoders import encode


try:
    from .. import internal
except ImportError:
    internal = None
from .. import publicapi


class PacketHandler:
    '''Class that wraps the comm layer and handles encoding and decoding requests and responses
    '''

    def __init__(self, eye_mask):
        self._logger = logging.getLogger(__name__)
        self._pending_requests = collections.defaultdict(collections.deque)
        self._registered_handlers = collections.defaultdict(list)
        self._rx_cv = threading.Condition()
        self._responses = collections.deque()
        self._com = None
        self._eye_mask = eye_mask

    def set_eye_mask(self, eye_mask):
        '''Set the current eye mask'''
        self._eye_mask = eye_mask

    def start(self, connect_cb=None, disconnect_cb=None):
        '''Start communication with AdHawk service'''

        self._com = backendcom.BackendStream(self._handle_packet)

        # Register connection handlers here since they are only
        # sent and received by the comm layer. The client of the API
        # shouldn't have to register for it
        connect_cb = connect_cb if connect_cb else (lambda *args: None)
        disconnect_cb = disconnect_cb if disconnect_cb else (lambda *args: None)

        self._registered_handlers[publicapi.PacketType.UDP_CONN].append(connect_cb)
        self._registered_handlers[publicapi.PacketType.END_UDP_CONN].append(disconnect_cb)

        self._com = backendcom.BackendStream(self._handle_packet)
        self._com.start()

    def shutdown(self):
        '''Stop all data streams and shutdown comms'''
        self._com.shutdown()

    def request(self, packet_type, *args, callback=None, **kwargs):
        '''Send a request to backend given a packet type and the arguments'''

        self._logger.debug(f'[tx] {repr(packet_type)}: {args}')
        # setup sync or async callbacks
        if callback is None:
            self._pending_requests[packet_type].append(self._blocking_handler)
        else:
            self._pending_requests[packet_type].append(callback)

        # encode and send the message
        message = encode(packet_type, *args, *kwargs)
        self._com.send(message)

        # wait on response if required
        if callback:
            return None
        with self._rx_cv:
            self._logger.debug('Waiting for response...')
            self._rx_cv.wait(publicapi.REQUEST_TIMEOUT + 1)
            try:
                response = self._responses.pop()
                if response[0] != publicapi.AckCodes.SUCCESS:
                    raise publicapi.APIRequestError(response[0])
                return response
            except IndexError:
                raise publicapi.APIRequestError(publicapi.AckCodes.REQUEST_TIMEOUT)

    def register_stream_handler(self, packet_type, handler=None):
        '''Add a listener for a particular packet type'''
        if not packet_type.is_stream():
            # Ensure we only register or unregister stream packets
            # All other packets are automatically registered through
            # the api callback parameter
            return

        if handler:
            self._registered_handlers[packet_type].append(handler)
        else:
            if packet_type in self._registered_handlers:
                self._registered_handlers.pop(packet_type)

    def _blocking_handler(self, *args):
        '''Provides a handler that wakes up all threads waiting for a specific response'''
        with self._rx_cv:
            self._responses.append(args)
            self._rx_cv.notify()

    def _handle_packet(self, packet_type_int, data):
        '''Determines the packet type and decodes it'''
        try:
            try:
                packet_type = publicapi.PacketType(packet_type_int)
            except ValueError:
                if internal is None:
                    raise
                packet_type = internal.PacketType(packet_type_int)
        except ValueError:
            self._logger.warning(f'Unrecognized packet: {hex(packet_type_int)}')
            return

        decoded = decode(packet_type, data, self._eye_mask)
        if decoded is None:
            return

        # handle udp comm packets and any registered stream handlers first
        handlers = self._registered_handlers[packet_type]
        if handlers:
            for handler in handlers:
                handler(*decoded)
            return

        if not packet_type.is_stream():
            # Checking pending requests
            self._logger.debug(f'[rx] {repr(packet_type)} {decoded}')
            try:
                # responses from backend are for the most part strictly ordered
                # there are a few packets types that are handled prior to streaming
                # therefore we key on the packet type and then pop the requests
                # off the queue
                handler = self._pending_requests[packet_type].popleft()
            except IndexError:
                self._logger.warning(f'Received unexpected packet: {repr(packet_type)}')
            else:
                handler(*decoded)
