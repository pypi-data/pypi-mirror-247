'''
A simple frontend example that enables the camera capture and receives the video stream as well as the
gaze point projected in the image
'''

import sys
import typing

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

import adhawkapi
import adhawkapi.frontend
from adhawkapi import errormsg


RESOLUTION = adhawkapi.CameraResolution.MEDIUM
MARKER_SIZE = 20  # diameter of the circle in pixels
MARKER_COLOR = (0, 250, 50)


class ImageReceiver:
    '''Class for receiving the video stream and displaying it '''

    def __str__(self):
        return self.__class__.__name__

    def __init__(self, frame_handler, shutdown_handler):
        self._frame_handler = frame_handler
        self._shutdown_handler = shutdown_handler
        self._video_receiver = adhawkapi.frontend.VideoReceiver()
        self._video_receiver.frame_received_event.add_callback(self._frame_handler)
        self._video_receiver.start()

        self._frame_size = (1000, 1000)
        self._frame = np.zeros(self._frame_size, np.uint8)
        self._frame_timestamp = 0

        self._img_size = None

    @property
    def address(self):
        ''' Return the receiver address '''
        return self._video_receiver.address


class Frontend:
    ''' Frontend communicating with the backend '''

    def __init__(self,
                 gaze_in_image_callback: typing.Callable[[float, float], None] = lambda *_args: None,
                 address=None):
        self._gaze_in_image_callback = gaze_in_image_callback
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.TRACKER_STATUS, self._handle_tracker_status)
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE_IN_IMAGE, self._handle_gaze_in_image_data)
        self._api.start(connect_cb=self._handle_connect)
        self._address = address

    def trigger_camera_start(self):
        '''Send start camera command to backend'''
        self._api.start_camera_capture(0, RESOLUTION, False, callback=self._handle_camera_start_response)

    def shutdown(self):
        ''' Shutdown the port '''
        self._stop_video_stream()
        self._api.stop_camera_capture(lambda *_args: None)
        self._api.shutdown()

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.GAZE_IN_IMAGE, 1, callback=(lambda *args: None))
            self.trigger_camera_start()

    @staticmethod
    def _handle_tracker_status(status):
        print(f'tracker status received: {errormsg(status)}')

    def _handle_gaze_in_image_data(self, *data):
        self._gaze_in_image_callback(*data)

    def _handle_camera_start_response(self, response):
        if response:
            print(f'camera start response: {response}')
        else:
            self._start_video_stream()

    def _start_video_stream(self):
        ''' Start the video streaming '''
        self._api.start_video_stream(*self._address, lambda *x: None)

    def _stop_video_stream(self):
        ''' stop video streaming '''
        self._api.stop_video_stream(*self._address, lambda *x: None)


class GazePreview(QtWidgets.QWidget):
    ''' Class for receiving the video stream and displaying it '''

    start_board_signal = QtCore.Signal()
    update_gaze_signal = QtCore.Signal(object)

    def __init__(self):
        # Create Gui Elements
        super().__init__()

        self.setWindowTitle('Video & gaze projection')

        # setup video receiver
        # create the label that holds the image
        self.image_label = QtWidgets.QLabel(self)
        # create a vertical box layout and add the two labels
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        self._image_receiver = ImageReceiver(self._handle_new_frame,
                                             self._handle_shutdown)

        self.frontend = Frontend(
            gaze_in_image_callback=self._update_gaze_in_image,
            address=self._image_receiver.address
        )

        self._frame_size = None
        self._gaze_timestamp = None
        self._frame_timestamp = None
        self._frame = None
        self._gaze_image = (0, 0)

    def closeEvent(self, event):
        '''Override method to handle closed window event.'''
        super().closeEvent(event)
        self._handle_shutdown()

    def _handle_new_frame(self, gaze_timestamp, _frame_index, image_buf, frame_timestamp):
        qt_img = QtGui.QPixmap()
        qt_img.loadFromData(image_buf, 'JPEG')
        size = qt_img.size().toTuple()
        if not np.all(np.equal(self._frame_size, size)):
            self._frame_size = size
            self.image_label.resize(self._frame_size[0], self._frame_size[1])

        self._gaze_timestamp = gaze_timestamp
        self._frame_timestamp = frame_timestamp
        self._draw_gaze_marker(qt_img)
        self.image_label.setPixmap(qt_img)

    def _update_gaze_in_image(self, _timestamp, gaze_img_x, gaze_img_y, _deg_to_pix_x, _deg_to_pix_y):
        self._gaze_image = np.array([gaze_img_x, gaze_img_y], dtype=int)

    def _handle_shutdown(self):
        self.frontend.shutdown()
        self.close()

    def _draw_gaze_marker(self, qt_img):
        painter = QtGui.QPainter(qt_img)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0), QtCore.Qt.SolidPattern))
        painter.setPen(QtGui.QPen(QtGui.QColor(*MARKER_COLOR, 1),
                                  5,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawEllipse(QtCore.QRectF(self._gaze_image[0] - MARKER_SIZE / 2,
                                          self._gaze_image[1] - MARKER_SIZE / 2,
                                          MARKER_SIZE, MARKER_SIZE))
        painter.end()


def main():
    '''Main function'''
    app = QtGui.QApplication(sys.argv)
    main_window = GazePreview()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
