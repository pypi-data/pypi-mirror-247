''' Customer stream data viewer for AdHawk Backend

Requirements:
- Windows 10
- Python 3.6+

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend_diag.py
- The customer data is print out in the console

'''

import time
import struct
import adhawkapi.frontend.backendcom as com


class FrontendData:
    ''' Handle the data aggregation from backend '''

    def __init__(self):
        self._customer_data = []
        self._frontend_handlers = {}
        self._frontend_handlers[0x15] = self._handle_customer_data
        self._frontend_handlers[0xc0] = lambda data: self._handle_stream_enable()
        self._port = com.BackendStream(self._handle_data)
        self._port.start()

    def _handle_data(self, header, data):
        if header in self._frontend_handlers:
            self._frontend_handlers[header](data)

    def _handle_customer_data(self, data):
        self._customer_data = data
        print(data)

    def _handle_stream_enable(self):
        self._port.send(struct.pack('<BI', 0x8a, 0x80000000))

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
