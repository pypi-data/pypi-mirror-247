''' Pupil diameter stream for AdHawk Backend

Requirements:
- Windows 10
- Python 3.6+

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend_pupilsize.py
- All the data is output to stdout in a csv format

'''

import sys
import time
import csv

import adhawkapi
import adhawkapi.frontend


class FrontendData:
    ''' Handle the data aggregation from backend '''

    def __init__(self):
        self._csvwriter = csv.writer(sys.stdout, delimiter=',')
        self._csvwriter.writerow(['timestamp', 'right pupil diameter (mm)', 'left pupil diameter (mm)'])

        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.PUPIL_DIAMETER, self._handle_pupilsize_data)
        self._api.start(connect_cb=self._handle_connect)

    def _handle_pupilsize_data(self, timestamp, rightpupil, leftpupil):
        self._csvwriter.writerow([timestamp, rightpupil, leftpupil])

    def _handle_connect(self, error):
        if not error:
            streams = [
                adhawkapi.PacketType.PUPIL_DIAMETER,
            ]
            for stream in streams:
                self._api.set_stream_control(stream, 120, callback=(lambda *args: None))

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()


def main():
    ''' App entrypoint '''
    frontend = FrontendData()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()
