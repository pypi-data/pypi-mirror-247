''' IMU sensor data stream '''

import os
import pickle
import sys
import time

import numpy as np
import pyqtgraph
from pyqtgraph.dockarea import DockArea
from pyqtgraph.Qt import QtCore, QtGui
from scipy.spatial.transform import Rotation as R

import adhawkapi
import adhawkapi.frontend
from adhawkguitools.gltools.opengl_gui import DockableGLView, GLObject


class OffsetTimer:
    ''' Provides a timestamp whose epoch can be set '''

    def __init__(self):
        self._dt = 0

    @property
    def timestamp(self):
        ''' Get the current timestamp '''
        return time.perf_counter() + self._dt

    @timestamp.setter
    def timestamp(self, timestamp):
        ''' Set the current timestamp '''
        self._dt = timestamp - time.perf_counter()


class FrontendData:
    ''' Handle the data aggregation from backend '''

    imu_rate = 200
    plot_window = 2  # sec

    def __init__(self, handler):
        os.makedirs('gyro_logs', exist_ok=True)
        self._timer = OffsetTimer()
        self.bufsize = self.plot_window * self.imu_rate
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.IMU, self._handle_raw_imu)
        self._api.register_stream_handler(adhawkapi.PacketType.IMU_ROTATION, self._handle_imu_rotation)
        self._api.start(connect_cb=self._handle_connect)

        self._data_buf = np.zeros((self.bufsize, 6))
        self._data_tbuf = np.zeros(self.bufsize)
        self._data_bufptr = 0
        self._handler = handler
        self._data_all = []

    def _handle_raw_imu(self, timestamp, *data):
        ''' Handles the latest imu sensor data '''

        gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = np.array(data) * 1e-3

        self._data_all.append([timestamp, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z])

        self._data_buf[self._data_bufptr] = [gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z]
        self._data_tbuf[self._data_bufptr] = timestamp
        self._data_bufptr = (self._data_bufptr + 1) % self.bufsize
        self._timer.timestamp = timestamp

    def _handle_imu_rotation(self, timestamp, *data):
        ''' Handles the latest imu rotation data (after sensor fusion) '''

        self._handler(timestamp, data)

    def get_data(self):
        ''' get error data time series dictionary '''
        order = np.concatenate((np.arange(self._data_bufptr, self.bufsize),
                                np.arange(self._data_bufptr)))
        pdata = self._data_buf[order]
        tdata = self._data_tbuf[order] - self._timer.timestamp
        return tdata, pdata

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.IMU,
                                         self.imu_rate, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.IMU_ROTATION,
                                         self.imu_rate, callback=(lambda *args: None))

    def shutdown(self):
        ''' Shutdown the port '''
        with open('gyro_logs\\data.pkl', 'wb') as handle:
            pickle.dump(self._data_all, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self._api.shutdown()


# Colors for drawing the plots
ALLCOLORS = [
    QtGui.QColor(255, 0, 0, 255),  # R
    QtGui.QColor(0, 255, 0, 255),  # G
    QtGui.QColor(0, 0, 255, 255)]  # B
ALLBRUSHES = [pyqtgraph.mkBrush(color) for color in ALLCOLORS]


class ImuCube3D(DockArea):
    ''' Plot a cube in a ``DockableGlView`` and control its object transformation '''

    RATE = 200

    def __init__(self):
        super().__init__()

        self._glwindow = DockableGLView('OpenGL View')

        vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
        colors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1))
        normals = [[c * 2 - 1 for c in color] for color in colors]
        faces = ({'indices': (3, 2, 1, 0), 'normals': (0, 0, 0, 0), 'material': 0},
                 {'indices': (6, 7, 2, 3), 'normals': (1, 1, 1, 1), 'material': 1},
                 {'indices': (4, 5, 7, 6), 'normals': (2, 2, 2, 2), 'material': 2},
                 {'indices': (0, 1, 5, 4), 'normals': (3, 3, 3, 3), 'material': 3},
                 {'indices': (2, 7, 5, 1), 'normals': (4, 4, 4, 4), 'material': 4},
                 {'indices': (6, 3, 0, 4), 'normals': (5, 5, 5, 5), 'material': 5})

        cube_object = GLObject()
        cube_object.set_data(vertices, colors, normals, faces)
        self._glwindow.children.append(cube_object)

        self._rotation_matrix = np.zeros((4, 4))
        self._rotation_matrix[3, 3] = 1.0

        self._sensor_data = None

        self.addDock(self._glwindow)

    def draw(self):
        ''' Apply cube object transformations based on rotation matrix '''

        self._glwindow.transformation.rotation = self._rotation_matrix.copy()
        self._glwindow.draw()

    def update(self, _timestamp, *rvec):
        '''update the cube'''
        self._rotation_matrix[:3, :3] = R.from_rotvec(rvec).as_matrix()


class MainWindow(QtGui.QMainWindow):
    ''' Main pyqtgraph Gui window '''
    refresh_rate = 200

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create Gui Elements
        canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(canvas)

        self.cube = ImuCube3D()
        self.cube.setGeometry(0, 110, 1920, 1080)
        self.cube.show()

        self.frontend = FrontendData(self.cube.update)

        # scatterplots
        plots = []
        self.yplotdata = {'Gyro': [], 'Acc': []}
        x_range = (self.frontend.bufsize * 1e-3, 0)
        y_range = [(-1e2, 1e2), (-1.500, 1.500)]
        for sensor_i, sensor in enumerate(self.yplotdata.keys()):
            plots.append(canvas.addPlot(title=sensor, bottom='Time'))
            for xyz_i in range(3):
                self.yplotdata[sensor].append(plots[-1].plot(pen=ALLCOLORS[xyz_i],
                                                             symbolBrush=ALLBRUSHES[xyz_i],
                                                             symbolPen=None,
                                                             symbolSize=7))

            plots[-1].setRange(QtCore.QRectF(-x_range[0],
                                             y_range[sensor_i][0],
                                             x_range[1] - x_range[0],
                                             y_range[sensor_i][1] - y_range[sensor_i][0]))
            plots[-1].setLimits(xMin=-x_range[0],
                                xMax=x_range[1],
                                yMin=y_range[sensor_i][0],
                                yMax=y_range[sensor_i][1])
            canvas.nextRow()

        # canvas.ci.layout.setRowStretchFactor(1, 1)

        # Start

        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._draw)
        self._drawtimer.start(1000 / self.refresh_rate)

    def _draw(self):
        tdata, pdata = self.frontend.get_data()
        cdata = np.append(np.diff(tdata) < 0.1, False)

        for sensor_i, sensor in enumerate(['Gyro', 'Acc']):
            for ch_i in range(3):
                y_data = pdata[:, sensor_i * 3 + ch_i]
                self.yplotdata[sensor][ch_i].setData(
                    **{'x': tdata, 'y': y_data, 'connect': cdata,
                       'symbol': 'o',
                       # 'pen': None,
                       # 'symbol': None,
                       'pen': ALLCOLORS[ch_i],
                       })
        self.cube.draw()

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()


def main():
    ''' App entrypoint '''
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
