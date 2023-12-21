''' IMU sensor data stream '''

import time

import adhawkapi
import adhawkapi.frontend


class FrontendData:
    ''' Handle the data aggregation from backend '''

    def __init__(self):
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.IMU, self._handle_imu_data)
        self._api.start(connect_cb=self._handle_connect)

    @staticmethod
    def _handle_imu_data(timestamp, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z):
        ''' Handles the latest imu sensor data '''
        # for now just print the imu data
        print(f"time:{timestamp} gyro(x:{gyro_x}, y:{gyro_y},z:{gyro_z}) accel(x:{accel_x}, y:{accel_y}, z:{accel_z})")

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.IMU, 200, callback=(lambda *args: None))

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
