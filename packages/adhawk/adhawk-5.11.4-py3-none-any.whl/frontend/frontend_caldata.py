''' Calibrated data streamer for AdHawk Backend

Requirements:
- Windows 10
- Python 3.6+

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend_caldata.py
- All the data is output to stdout in a csv format

'''

import csv
import struct
import sys
import time

import adhawkapi.frontend.backendcom as com


class FrontendData:
    ''' Handle the data aggregation from backend '''
    bufduration = 0.1  # glint buffer duration in seconds

    def __init__(self):
        self._csvwriter = csv.writer(sys.stdout, delimiter=',')
        self._csvwriter.writerow(['timestamp', 'gaze_x', 'gaze_y', 'gaze_z'])

        self._frontend_handlers = {}
        self._frontend_handlers[0x01] = lambda data: self._handle_cal_data(*struct.unpack('<fff', data))
        self._frontend_handlers[0x03] = lambda data: self._handle_ts_cal_data(*struct.unpack('<ffff', data))
        self._frontend_handlers[0xc0] = lambda data: self._handle_stream_enable()
        self._port = com.BackendStream(self._handle_data)
        self._port.start()

    def _handle_data(self, header, data):
        if header in self._frontend_handlers:
            self._frontend_handlers[header](data)

    def _handle_cal_data(self, xpos, ypos, zpos):
        self._csvwriter.writerow([time.perf_counter(), xpos, ypos, zpos])

    def _handle_ts_cal_data(self, timestamp, xpos, ypos, zpos):
        self._csvwriter.writerow([timestamp, xpos, ypos, zpos])

    def _handle_stream_enable(self):
        self._port.send(struct.pack('<BI', 0x8a, 0x1))

    def shutdown(self):
        ''' Shutdown the port '''
        self._port.shutdown()


def main():
    ''' App entrypoint '''
    frontend = FrontendData()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()
