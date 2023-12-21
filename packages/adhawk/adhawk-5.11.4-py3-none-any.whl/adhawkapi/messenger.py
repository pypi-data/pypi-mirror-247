'''Reads data, inserts into message queue, and dispatches data to registered listeners'''

import logging
import sys
import threading
import queue
import adhawktools.queue
from .com import (
    PortClosedError,
    RecoverableCommunicationError,
    CommunicationError)


class Messenger:
    """Implements a poller+dispatcher system used by PacketizedCom class

    Description:

    self._read_func - The routine invoked to collect data
    self._dispatch_func - The routine invoked to handle data that was collected
    self._stopthread - Flag that indicates whether or not the messenger should keep on reading and
                       dispatching data to observers
    self._msgq - Queue into which the producer pushes read data; the consumer then pops data from
                  the queue and distributes it to registered observers
    self._readthread - Thread that performs the reading of data (producer)
    self._dispatchthread - Thread that performs the distributing of data to registered observers
                           (consumer)

    """

    def __init__(self, read_func, dispatch_func, fault_func):
        self._read_func = read_func
        self._dispatch_func = dispatch_func
        self._fault_func = fault_func
        # number of consecutive recoverable errors
        self._ncont_recoverable_errors = 0
        self._stopthread = False
        self._received = 0
        self._dropped = 0
        self._high_prio_msgq = adhawktools.queue.BoundedQueue()
        self._low_prio_msgq = adhawktools.queue.BoundedQueue(maxsize=25)
        self._readthread = threading.Thread(target=self._read_data, name='AdhawkapiRead')
        self._readthread.start()
        self._dispatchthreadlow = threading.Thread(target=self._distribute_data,
                                                   args=[self._low_prio_msgq],
                                                   name='AdhawkapiDispatchLowPrio')
        self._dispatchthreadlow.start()
        self._dispatchthreadhigh = threading.Thread(target=self._distribute_data,
                                                    args=[self._high_prio_msgq],
                                                    name='AdhawkapiDispatchHighPrio')
        self._dispatchthreadhigh.start()

    def stats(self):
        ''' Returns received / dropped packet stats'''
        return self._received, self._dropped

    def stop_reading(self):
        """Stops messenger from reading and distributing data"""
        logging.debug('Stopping Messenger')
        self._stopthread = True
        self._high_prio_msgq.put(None)
        self._low_prio_msgq.put(None)
        if threading.current_thread() is not self._dispatchthreadlow:
            self._dispatchthreadlow.join()
        if threading.current_thread() is not self._dispatchthreadhigh:
            self._dispatchthreadhigh.join()

    def _read_data(self):
        while not self._stopthread:
            try:
                data_packet, is_high_priority = self._read_func()  # read one full packet of data
                self._received += 1
            except PortClosedError:
                # the port has been closed, so we need to terminate the loop
                break
            except RecoverableCommunicationError as excp:
                logging.warning(f'{excp}')
                self._ncont_recoverable_errors += 1
            except Exception as excp:  # pylint: disable=broad-except
                self._high_prio_msgq.put_nowait(excp)
                break  # terminate the thread
            else:
                try:
                    if is_high_priority:
                        self._high_prio_msgq.put_nowait(data_packet)
                    else:
                        self._low_prio_msgq.put_nowait(data_packet)
                except queue.Full:
                    self._dropped += 1
                    pass

        logging.debug('Messenger\'s read thread stopped')

    def _distribute_data(self, dist_queue):
        while True:
            data_packet = dist_queue.get()
            exception = None
            if data_packet is None:
                # None in the queue is the signal to exit
                break
            if isinstance(data_packet, Exception):
                logging.info('Got exception in Messenger dispatch: %s', data_packet)
                self._fault_func(data_packet)
                break  # terminate the thread
            try:
                self._dispatch_func(data_packet)
            except RecoverableCommunicationError as excp:
                logging.warning(f'{excp}')
                self._ncont_recoverable_errors += 1
            except Exception as excp:  # pylint: disable=broad-except
                if not getattr(sys, 'frozen', False):
                    logging.exception('Got exception in Messenger dispatch')
                exception = excp
            else:
                self._ncont_recoverable_errors = 0

            if self._ncont_recoverable_errors >= 10:
                exception = CommunicationError('Too many consecutive bad packets')

            if exception is not None:
                logging.info('Got exception in Messenger dispatch: %s', exception)
                self._fault_func(exception)
                break  # terminate the thread

        logging.debug('Messenger\'s distribute thread stopped')
