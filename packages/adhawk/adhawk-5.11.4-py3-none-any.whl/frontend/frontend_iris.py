''' Demo for AdHawk's Iris Imager

Requirements:
- Windows 10
- Python 3.6+
- Additional python packages: numpy PyQt5 pyqtgraph pillow
  e.g. python -m pip install numpy PyQt5 pyqtgraph pollow

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend\\frontend_iris.py

'''


import argparse
import datetime
import os
import sys
import threading

import numpy as np
import PIL.Image
import pyqtgraph
from pyqtgraph.dockarea import Dock
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

import adhawkapi
import adhawkapi.frontend
import adhawkapi.frontend.internal as internalapi
from adhawkguitools.standardappstyle import guibuilder


N_TRACKERS = 2  # Number of tracker modules
IMAGE_WIDTH = 140  # pixels, image size = IMAGE_WDITH * IMAGE_WIDTH
DEFAULT_SCAN_POWER = 70  # %


class DockablePicture(Dock):
    '''Plot for displaying a photo.'''

    def __init__(self, name: str):
        super().__init__(name)
        self._q_label = QtWidgets.QLabel()
        self._q_label.setScaledContents(True)
        self._picture_viewer = QtGui.QPixmap()
        self.addWidget(self._q_label)

    def set_image(self, image: str) -> None:
        '''Set the image of this plot using a string containing the path to the resource.'''
        p_map = QtGui.QPixmap(image)
        self._q_label.setPixmap(p_map)


class FrontendData:
    ''' Handle the data aggregation from backend '''

    def __init__(self, on_connected=None, on_captured=None, on_autotuned=None):
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.IRIS_IMAGE_DATA_STREAM, self._handle_image_data)
        self._internalapi = internalapi.InternalApi()
        self._on_connected = on_connected
        self._on_captured = on_captured
        self._on_autotuned = on_autotuned
        self._internalapi.start()
        self._api.start(connect_cb=self._handle_connect)

        # image data streams are expected to be a constant size of 100
        self._num_image_data_expected = 100
        self._num_image_data_collected = {tracker_id: 0 for tracker_id in range(N_TRACKERS)}
        self._image_data = {tracker_id: [0] * int(IMAGE_WIDTH ** 2)
                            for tracker_id in range(N_TRACKERS)}

    def _reset_data(self):
        self._num_image_data_collected = {tracker_id: 0 for tracker_id in range(N_TRACKERS)}
        self._image_data = {tracker_id: [0] * int(IMAGE_WIDTH ** 2)
                            for tracker_id in range(N_TRACKERS)}

    def _handle_connect(self, _error):
        if callable(self._on_connected):
            self._on_connected()

    def _handle_image_data(self, tracker_id, index, *data):
        if self._num_image_data_expected != len(data):
            print(f'Received image stream with missing data. '
                  f'expected={self._num_image_data_expected}, received={len(data)}')
            return

        if index >= IMAGE_WIDTH**2:
            print('Received bad index')
            return

        if self._num_image_data_collected[tracker_id] >= IMAGE_WIDTH**2:
            print('Received bad data')
            return

        self._image_data[tracker_id][index:] = data
        self._num_image_data_collected[tracker_id] += len(data)

    def trigger_capture(self):
        '''Start iris capture on active trackers'''
        self._api.iris_trigger_capture(callback=self._handle_capture_ended)

    def trigger_autotune(self):
        '''Start the autotune process'''
        self._api.trigger_autotune(callback=self._handle_autotune_results)

    def set_scan_power(self, eyeindex, laser_pct, callback=None):
        '''Set scan power for a given eye in percentage'''
        self._internalapi.set_scan_power(eyeindex, laser_pct, callback=callback)

    def get_scan_power(self, eyeindex, callback=None):
        '''Get scan power for a given eye in percentage'''
        return self._internalapi.get_scan_power(eyeindex, callback=callback)

    def _handle_autotune_results(self, *args):
        print('Autotune completed')
        ack = adhawkapi.AckCodes(args[0])
        if self._on_autotuned is not None:
            self._on_autotuned(ack)

    def _handle_capture_ended(self, *args):
        print('Iris imaging completed')
        ack = adhawkapi.AckCodes(args[0])
        if self._on_captured is not None:
            self._on_captured(ack, self._image_data[0].copy(), self._image_data[1].copy())

        self._reset_data()

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()
        self._internalapi.shutdown()


class MainWindow(QtGui.QMainWindow):  # pylint: disable=too-few-public-methods
    ''' Main pyqtgraph Gui window '''

    # pylint: disable=too-many-instance-attributes

    _warning_signal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(canvas)

        self._capture_image_button = QtWidgets.QPushButton('Capture')
        self._capture_image_button.clicked.connect(self._handle_capture_pressed)

        self._continuous_capture = None
        self._imaging = False
        self._params = self._build_param_area()
        self._plot_right = DockablePicture('Iris Right')
        self._plot_left = DockablePicture('Iris Left')

        self._warning_signal.connect(self._show_dialog)
        self._warning_dialog = guibuilder.build_popup(title='AdHawk Frontend Warning',
                                                      icon=QtWidgets.QMessageBox.Warning)

        save_layout = QtWidgets.QVBoxLayout()
        save_layout.addWidget(self._select_destination_button)
        save_layout.addWidget(self._destination_folder)
        save_layout.setAlignment(QtCore.Qt.AlignTop)

        grid = QtWidgets.QVBoxLayout()
        grid.addWidget(self._capture_image_button)
        grid.addWidget(self._autotune_button)
        grid.addWidget(self._params)

        self._save_grid = QtWidgets.QGroupBox()
        self._save_grid.setLayout(save_layout)

        grid.addWidget(self._save_grid)
        grid.setAlignment(QtCore.Qt.AlignTop)

        self._param_area = grid
        self._work_area = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        param_widget = QtWidgets.QWidget()
        param_widget.setLayout(self._param_area)
        self._work_area.addWidget(param_widget)
        self._work_area.setCollapsible(0, True)
        self._work_area.setStretchFactor(0, 1)
        self._work_area.addWidget(self._plot_left)
        self._work_area.setCollapsible(1, False)
        self._work_area.setStretchFactor(1, 7)
        self._work_area.addWidget(self._plot_right)
        self._work_area.setCollapsible(2, False)
        self._work_area.setStretchFactor(2, 7)
        self._work_area.setEnabled(True)
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(self._work_area)
        canvas.addItem(proxy)

        # set of image captures are discarded if:
        # - frontend just connected to the backend
        # - set laser power api was called
        self._discard_next_frame = True

        # keep all ui elements disabled until connected to backend
        self._disable_params()
        self.frontend = FrontendData(self._on_connected, self._on_captured, self._on_autotuned)

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()

    def _on_connected(self):
        print('Successfully connected to backend')
        self._enable_params()
        self._discard_next_frame = True

    def _show_dialog(self, message):
        self._warning_dialog.setText(message)
        self._warning_dialog.exec_()
        self._enable_params()

    def _handle_captured_image(self, images, image_plots, names, savetofile):
        for image_data, image_plot, name, save in zip(images, image_plots, names, savetofile):
            image = np.array(image_data).reshape(IMAGE_WIDTH, IMAGE_WIDTH)
            image = np.require(image, np.uint8, 'C')
            qimg = QtGui.QImage(image, image.shape[1], image.shape[0],
                                QtGui.QImage.Format_Grayscale8)
            image_plot.set_image(qimg)
            if save:
                now = datetime.datetime.now(tz=datetime.timezone.utc)
                datesuffix = now.astimezone().strftime('%Y%m%d_%H%M%S_%f')
                filename = f'iris_{name}_{datesuffix}'
                dirpath = str(self._destination_folder.text())
                if not os.path.isdir(dirpath):
                    os.makedirs(dirpath)

                path = os.path.join(dirpath, filename)
                image_tosave = PIL.Image.fromarray(image.copy().astype(np.uint8))
                image_tosave.save(f'{path}.png', 'png')

    def _enable_params(self):
        self._capture_image_button.setEnabled(True)
        self._autotune_button.setEnabled(True)
        self._params.setEnabled(True)
        self._save_grid.setEnabled(True)

    def _disable_params(self):
        self._capture_image_button.setEnabled(False)
        self._autotune_button.setEnabled(False)
        self._params.setEnabled(False)
        self._save_grid.setEnabled(False)

    def _on_autotuned(self, ack):
        if ack != adhawkapi.AckCodes.SUCCESS:
            self._warning_signal.emit(f'Autotune Failed: {adhawkapi.AckCodes(ack).name.lower().replace("_", " ")}')
        else:
            self._enable_params()

    def _on_captured(self, ack, image_right, image_left):
        if ack != adhawkapi.AckCodes.SUCCESS:
            self._warning_signal.emit(f'Image Capture Failed: {adhawkapi.AckCodes(ack).name.lower().replace("_", " ")}')
        elif not self._discard_next_frame:
            threading.Thread(target=self._handle_captured_image,
                             args=([image_left, image_right], [self._plot_left, self._plot_right],
                                   ['left', 'right'], [self._save_left_eye.isChecked(),
                                                       self._save_right_eye.isChecked()])).start()
        self._handle_end_of_captures()

    def _build_param_area(self):
        self._select_destination_button = QtWidgets.QPushButton('Select Destination')
        self._select_destination_button.clicked.connect(self._handle_dialog)

        self._save_right_eye = QtWidgets.QCheckBox('Save Right Eye')
        self._save_left_eye = QtWidgets.QCheckBox('Save Left Eye')
        self._continuous_capture = QtWidgets.QCheckBox('Continuous Imaging')

        self._scan_power_btn_right = QtWidgets.QPushButton('Set Right Scan Power (%)')
        self._scan_power_btn_right.clicked.connect(lambda: self._set_scan_power(0))

        self._autotune_button = QtWidgets.QPushButton('Autotune')
        self._autotune_button.clicked.connect(self._autotune)

        self._scan_power_btn_left = QtWidgets.QPushButton('Set Left Scan Power (%)')
        self._scan_power_btn_left.clicked.connect(lambda: self._set_scan_power(1))

        self._scan_power_right = QtWidgets.QLineEdit()
        self._scan_power_right.setText(str(DEFAULT_SCAN_POWER))
        self._scan_power_left = QtWidgets.QLineEdit()
        self._scan_power_left.setText(str(DEFAULT_SCAN_POWER))

        validator = QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]$|^[1-9][0-9]$|^(100)$"),
                                           self._scan_power_right)
        self._scan_power_right.setValidator(validator)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]$|^[1-9][0-9]$|^(100)$"),
                                           self._scan_power_left)
        self._scan_power_left.setValidator(validator)

        self._destination_folder = QtWidgets.QLabel(os.getcwd())
        self._destination_folder.setWordWrap(True)

        params_layout = QtWidgets.QVBoxLayout()
        params_layout.addWidget(self._scan_power_btn_right)
        params_layout.addWidget(self._scan_power_right)
        params_layout.addWidget(self._scan_power_btn_left)
        params_layout.addWidget(self._scan_power_left)
        params_layout.addWidget(self._continuous_capture)
        params_layout.addWidget(self._save_right_eye)
        params_layout.addWidget(self._save_left_eye)
        params_layout.setAlignment(QtCore.Qt.AlignTop)
        grid = QtWidgets.QGroupBox()
        grid.setLayout(params_layout)

        return grid

    def _autotune(self):
        self._disable_params()
        self.frontend.trigger_autotune()

    def _set_scan_power(self, eyeindex):
        self._discard_next_frame = True
        if eyeindex == 0:
            self.frontend.set_scan_power(0, float(self._scan_power_right.text()))
        else:
            self.frontend.set_scan_power(1, float(self._scan_power_left.text()))

    def _handle_end_of_captures(self):
        continuous = self._continuous_capture.isChecked()
        if self._imaging:
            if continuous or self._discard_next_frame:
                self._discard_next_frame = False
                self.frontend.trigger_capture()
            else:
                self._handle_capture_pressed()

    def _handle_capture_pressed(self):
        continuous = self._continuous_capture.isChecked()
        if self._imaging:
            self._capture_image_button.setText('Capture')
            self._enable_params()
            self._imaging = False
        else:
            self._disable_params()
            self.frontend.trigger_capture()
            if continuous:
                self._capture_image_button.setText('Stop Capture')
                self._capture_image_button.setEnabled(True)
            self._imaging = True

    def _handle_dialog(self):
        destination_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select destination folder', '',
            options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        self._destination_folder.setText(destination_folder)


def main():
    ''' App entrypoint '''
    parser = argparse.ArgumentParser(description='Iris Imaging Frontend')

    parser.parse_args(sys.argv[2:])

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
