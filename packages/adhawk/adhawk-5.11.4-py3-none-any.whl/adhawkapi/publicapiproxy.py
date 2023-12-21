'''This module implements a thin API to connect embedded eye tracker to backend output'''

import logging
import struct

from . import defaults
from . import internal
from . import register_api
from .base import RequestTimedOutError
from .packet import PublicPacketFactory
from .publicapi import (AckCodes, PacketType, PropertyType, SystemControlType,
                        errormsg, check_result)
from .version import SemanticVersion


class PublicApiProxy(register_api.RegisterApi):
    '''This class implements a thin API to connect to the embedded eye tracker

    Since the embedded eye tracker has full support for public API, this class
    simply proxies the requests/responses from to clients to embedded et and
    vice versa.

    Although PublicApi does not come from BaseApi, we inherit from BaseApi,
    which gives us the port management already in BaseApi.

    '''

    # pylint: disable=too-many-public-methods
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dest_id = self.firmware_info.num_trackers

    def register_data_streams(self, report_stream_cb):
        '''Register callback for data streams from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_stream_cb(pkt.packet_data),
                               0, mask=0xe0, key=report_stream_cb)

    def register_raw_streams(self, report_stream_cb):
        '''Register callback for raw data streams from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_stream_cb(pkt.packet_data),
                               internal.PacketType.RAW_PULSE, key=report_stream_cb)
        self._com.add_callback(lambda pkt: report_stream_cb(pkt.packet_data),
                               internal.PacketType.RAW_PULSE_V2, key=report_stream_cb)

    def register_system_info(self, report_sysinfo_cb):
        '''Register callback for system info msgs from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_sysinfo_cb(pkt.packet_data),
                               internal.PacketType.EMBEDDED_INFO, key=report_sysinfo_cb)

    def register_tracker_status(self, report_tracker_status_cb):
        '''Register callback for tracker status stream from embedded eye tracker'''
        # If you call `register_data_streams`, you don't need to call this
        self._com.add_callback(lambda pkt: report_tracker_status_cb(pkt.packet_data),
                               PacketType.TRACKER_STATUS, key=report_tracker_status_cb)

    def register_iris_data_streams(self, report_tracker_status_cb):
        '''Register callback for tracker iris image stream from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_tracker_status_cb(pkt.packet_data),
                               PacketType.IRIS_IMAGE_DATA_STREAM, key=report_tracker_status_cb)

    def register_analytics(self, report_analytics_cb):
        '''Register callback for analytics streams from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_analytics_cb(pkt.payload),
                               internal.PacketType.ANALYTICS, key=report_analytics_cb)

    def register_debug_annotations(self, report_annotation_cb):
        '''Register callback for debug annotation streams from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_annotation_cb(pkt.payload),
                               internal.PacketType.DEBUG_ANNOTATION, key=report_annotation_cb)

    def register_debug_msg(self, report_debug_msg_cb):
        '''Register callback for debug messages streams from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_debug_msg_cb(pkt.payload),
                               internal.PacketType.DEBUG_MSG, key=report_debug_msg_cb)

    def register_config_dump(self, report_config_dump_cb):
        '''Register callback for the config dump stream from embedded eye tracker'''
        self._com.add_callback(lambda pkt: report_config_dump_cb(pkt.payload),
                               PacketType.CONFIG_DUMP, key=report_config_dump_cb)

    def request_pub(self, pkttype, payload):
        '''Send a request to embedded eye tracker'''
        # logging.debug(f'forwarding request {repr(pkttype)} {payload}')
        pkt = PublicPacketFactory.construct(pkttype, payload)
        response = self._com.request(pkt, expecting_ack=True, timeout=5)
        if not response:
            raise RequestTimedOutError(f'Public API request {repr(pkttype)} timed out')
        # logging.debug(f'got response {response.packet_data}')
        return response

    def start(self):
        '''Start eye tracking and data streams'''
        self._com.start_stream()

    def trigger_autotune(self, args=None):
        '''Trigger autotune with no initial conditions or with a reference
           gaze vector with [x, y, z] float components'''
        res = self.request_pub(PacketType.TRIGGER_AUTOTUNE, args)
        return res.packet_data[1]

    def trigger_iris_capture(self):
        '''Triggers an iris capture operation in the embedded et'''
        res = self.request_pub(PacketType.IRIS_TRIGGER_CAPTURE, None)
        return res.packet_data[1]

    def trigger_config_dump(self):
        '''Triggers a config dump in the embedded et'''
        res = self.request_pub(PacketType.TRIGGER_CONFIG_DUMP, None)
        return res.packet_data[1]

    @staticmethod
    def _chunks(data):
        '''Generator that breaks the data into chunks '''

        size = len(data)
        offset = 0
        chunk_len = defaults.BLOB_CHUNK_LEN
        while (offset + chunk_len) <= size:
            yield offset, data[offset:offset + chunk_len]
            offset = offset + chunk_len
        yield offset, data[offset:]

    def write_blob(self, blob_type, blob_data):
        '''Write the specified blob to the embedded et in multiple chunks'''
        blob_data = bytes(blob_data)
        result = self.request_pub(PacketType.BLOB_SIZE, struct.pack('<BH', blob_type, len(blob_data)))

        if result.packet_data[1] != 0x00:
            logging.debug(f'Write Blob Size NACK: {result.packet_data[1]}')
            return result.packet_data[1]

        for offset, chunk in self._chunks(blob_data):
            result = self.request_pub(PacketType.BLOB_DATA, struct.pack('<BH', blob_type, offset) + chunk)

            if result.packet_data[1] != 0x00:
                logging.debug(f'Write Blob Data NACK: {result.packet_data[1]}')
                return result.packet_data[1]

        return 0

    def read_blob(self, blob_type):
        '''Reads the specified blob in multiple chunks from embedded et'''
        result = self.request_pub(PacketType.BLOB_SIZE, struct.pack('<B', blob_type))
        err, size = result.unpack_payload('<BH')

        if err != 0x00:
            logging.debug(f'Read Blob Size NACK: {err}')
            return err, None

        data = []
        offset = 0
        while offset <= size:
            result = self.request_pub(PacketType.BLOB_DATA, struct.pack('<BH', blob_type, offset))

            if result.packet_data[1] != 0x00:
                logging.debug(f'Read Blob Data NACK: {result.packet_data[1]}')
                return result.packet_data[1]

            data[offset:] = result.packet_data[2:]
            offset = offset + defaults.BLOB_CHUNK_LEN
        return 0, data

    def read_fault_info(self):
        '''Reads the fault debugging info from the device'''
        result = self.request_pub(internal.PacketType.FAULT_INFO, 0)
        ack_code = result.packet_data[1]
        data = result.packet_data[2:]
        return ack_code, data

    def get_property(self, property_type, data):
        '''Get the specified property'''
        logging.debug(f'get_property({property_type})')
        result = self.request_pub(PacketType.PROPERTY_GET, struct.pack('<B', property_type) + data)
        check_result(result.packet_data[1], f'Failed to get property {property_type}')
        return result.packet_data[2:]

    def set_property(self, property_type, data):
        '''Set the specified property'''
        logging.debug(f'set_property({property_type})')
        result = self.request_pub(PacketType.PROPERTY_SET, struct.pack('<B', property_type) + data)
        check_result(result.packet_data[1], f'Failed to set property {property_type}')

    def get_stream_control(self, stream_bit):
        '''Gets the stream rate specified for stream_bit'''
        logging.debug(f'get_stream_control({hex(stream_bit)})')
        prop = self.get_property(PropertyType.STREAM_CONTROL, struct.pack('<I', stream_bit))
        return struct.unpack_from('<f', prop, 1)[0]

    def set_stream_control(self, stream_bits, rate):
        '''Sets the streams specified by stream_bits to the specified rate'''
        logging.debug(f'set_stream_control({hex(stream_bits)}, {rate})')
        self.set_property(PropertyType.STREAM_CONTROL, struct.pack('<If', stream_bits, rate))

    def set_event_control(self, event_bits, enable):
        '''Controls the events specified by event_bits'''
        logging.debug(f'set_event_control({hex(event_bits)}, {enable})')
        self.set_property(PropertyType.EVENT_CONTROL, struct.pack('<IB', event_bits, enable))

    def enable_embedded_et(self):
        '''Enables embedded ET'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 62, 0)) < 0:
            result = self.request_pub(internal.PacketType.CONTROL,
                                      struct.pack('<B', internal.ControlType.START))
        else:
            result = self.request_pub(PacketType.SYSTEM_CONTROL,
                                      struct.pack('<BB', SystemControlType.TRACKING, 1))
        check_result(result.packet_data[1], 'Failed to enable embedded ET')

    def disable_embedded_et(self):
        '''Disables embedded ET'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 62, 0)) < 0:
            result = self.request_pub(internal.PacketType.CONTROL,
                                      struct.pack('<B', internal.ControlType.STOP))
        else:
            result = self.request_pub(PacketType.SYSTEM_CONTROL,
                                      struct.pack('<BB', SystemControlType.TRACKING, 0))
        check_result(result.packet_data[1], 'Failed to disable embedded ET')

    def enable_laser_safety_algorithm(self):
        '''Enables laser safety algorithm'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 31, 0)) < 0:
            logging.warning('This tracker does not support laser safety enable')
            return

        result = self.request_pub(internal.PacketType.CONTROL,
                                  struct.pack('<BB', internal.ControlType.LASER_SAFETY_CONTROL, 1))
        check_result(result.packet_data[1], 'Failed to enable laser safety algorithm')

    def disable_laser_safety_algorithm(self):
        '''Disables laser safety algorithm'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 31, 0)) < 0:
            logging.warning('This tracker does not support laser safety disable')
            return

        result = self.request_pub(internal.PacketType.CONTROL,
                                  struct.pack('<BB', internal.ControlType.LASER_SAFETY_CONTROL, 0))
        check_result(result.packet_data[1], 'Failed to disable laser safety algorithm')

    def set_internal_stream_control(self, log_mode):
        '''Enable or disable internal streams'''
        logging.debug(f'set_internal_stream_control({log_mode})')
        result = self.request_pub(internal.PacketType.CONTROL,
                                  struct.pack('<BB', internal.ControlType.LOG_MODE, log_mode))
        check_result(result.packet_data[1], 'Failed to enable internal streams')

    def get_tracker_status(self):
        '''Get the tracker status/state'''
        logging.debug('get_tracker_status')
        result = self.request_pub(PacketType.TRACKER_STATE, None)
        if result.packet_data[1] == AckCodes.SUCCESS:
            logging.debug('Trackers Ready')
        elif result.packet_data[1] == AckCodes.FAILURE:
            logging.error('Tracker Fault')
        else:
            logging.debug(errormsg(result.packet_data[1]))

        return result.packet_data[1]
