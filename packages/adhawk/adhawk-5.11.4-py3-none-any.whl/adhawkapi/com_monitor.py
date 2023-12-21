'''This module monitors the com layer's performance'''

import time
import threading
import logging
import struct

from . import error
from . import publicapiproxy
from . import registers
from . import StreamControlBit


class ComMonitor():
    '''This class monitors the com layer's performance'''

    def __init__(self, kit, com, debug_stats):
        self._com = com
        self._last_received = 0
        self._last_dropped = 0
        self._embedded_tx_count = 0
        self._embedded_dropped_count = 0
        self._stopthread = False

        if debug_stats:
            try:
                port = kit.get_endpoints(registers.SpecCapability.EMBEDDED_ET)[0][0]
            except IndexError:
                raise error.Error('Device capable of embedded eye tracking not found')
            self._pubapi = publicapiproxy.PublicApiProxy(port)
            self._pubapi.register_system_info(self._handle_embedded_info)
            self._pubapi.set_stream_control(StreamControlBit.EMBEDDED_INFO, 10)

            self._thread = threading.Thread(target=self._main_loop, name='ComMonitor')
            self._thread.start()

    def shutdown(self):
        '''Stops the module'''
        if getattr(self, '_thread', None) is not None:
            self._stopthread = True
            self._thread.join()

        total_received, total_dropped = self._com.stats()
        total_packets = total_dropped + total_received
        if total_packets:
            logging.debug(f'Host COM Stats: Packets Received: {total_received}, Packets Dropped: {total_dropped} '
                          f'({(total_dropped / (total_packets) * 100):.1f}%)')

    def _handle_embedded_info(self, data):
        # pylint: disable=unused-variable
        if data[1] == 2:
            timestamp, rx_count, tx_count, mainloop_tx_count = struct.unpack_from('<f3H', data, 2)
            self._embedded_tx_count += tx_count
        if data[1] == 3:
            timestamp, max_stack_usage, mainloop_work, interrupt_work, dropped_packets_queue_full, \
                dropped_packets_queue_busy, dropped_packets_spi, dropped_packets_oom, dropped_packets_length = \
                struct.unpack_from('<f3I5B', data, 2)
            self._embedded_dropped_count += dropped_packets_queue_full
            self._embedded_dropped_count += dropped_packets_queue_busy
            self._embedded_dropped_count += dropped_packets_spi
            self._embedded_dropped_count += dropped_packets_oom
            self._embedded_dropped_count += dropped_packets_length

    def _main_loop(self):
        while not self._stopthread:
            time.sleep(1)

            total_received, total_dropped = self._com.stats()
            received = total_received - self._last_received
            dropped = total_dropped - self._last_dropped
            self._last_received = total_received
            self._last_dropped = total_dropped

            # The sent / received numbers won't match exactly, because the windows they are measured
            # over differ slightly, but if they aren't close it's a red flag
            logging.debug(f'Embedded Sent: {self._embedded_tx_count}, Host Received: {received}, '
                          f'Embedded Dropped: {self._embedded_dropped_count}, Host Dropped: {dropped}')
            self._embedded_tx_count = 0
            self._embedded_dropped_count = 0
