'''
A simple frontend example that enables the camera capture and receives the video stream
dependency: opencv-contrib-python
'''
import logging
import sys
import threading

import cv2
import numpy as np

import adhawkapi
import adhawkapi.frontend


RESOLUTION = adhawkapi.CameraResolution.MEDIUM


class FrontendData:
    ''' grab the imu data from backend '''

    def __init__(self, receiver_addr):
        self._receiver_addr = receiver_addr
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.start(connect_cb=self._handle_connect)

    def _handle_connect(self, error):
        if error == adhawkapi.AckCodes.SUCCESS:
            threading.Thread(target=self._trigger_camera_start).start()

    def _trigger_camera_start(self):
        '''Send start calibrate command to backend'''
        self._api.start_camera_capture(0, RESOLUTION, callback=self._handle_camera_start_response)
        print(f'self._receiver_addr: {self._receiver_addr}')
        self._api.start_video_stream(*self._receiver_addr, lambda x: None)

    @staticmethod
    def _handle_camera_start_response(response):
        print(response)

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.stop_camera_capture(lambda x: None)
        self._api.stop_video_stream(*self._receiver_addr, lambda x: None)
        self._api.shutdown()


class ImageReceiver():
    '''Class for receiving the video stream and displaying it '''

    def __str__(self):
        return self.__class__.__name__

    def __init__(self, ):

        self._video_receiver = adhawkapi.frontend.VideoReceiver()
        self._video_receiver.frame_received_event.add_callback(self._handle_new_frame)

        self.frontend = FrontendData(self._video_receiver.address)
        self._image_size = (1000, 1000)
        self._image = np.zeros(self._image_size, np.uint8)
        self._window_title = "receiver"
        self._opencv_window_thread = threading.Thread(target=self._display, name='opencv window')
        self._opencv_window_thread.start()

    def _handle_new_frame(self, _timestamp, _frame_index, image_buf):
        image = cv2.imdecode(np.frombuffer(image_buf, dtype=np.uint8), 1)
        if not np.all(np.equal(self._image_size, image.shape[:2][::-1])):
            self._image_size = image.shape[:2][::-1]
            window_width = 1000
            cv2.resizeWindow(self._window_title, window_width,
                             int(window_width * self._image_size[1] / self._image_size[0]))

        self._image = image

    def _display(self):

        cv2.namedWindow(self._window_title, cv2.WINDOW_GUI_NORMAL)
        cv2.waitKey(1)
        cv2.imshow(self._window_title, self._image)

        self._video_receiver.start()

        while True:
            img = np.copy(self._image)
            key_code = cv2.waitKey(1)
            if (key_code == 27) or (key_code == ord('q')):  # break by ECS key
                break

            cv2.putText(img, f"{img.shape[:2][::-1]}, {self._video_receiver.fps:.2f} fps, "
                        f"{1e-6 * self._video_receiver.bitrate:.2f} Mbps",
                        (0, img.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 255),
                        2,
                        cv2.LINE_AA)

            cv2.imshow(self._window_title, img)

        self._video_receiver.shutdown()
        self.frontend.shutdown()
        sys.exit(0)


def main():
    '''Main function'''
    logging.basicConfig(level=logging.INFO,
                        style='{',
                        format='{asctime} {levelname}:  {message}')
    ImageReceiver()
    sys.exit(0)
