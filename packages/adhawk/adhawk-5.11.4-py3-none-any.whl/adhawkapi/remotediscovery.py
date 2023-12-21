'''This module provides the scanning of our daydream devices based on UDP Multicast packets.'''

import logging
import socket
import time
import threading
import collections

UDP_DISCOVERY_PORT = 11001
UDP_MULTICAST_GROUP = '239.0.0.222'


class RemoteEyetrackerAdvertise:
    '''Generates multicast packets for eye tracker discovery'''

    __instance = None

    def __init__(self):
        if RemoteEyetrackerAdvertise.__instance is not None:
            raise Exception("This class is a singleton!")
        RemoteEyetrackerAdvertise.__instance = self

        self._opts = {}
        hostname = socket.gethostname()
        ipaddr = socket.gethostbyname(hostname)
        self.add_option('Serial', hostname)
        self.add_option('IP', ipaddr)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._shouldstop = False
        self._thread = threading.Thread(target=self._handle_advertise, name='RemoteAdvertise')
        self._thread.start()

    @classmethod
    def get_instance(cls):
        '''Returns the singleton instance and create one if not initialized'''
        if cls.__instance is None:
            cls()
        return cls.__instance

    def shutdown(self):
        '''set the flag that stops our thread'''
        self._shouldstop = True
        self._thread.join()  # max 1s delay

    def add_option(self, opt, val):
        '''Adds additional capabilities to the advertised message'''
        self._opts[opt] = val

    def _build_msg(self):
        tokens = ['UDP'] + [f'{key}:{val}' for key, val in self._opts.items()]
        return ' '.join(tokens)

    def _handle_advertise(self):
        while not self._shouldstop:
            msg = self._build_msg().encode()
            try:
                self._sock.sendto(bytearray(msg), (UDP_MULTICAST_GROUP, UDP_DISCOVERY_PORT))
            except OSError:
                break
            time.sleep(1)

        self._sock.close()


class RemoteEyetrackerDiscovery:
    '''Handles multicast packets for eye tracker discovery'''

    __instance = None
    DeviceInfo = collections.namedtuple('DeviceInfo', 'type, name, opts, last_seen_time')

    def __init__(self):
        self._is_running = True
        if RemoteEyetrackerDiscovery.__instance is not None:
            raise Exception("This class is a singleton!")
        RemoteEyetrackerDiscovery.__instance = self
        self._device_list = {}
        self._device_list_detailed = {}
        try:
            self._discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                              socket.inet_aton(UDP_MULTICAST_GROUP) + socket.inet_aton('0.0.0.0'))
            self._discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            self._discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._discovery_socket.settimeout(2)
            self._discovery_socket.bind(('', UDP_DISCOVERY_PORT))
        except OSError as excp:
            logging.error(f'Unable to run remote tracker discovery: {excp}')
            return
        self._scanner_thread = threading.Thread(target=self._handle_add_devices, name='RemoteDiscovery')
        self._scanner_thread.start()

    @classmethod
    def get_instance(cls):
        '''Returns the singleton instance and create one if not initialized'''
        if cls.__instance is None:
            cls()
        return cls.__instance

    def shutdown(self):
        '''set the flag that stops our thread'''
        self._is_running = False

    @property
    def incoming_ports(self):
        '''Returns list of discovered ports capable of streaming data to us'''
        return [dev.name for dev in self._device_list.values()]

    @property
    def outgoing_ports(self):
        '''Returns list of discovered ports capable of receiving streaming data'''
        return [dev.name for dev in self._device_list.values() if 'INPORT' in dev.opts]

    def get_device_info(self, portname):
        '''get device IP and port based on given key'''
        return self._device_list[portname]

    def _delete_stale_devices(self):
        '''check and delete any device that not discovered for more than 3 seconds'''
        to_delete_keys = {}
        for key, value in self._device_list_detailed.items():
            last_seen = value.last_seen_time
            if float(time.time() - int(last_seen)) > 3.0:
                to_delete_keys[key] = key
        for key, value in to_delete_keys.items():
            del self._device_list[key]
            del self._device_list_detailed[key]

    def _handle_add_devices(self):
        '''listen on multicast port and add new devices to the list'''
        while self._is_running is True:
            self._delete_stale_devices()
            try:
                data = self._discovery_socket.recv(1024).decode('ascii')
            except socket.timeout:
                pass
            else:
                # Broadcast packet format : #Packet_Type Serial:#serial_number IP:#device_ip_address PORT:#portnumber
                # parameters are blank space separated
                comtype, opts_str = data.split(maxsplit=1)

                opts = {}
                for opt in opts_str.split():
                    key, val = opt.split(':')
                    opts[key] = val

                if 'IP' not in opts or not opts['IP']:
                    # Bad discovery packet, ignore it
                    continue

                serial = opts.get('Serial', 'N/A')
                iplo = opts['IP'].rsplit('.', maxsplit=1)[1]
                name = f'{comtype} {serial} (.{iplo})'

                self._device_list[name] = self.DeviceInfo(comtype, name, opts, time.time())

        # Close our socket only when the thread is existing
        self._discovery_socket.close()
