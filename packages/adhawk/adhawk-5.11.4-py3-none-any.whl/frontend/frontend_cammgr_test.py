'''
A simple frontend example that that allows testing different functionalities of the camera manager:
- enables the camera capture and receives the video stream
- receives the gaze_in_image stream
- press "a" to perform an autotune via marker sequence gui
- press "q" to perform an quickstart via marker sequence gui
- press "c" to perform an calibration via marker sequence gui
- press "r" to record the video with gaze overlaid
- press "s" to run screen tracking demo

'''

import collections
import functools
import os.path
import pathlib
import sys
import threading
import time
import typing

import cv2
import cv2.aruco as aruco  # pylint: disable=no-member, import-error
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

import adhawkapi
import adhawkapi.frontend
from adhawkapi.publicapi import MarkerSequenceMode, errormsg
from adhawktools import ratelimiter


BOARD_IMAGE_FILE = 'board_image.png'
LOG_SESSION = False
RESOLUTION = adhawkapi.CameraResolution.MEDIUM
FANCY_MARKER = True  # use an animated gaze marker in the screen during screen tracking
VIDEO_EXPORT_PATH = os.path.join('logs', 'screen tracking demo')
IMU_RATE = 206


class GazeDot(QtWidgets.QLabel):
    ''' Widget to display the gaze in board sample '''
    GAZE_SIZE = 130
    TAIL_SIZE = 20  # number of samples in the tail

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(self.GAZE_SIZE * 2, self.GAZE_SIZE * 2)
        self._gaze_pos_buffer = collections.deque(maxlen=self.TAIL_SIZE)
        self._refresh_ratelimiter = ratelimiter.RateLimiter(30)

    def update_gaze(self, xpos, ypos):
        ''' Update the gaze sample '''
        if 0 in (xpos, ypos):
            return
        if self._refresh_ratelimiter.limit(''):
            self.move(xpos - self.width() / 2, ypos - self.height() / 2)

    def paintEvent(self, _event):
        ''' Override paint event '''
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0), QtCore.Qt.SolidPattern))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0, 1),
                                  5,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawEllipse(QtCore.QRectF(self.width() / 2 - self.GAZE_SIZE / 2,
                                          self.height() / 2 - self.GAZE_SIZE / 2,
                                          self.GAZE_SIZE, self.GAZE_SIZE))
        painter.end()


class FancyGazeDot(QtWidgets.QLabel):
    ''' Widget to display the gaze in board sample '''
    GAZE_SIZE = 130
    TAIL_SIZE = 20  # number of samples in the tail

    def __init__(self, parent):
        super().__init__(parent)
        self._gaze_pos_buffer = collections.deque(maxlen=self.TAIL_SIZE)
        self._refresh_ratelimiter = ratelimiter.RateLimiter(30)

    def update_gaze(self, xpos, ypos):
        ''' Update the gaze sample '''
        if 0 in (xpos, ypos):
            return
        self._gaze_pos_buffer.append([xpos, ypos])
        if self._refresh_ratelimiter.limit(''):
            self.update()

    def paintEvent(self, _event):
        ''' Override paint event '''
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 0), QtCore.Qt.SolidPattern))
        for sample_index, sample in enumerate(self._gaze_pos_buffer):
            painter.setPen(QtGui.QPen(QtGui.QColor(
                255,  # red
                255 - 255 * (sample_index / self.TAIL_SIZE),  # green
                0,  # blue
                255 * (sample_index / self.TAIL_SIZE)),
                10 * (sample_index / self.TAIL_SIZE),
                QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap,
                QtCore.Qt.RoundJoin))
            size = self.GAZE_SIZE * ((sample_index + 1) / self.TAIL_SIZE)
            painter.drawEllipse(QtCore.QRectF(sample[0] - size / 2,
                                              sample[1] - size / 2,
                                              size, size))
        painter.end()


class BoardWindow(QtWidgets.QLabel):
    ''' Handles showing a single centered marker in a dedicated window '''

    def __init__(self, close_cb=lambda *args: None):
        super().__init__()
        self._close_cb = close_cb

        self._background_widget = QtWidgets.QLabel(self)
        self._background_widget.setPixmap(QtGui.QPixmap(BOARD_IMAGE_FILE))

        if FANCY_MARKER:
            self._gaze_widget = FancyGazeDot(self)
        else:
            self._gaze_widget = GazeDot(self)
        self._gaze_widget.show()

    def resizeEvent(self, event):
        ''' Override method to setup window when displaying '''
        super().resizeEvent(event)
        self._gaze_widget.update()
        self._gaze_widget.setFixedSize(self.width(), self.height())
        self._gaze_widget.move(0, 0)

    def closeEvent(self, event):
        ''' Override method to handle closed window event.'''
        super().closeEvent(event)
        self._close_cb()

    def update_gaze(self, gaze_pos):
        ''' Update the gaze sample '''
        self._gaze_widget.update_gaze(*gaze_pos)


class Board:
    ''' Display the marker window '''

    MARKER_DIC = cv2.aruco.DICT_5X5_50  # pylint: disable=no-member
    EDGE_OFFSETS_MM = np.array([[10, 10], [10, 20]])  # [[left, right], [top, bottom]]
    MARKER_SIZE_MM = 30

    def __init__(self, register_screen_cb, shutdown_handler):
        super().__init__()
        self._register_screen_cb = register_screen_cb
        self._shutdown_handler = shutdown_handler

        self._board_window = None

        dpi_x = QtWidgets.QApplication.instance().primaryScreen().physicalDotsPerInchX()
        dpi_y = QtWidgets.QApplication.instance().primaryScreen().physicalDotsPerInchY()
        self._dpi = np.mean([dpi_x, dpi_y])
        self._size_pix = np.array([QtWidgets.QApplication.instance().primaryScreen().geometry().width(),
                                   QtWidgets.QApplication.instance().primaryScreen().geometry().height()])
        self._size_mm = self._pix_to_mm(self._size_pix)
        print(f'screen info: \n    dpi={self._dpi}\n    size_pix={self._size_pix}\n    size_mm={self._size_mm}')

        self._marker_ids = [0, 1, 2, 3]
        self._board_image = None
        self._gaze_in_image = None
        self._refresh_gui = True
        self._offsets = (0, 0)

    def start(self):
        ''' Define the board '''
        markers_pos = self._create_custom_board()
        self._register_screen_cb(self._size_mm[0] * 1e-3, self._size_mm[1] * 1e-3,
                                 self.MARKER_DIC, self._marker_ids, markers_pos)

        self._board_image = self._create_custom_board_image()
        # save the image
        cv2.imwrite(BOARD_IMAGE_FILE, self._board_image)  # pylint: disable=no-member
        self._board_window = BoardWindow(self._shutdown_handler)
        self._board_window.setWindowTitle('Board Window')
        self._board_window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self._board_window.showMaximized()

    def stop(self):
        ''' close the board window '''
        self._board_window.close()

    @property
    def board_image(self):
        ''' Return the board image '''
        return self._board_image

    def _mm_to_pix(self, length_mm):
        cm2inch = 2.54
        return (np.array(length_mm) * 1e-1 * self._dpi / cm2inch).astype(np.int)

    def _pix_to_mm(self, length_pix):
        cm2inch = 2.54
        return np.array(length_pix) * cm2inch / (1e-1 * self._dpi)

    @staticmethod
    def _draw_text(image, text, scale, position):
        # pylint: disable=no-member
        # draw duration
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        text_thickness = 1
        text_size, _ = cv2.getTextSize(text, fontface, scale, text_thickness)
        text_origin = (position[0] - text_size[0] / 2, position[1] + text_size[1] / 2)
        cv2.putText(image, text,
                    (int(text_origin[0]), int(text_origin[1])),
                    fontFace=fontface,
                    fontScale=scale,
                    color=0)

    def _create_custom_board_image(self, draw_id=True):
        # we assume the origin to be at the very top/left corner of the window

        marker_size = int(self._size_pix[0] * self.MARKER_SIZE_MM / self._size_mm[0])
        margins = self._mm_to_pix(self.EDGE_OFFSETS_MM)
        board_image = np.ones((self._size_pix[1], self._size_pix[0]), dtype=np.uint8) * 255

        # place the markers in the image
        offsets = {0: (margins[0, 0], margins[1, 0]),
                   1: (self._size_pix[0] - margins[0, 1] - marker_size, margins[1, 0]),
                   2: (margins[0, 0], self._size_pix[1] - margins[1, 1] - marker_size),
                   3: (self._size_pix[0] - margins[0, 1] - marker_size,
                       self._size_pix[1] - margins[1, 1] - marker_size)}

        for _id_i, _id in enumerate(self._marker_ids):
            _img = np.zeros((marker_size, marker_size), dtype=np.uint8)
            _img = aruco.drawMarker(aruco.Dictionary_get(self.MARKER_DIC), _id, marker_size, _img, 1)
            board_image[offsets[_id_i][1]:offsets[_id_i][1] + marker_size,
                        offsets[_id_i][0]:offsets[_id_i][0] + marker_size] = _img

            if draw_id:
                scale = 1
                pos_x = offsets[_id_i][0] + marker_size / 2
                pos_y = offsets[_id_i][1] + marker_size + int(0.2 * marker_size)
                self._draw_text(board_image,
                                str(_id),
                                scale,
                                (pos_x, pos_y))

        return board_image

    def _create_custom_board(self):
        # position of the bottom/left corners of the 4 markers inside the board
        # we assume the origin to be at the very top/left corner of the window
        margin_size = self.EDGE_OFFSETS_MM * 1e-3
        board_size = self._size_mm * 1e-3
        marker_size = self.MARKER_SIZE_MM * 1e-3
        positions = np.array([
            [margin_size[0, 0], - margin_size[1, 0] - marker_size],
            [board_size[0] - margin_size[0, 1] - marker_size, - margin_size[1, 0] - marker_size],
            [margin_size[0, 0], - board_size[1] + margin_size[1, 1]],
            [board_size[0] - margin_size[0, 1] - marker_size, - board_size[1] + margin_size[1, 1]],
        ])
        markers = []
        for marker_pos in positions:
            markers.append([*marker_pos, marker_size])
        return markers

    def update_gaze_dot(self, gaze_pos=(0, 0)):
        ''' Get the gaze xy pos in the board coordinate system in meter, convert the xy to pixels and draw on
        the board '''
        if (self._board_image is None) or np.any(np.isnan(gaze_pos)):
            return
        # print(gaze_pos)
        img_h, img_w = self._board_image.shape

        x_pix = np.clip(gaze_pos[0] * img_w, 0, img_w)
        y_pix = np.clip(gaze_pos[1] * img_h, 0, img_h)
        self._board_window.update_gaze((x_pix, y_pix))


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


class FrontendData:
    ''' Frontend communicating with the backend '''

    def __init__(self,
                 gaze_in_image_callback:
                 typing.Callable[[float, float, float, float, float], None] = lambda *_args: None,
                 gaze_in_screen_callback: typing.Callable[[float, float, float], None] = lambda *_args: None,
                 address=None,
                 ):
        self._gaze_in_image_callback = gaze_in_image_callback
        self._gaze_in_screen_callback = gaze_in_screen_callback
        self._address = address
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.TRACKER_STATUS, self._handle_tracker_status)
        self._api.register_stream_handler(adhawkapi.PacketType.IMU, (lambda *args: None))  # just to set the rate
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE_IN_IMAGE, self._handle_gaze_in_image_data)
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE_IN_SCREEN, self._handle_gaze_in_screen_data)
        # this is only used to check the imu calibration state
        self._api.register_stream_handler(adhawkapi.PacketType.IMU_ROTATION, self._handle_imu_rotation)
        self._imu_calibrated = False
        self._user_instructed_to_calibrate_imu = False
        self._api.start(connect_cb=self._handle_connect)

    @property
    def imu_calibrated(self):
        ''' indicate if the imu in the backend is calibrated or not '''
        return self._imu_calibrated

    def register_screen(self, screen_width, screen_height, aruco_dic, marker_ids, markers):
        ''' Register the screen and starts tracking '''
        self._api.register_screen_board(screen_width, screen_height, aruco_dic, marker_ids, markers,
                                        lambda *_args: None)

    def trigger_camera_start(self):
        '''Send start calibrate command to backend'''
        if LOG_SESSION:
            self._api.start_log_session(log_mode=adhawkapi.LogMode.NONE)
        self._api.start_camera_capture(0, RESOLUTION, False, callback=self._handle_camera_start_response)

    def shutdown(self):
        ''' Shutdown the port '''
        if LOG_SESSION:
            self._api.stop_log_session()
        self.enable_screen_tracking(False)
        self._stop_video_stream()
        self._api.stop_camera_capture(lambda *_args: None)
        self._api.shutdown()

    def calibrate(self):
        ''' Calibrate the gaze tracker '''
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_GAZE.value,
                                        n_points=5, marker_size_mm=35,
                                        randomize=True,
                                        fov=(30, 25, 0, -10),
                                        callback=lambda *x: None)

    def autotune(self):
        ''' Perform Autotune '''
        self._api.autotune_gui(mode=MarkerSequenceMode.FIXED_GAZE.value,
                               marker_size_mm=35,
                               callback=lambda *x: None)

    def quickstart(self):
        ''' Perform Quickstart '''
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE.value, marker_size_mm=35, returning_user=True,
                                  callback=lambda *x: None)

    def enable_screen_tracking(self, enable):
        ''' Enable the screen tracking '''
        if enable:
            print('Screen tracking on')
            self._api.start_screen_tracking(lambda *_args: None)
        else:
            print('Screen tracking off')
            self._api.stop_screen_tracking(lambda *_args: None)

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.GAZE_IN_IMAGE, 60, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.GAZE_IN_SCREEN, 60, callback=(lambda *args: None))

            # just to set the rate
            self._api.set_stream_control(adhawkapi.PacketType.IMU, IMU_RATE, callback=(lambda *args: None))
            # just to check the imu calibration status
            self._api.set_stream_control(adhawkapi.PacketType.IMU_ROTATION, 1, callback=(lambda *args: None))

            self.trigger_camera_start()

    def _handle_imu_rotation(self, _timestamp, *rvec):
        if np.all(np.isfinite(rvec)):
            if not self._imu_calibrated:
                self._imu_calibrated = True
        else:
            if self._imu_calibrated:
                self._imu_calibrated = False
                self._user_instructed_to_calibrate_imu = False
            if not self._user_instructed_to_calibrate_imu:
                self._user_instructed_to_calibrate_imu = True

    @staticmethod
    def _handle_tracker_status(status):
        print(f'tracker status received: {errormsg(status)}')

    def _handle_gaze_in_image_data(self, *data):
        self._gaze_in_image_callback(*data)

    def _handle_gaze_in_screen_data(self, *data):
        self._gaze_in_screen_callback(*data)

    def _handle_camera_start_response(self, response):
        if response:
            print(f'camera start response: {response}')
        else:
            self._api.set_camera_user_settings(adhawkapi.CameraUserSettings.PARALLAX_CORRECTION, False, lambda *x: None)
            self._start_video_stream()

    def _start_video_stream(self):
        ''' Start the video streaming '''
        self._api.start_video_stream(*self._address, lambda *x: None)

    def _stop_video_stream(self):
        ''' stop video streaming '''
        self._api.stop_video_stream(*self._address, lambda *x: None)


class BasicFrontend(QtWidgets.QWidget):
    ''' Class for receiving the video stream and displaying it '''

    update_gaze_in_screen_signal = QtCore.Signal(object)

    def __init__(self):
        # Create Gui Elements
        super().__init__()

        self._frame_size = None
        self._gaze_timestamp = None
        self._frame_timestamp = None
        self._gaze_in_image = (0, 0)
        self.setWindowTitle('Basic frontend')

        self._board = None

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

        self.frontend = FrontendData(
            gaze_in_image_callback=self._update_gaze_in_image,
            gaze_in_screen_callback=self._update_screen_image,
            address=self._image_receiver.address,
        )

        # video export
        self._stop = False
        self._buffer = collections.deque()
        self._writer = None
        self._writer_thread = None

    def keyPressEvent(self, event):
        '''Override default keyPressEvent behaviour so we can track key press'''
        super().keyPressEvent(event)
        if event.isAutoRepeat():
            return

    def keyReleaseEvent(self, event):
        '''Override default keyReleaseEvent behaviour so we can track key release'''
        super().keyReleaseEvent(event)
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_Escape:
            self._handle_shutdown()
        elif event.key() == QtCore.Qt.Key_C:
            self._enable_screen_tracking(False)
            self.frontend.calibrate()
        elif event.key() == QtCore.Qt.Key_A:
            self._enable_screen_tracking(False)
            self.frontend.autotune()
        elif event.key() == QtCore.Qt.Key_Q:
            self._enable_screen_tracking(False)
            self.frontend.quickstart()
        elif event.key() == QtCore.Qt.Key_S:
            self._enable_screen_tracking(self._board is None)
        elif event.key() == QtCore.Qt.Key_R:
            if self._writer:
                self._stop_recording()
            else:
                self._start_recording()

    def closeEvent(self, event):
        '''Override method to handle closed window event.'''
        super().closeEvent(event)
        self._handle_shutdown()

    def convert_cv_qt(self, cv_img):
        ''' Convert from an opencv image to QPixmap '''
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, dimention = rgb_image.shape
        bytes_per_line = dimention * width
        convert_to_qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = convert_to_qt_format.scaled(self._frame_size[0], self._frame_size[1], QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(pixmap)

    def _enable_screen_tracking(self, enable):
        if enable:
            self._board = Board(self._register_screen, functools.partial(self._enable_screen_tracking, False))
            self.update_gaze_in_screen_signal.connect(self._board.update_gaze_dot)
            self._board.start()
            self.frontend.enable_screen_tracking(True)
        else:
            if self._board is not None:
                self._board.stop()
                self._board = None
                self.frontend.enable_screen_tracking(False)

    def _handle_new_frame(self, gaze_timestamp, _frame_index, image_buf, frame_timestamp):
        image = cv2.imdecode(np.frombuffer(image_buf, dtype=np.uint8), 1)
        if not np.all(np.equal(self._frame_size, image.shape[:2][::-1])):
            self._frame_size = image.shape[:2][::-1]
            self.image_label.resize(self._frame_size[0], self._frame_size[1])

        self._gaze_timestamp = gaze_timestamp
        self._frame_timestamp = frame_timestamp

        if np.isfinite(self._gaze_in_image[0]) and np.isfinite(self._gaze_in_image[1]):
            cv2.circle(image, (int(self._gaze_in_image[0]), int(self._gaze_in_image[1])), 8, (0, 250, 50), -1)
        if self._writer:
            self._buffer.append(image.copy())
            cv2.circle(image, (self._frame_size[0] - 50, 50), 25, (0, 0, 250), -1)

        # instructions
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)
        thickness = 2
        line_type = 2
        for line, text in enumerate([
            'a: Autotune',
            'q: Quickstart',
            'c: Calibration',
            'r: Toggle Video Record',
            's: Screen Tracking',
        ]):
            cv2.putText(image,
                        text,
                        (10, 50 + line * 50),
                        font,
                        font_scale,
                        font_color,
                        thickness,
                        line_type)

        if not self.frontend.imu_calibrated:
            cv2.putText(image,
                        'IMU not calibrated',
                        (self._frame_size[0] - 300, 100),
                        font,
                        font_scale,
                        (0, 0, 255),
                        thickness,
                        line_type)
        qt_img = self.convert_cv_qt(image)
        self.image_label.setPixmap(qt_img)

    def _start_recording(self):
        pathlib.Path(VIDEO_EXPORT_PATH).mkdir(parents=True, exist_ok=True)
        self._writer = cv2.VideoWriter(
            os.path.join(VIDEO_EXPORT_PATH, 'video.mp4'),
            cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
            30,
            self._frame_size)
        self._writer_thread = threading.Thread(target=self._write_frames, name='RecordVideo')
        self._writer_thread.start()

    def _stop_recording(self):
        self._stop = True
        if self._writer_thread and self._writer_thread.is_alive():
            self._writer_thread.join()
            self._writer_thread = None
        self._buffer.clear()
        if self._writer:
            print(f"video exported to {os.path.join(VIDEO_EXPORT_PATH, 'video.mp4')}")
            self._writer.release()
            self._writer = None

    def _write_frames(self):
        while not self._stop:
            if self._buffer and self._writer:
                try:
                    self._writer.write(self._buffer.popleft())
                except cv2.error:
                    pass
            else:
                time.sleep(1 / 30)

    def _register_screen(self, screen_width, screen_height, aruco_dic, marker_ids, markers):
        self.frontend.register_screen(screen_width, screen_height, aruco_dic, marker_ids, markers)

    def _update_gaze_in_image(self, _timestamp, gaze_img_x, gaze_img_y, _deg_to_pix_x, _deg_to_pix_y):
        self._gaze_in_image = (gaze_img_x, gaze_img_y)

    def _update_screen_image(self, _timestamp, gaze_x, gaze_y):
        self.update_gaze_in_screen_signal.emit((gaze_x, gaze_y))

    def _handle_shutdown(self):
        self._enable_screen_tracking(False)
        self._stop_recording()
        self.frontend.shutdown()
        self.close()


def main():
    '''Main function'''
    app = QtGui.QApplication(sys.argv)
    main_window = BasicFrontend()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
