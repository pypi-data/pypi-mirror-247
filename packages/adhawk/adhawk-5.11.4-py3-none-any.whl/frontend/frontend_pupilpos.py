''' pupil position stream for AdHawk Backend

Requirements:
- Windows 10
- Python 3.6+

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend.py frontend_pupilpos
- All the data is output to stdout in a csv format

'''

import csv
import sys
import time

import adhawkapi.frontend


class FrontendData:
    ''' Handle the data aggregation from backend '''
    bufduration = 0.1  # glint buffer duration in seconds

    def __init__(self):
        self._csvwriter = csv.writer(sys.stdout, delimiter=',')
        self._csvwriter.writerow(['timestamp', 'xL', 'yL', 'zL', 'xR', 'yR', 'zR'])

        self._frontend_handlers = {}
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.PUPIL_POSITION, self._handle_pupilpos_data)
        self._api.start(connect_cb=self._handle_connect)

    def _handle_connect(self, error):
        if not error:
            streams = [adhawkapi.PacketType.PUPIL_POSITION]
            for stream in streams:
                self._api.set_stream_control(stream, 120, callback=(lambda *args: None))

    def _handle_pupilpos_data(self, timestamp, xright, yright, zright, xleft, yleft, zleft):
        self._csvwriter.writerow([timestamp, xleft, yleft, zleft, xright, yright, zright])

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
