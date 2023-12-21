'''
A simple frontend example that displays markers and enables the screen tracking for eye control
instructions at https://adhawkdev.atlassian.net/browse/TRSW-3839
'''

import sys

import cv2
import cv2.aruco as aruco  # pylint: disable=no-member, import-error
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

import adhawkapi
import adhawkapi.frontend
from adhawkapi.publicapi import MarkerSequenceMode, errormsg

BOARD_IMAGE_FILE = 'board_image.png'
LOG_SESSION = False
RESOLUTION = adhawkapi.CameraResolution.MEDIUM
IMU_RATE = 100
GAZE_RATE = 60  # to work with eye control


class FrontendData:
    ''' Frontend communicating with the backend '''

    def __init__(self, camera_started_cb):
        self._camera_started_cb = camera_started_cb
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.TRACKER_STATUS, self._handle_tracker_status)
        self._api.register_stream_handler(adhawkapi.PacketType.IMU, (lambda *args: None))  # just to set the rate
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE,
                                          (lambda *args: None))  # just to set the rate
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE_IN_SCREEN, self._handle_gaze_in_screen_data)

        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)

        self._api.start(connect_cb=self._handle_connect)

    def register_screen(self, screen_width, screen_height, aruco_dic, marker_ids, markers):
        ''' Register the screen and starts tracking '''
        self._api.register_screen_board(screen_width, screen_height, aruco_dic, marker_ids, markers,
                                        self._handle_screen_registered_response)

    def trigger_camera_start(self):
        '''Send start calibrate command to backend'''
        if LOG_SESSION:
            self._api.start_log_session(log_mode=adhawkapi.LogMode.NONE)
            print('backend started logging session')
        self._api.start_camera_capture(0, RESOLUTION, False, callback=self._handle_camera_start_response)

    def shutdown(self):
        ''' Shutdown the port '''
        if LOG_SESSION:
            self._api.stop_log_session()
        self.enable_screen_tracking(False)
        self._api.stop_camera_capture(lambda *_args: None)
        self._api.shutdown()

    def calibrate(self):
        ''' Calibrate the gaze tracker '''
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_GAZE.value,
                                        n_points=5, marker_size_mm=35,
                                        randomize=True,
                                        fov=(30, 25, 0, -10),
                                        callback=lambda *x: None)

    def quickstart(self):
        ''' Perform Quickstart '''
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE.value, marker_size_mm=35, returning_user=True,
                                  callback=lambda *x: None)

    def enable_screen_tracking(self, enable):
        ''' Enable the screen tracking '''
        if enable:
            print('Starting screen tracking')
            self._api.start_screen_tracking(callback=lambda *x: None)
        else:
            print('Stopping screen tracking')
            self._api.stop_screen_tracking(callback=lambda *x: None)

    @staticmethod
    def _handle_gaze_in_screen_data(*_data):
        return

    def _handle_events(self, event_type, _timestamp, *_args):
        if event_type == adhawkapi.Events.PROCEDURE_ENDED:
            self.enable_screen_tracking(True)

    def _handle_screen_registered_response(self, response):
        if not response:
            print('aruco markers registered')
            self.enable_screen_tracking(True)

    def _handle_connect(self, error):
        if not error:
            print('backend connected')
            self._api.set_stream_control(adhawkapi.PacketType.GAZE, GAZE_RATE, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.GAZE_IN_SCREEN, GAZE_RATE, callback=(lambda *args: None))

            # just to set the rate
            self._api.set_stream_control(adhawkapi.PacketType.IMU, IMU_RATE, callback=(lambda *args: None))

            self._api.set_event_control(adhawkapi.EventControlBit.PROCEDURE_START_END, 1, callback=(lambda *args: None))
            self.trigger_camera_start()

    @staticmethod
    def _handle_tracker_status(status):
        print(f'tracker status received: {errormsg(status)}')

    def _handle_camera_start_response(self, response):
        if response:
            print(f'camera start response: {response}')
        else:
            print('camera started')
            self._api.set_camera_user_settings(adhawkapi.CameraUserSettings.PARALLAX_CORRECTION, False, lambda *x: None)
            self._camera_started_cb()


class BasicFrontend(QtWidgets.QWidget):
    ''' Class for enabling screen tracking '''
    MARKER_DIC = cv2.aruco.DICT_4X4_50  # pylint: disable=no-member
    EDGE_OFFSETS_MM = np.array([[10, 10], [10, 20]])  # [[left, right], [top, bottom]]
    MARKER_SIZE_MM = 25

    def __init__(self):
        # Create Gui Elements
        super().__init__()

        dpi_x = QtWidgets.QApplication.instance().primaryScreen().physicalDotsPerInchX()
        dpi_y = QtWidgets.QApplication.instance().primaryScreen().physicalDotsPerInchY()
        self._dpi = np.mean([dpi_x, dpi_y])
        self._size_pix = np.array([QtWidgets.QApplication.instance().primaryScreen().geometry().width(),
                                   QtWidgets.QApplication.instance().primaryScreen().geometry().height()])
        self._size_mm = self._pix_to_mm(self._size_pix)
        print(f'screen info: \n    dpi={self._dpi}\n    size_pix={self._size_pix}\n    size_mm={self._size_mm}')

        self._marker_ids = [0, 1, 2, 3]
        self._board_image = None
        self._offsets = (0, 0)

        self.setWindowTitle('Eye control frontend')

        self._markers_pos = self._create_custom_board()

        self._board_image = self._create_custom_board_image()
        cv2.imwrite(BOARD_IMAGE_FILE, self._board_image)  # pylint: disable=no-member
        self._background_widget = QtWidgets.QLabel(self)
        self._background_widget.setPixmap(QtGui.QPixmap(BOARD_IMAGE_FILE))

        self.frontend = FrontendData(self._camera_started_cb)

    def _camera_started_cb(self):
        self.frontend.register_screen(self._size_mm[0] * 1e-3, self._size_mm[1] * 1e-3,
                                      self.MARKER_DIC, self._marker_ids, self._markers_pos)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

    def _mm_to_pix(self, length_mm):
        mm2inch = 25.4
        return (np.array(length_mm) * self._dpi / mm2inch).astype(np.int)

    def _pix_to_mm(self, length_pix):
        mm2inch = 25.4
        return np.array(length_pix) * mm2inch / self._dpi

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

    def _create_custom_board_image(self, draw_id=False):
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
            self.close()
        elif event.key() == QtCore.Qt.Key_C:
            self.frontend.enable_screen_tracking(False)
            self.frontend.calibrate()
        elif event.key() == QtCore.Qt.Key_Q:
            self.frontend.enable_screen_tracking(False)
            self.frontend.quickstart()

    def closeEvent(self, event):
        '''Override method to handle closed window event.'''
        super().closeEvent(event)
        self.frontend.shutdown()


def main():
    '''Main function'''
    app = QtGui.QApplication(sys.argv)
    main_window = BasicFrontend()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
