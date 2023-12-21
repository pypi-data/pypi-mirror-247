''' Demo eye gaze '''
import argparse
import enum
import os
import sys
import time

import numpy as np
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

import adhawkapi
import adhawkapi.frontend


N_TRACKERS = 2  # Number of tracker modules


class WhatToShow(enum.IntEnum):
    '''select what should be shown in the timeline plot'''
    ERROR = 0
    VERGENCE = 1


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


def angles2vector(angles):
    ''' given [yaw, pitch] in yx euler angles, return a direction vector '''
    return np.array((np.sin(angles[0]),
                     np.cos(angles[0]) * np.sin(angles[1]),
                     -np.cos(angles[0]) * np.cos(angles[1])))


def vector2angles(vector):
    ''' given a direction vector, return [yaw, pitch] in yx euler angles '''
    return np.array((np.arctan2(vector[0], np.sqrt(vector[1] ** 2 + vector[2] ** 2)),
                     np.arctan2(vector[1], -vector[2])))


class FrontendData:
    ''' Handle the data aggregation from backend '''
    bufsize = 250
    smoothing_n = 5

    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self._timer = OffsetTimer()

        self._gaze_data_buf = np.zeros((self.bufsize, 4))  # x,y,z,vergence
        self._gaze_data_buf_filtered = np.zeros((self.bufsize, 4))  # x,y,z,vergence
        self._gaze_data_tbuf = np.zeros(self.bufsize)
        self._gaze_data_bufptr = 0

        # calibration error
        self._err_data_buf = np.zeros(self.bufsize)
        self._err_data_buf_filtered = np.zeros(self.bufsize)
        self._err_data_tbuf = np.zeros(self.bufsize)
        self._err_data_bufptr = 0

        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.CALIBRATION_ERROR, self._handle_error_data)
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE, self._handle_gaze_data)
        self._api.start(connect_cb=self._handle_connect)

    def _handle_error_data(self, timestamp, error):
        self._err_data_buf[self._err_data_bufptr] = error
        order = np.concatenate((np.arange(self._err_data_bufptr, self.bufsize),
                                np.arange(self._err_data_bufptr)))
        self._err_data_buf_filtered[self._err_data_bufptr] = np.nanmedian(
            self._err_data_buf[order][-self.smoothing_n::], axis=0)
        self._err_data_tbuf[self._err_data_bufptr] = timestamp
        self._err_data_bufptr = (self._err_data_bufptr + 1) % self.bufsize

    def _handle_gaze_data(self, _timestamp, vec_x, vec_y, vec_z, vergence):
        self._gaze_data_buf[self._gaze_data_bufptr] = [vec_x, vec_y, vec_z, vergence]
        order = np.concatenate((np.arange(self._gaze_data_bufptr, self.bufsize),
                                np.arange(self._gaze_data_bufptr)))
        self._gaze_data_buf_filtered[self._gaze_data_bufptr] = np.nanmedian(
            self._gaze_data_buf[order][-self.smoothing_n::], axis=0)
        self._gaze_data_tbuf[self._gaze_data_bufptr] = _timestamp
        self._gaze_data_bufptr = (self._gaze_data_bufptr + 1) % self.bufsize
        self._timer.timestamp = _timestamp

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.GAZE, 120, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.CALIBRATION_ERROR, 120, callback=(lambda *args: None))

    def trigger_recenter(self):
        ''' Send recenter command to backend '''
        print("calibration recenter")
        self._api.recenter_calibration(0, 0, -1, callback=(lambda *args: None))

    def get_gaze_angles(self, view):
        ''' get gaze angles per eye from top or front view '''
        gaze_angles = np.zeros((N_TRACKERS, 2))
        order = np.concatenate((np.arange(self._gaze_data_bufptr, self.bufsize),
                                np.arange(self._gaze_data_bufptr)))
        pdata = self._gaze_data_buf_filtered[order]
        gaze = pdata[-1, 0:3]
        if view == 0:
            gaze = np.array([gaze[0], gaze[2], -gaze[1]])
        vergence = pdata[-1, 3]
        avg_angles = vector2angles(gaze)
        gaze_angles[:, 1] = avg_angles[1]
        gaze_angles[0, 0] = avg_angles[0] - vergence * 0.5
        gaze_angles[1, 0] = avg_angles[0] + vergence * 0.5
        return gaze_angles

    def get_error_data(self):
        ''' get error data time series dictionary '''
        order = np.concatenate((np.arange(self._err_data_bufptr, self.bufsize),
                                np.arange(self._err_data_bufptr)))
        pdata = self._err_data_buf_filtered[order]
        tdata = self._err_data_tbuf[order] - self._timer.timestamp
        cdata = np.append(np.diff(tdata) < 0.1, False)
        return {
            'x': tdata,
            'y': pdata,
            'connect': cdata
        }

    def get_vergence_data(self):
        ''' get vergece data time series dictionary '''
        order = np.concatenate((np.arange(self._gaze_data_bufptr, self.bufsize),
                                np.arange(self._gaze_data_bufptr)))
        pdata = np.degrees(self._gaze_data_buf_filtered[order][:, 3])  # pylint: disable=assignment-from-no-return
        tdata = self._gaze_data_tbuf[order] - self._timer.timestamp
        cdata = np.append(np.diff(tdata) < 0.1, False)
        return {
            'x': tdata,
            'y': pdata,
            'connect': cdata
        }

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()


# Colors for drawing the plots
ALLCOLORS = [QtGui.QColor(255, 255, 255, 255),  # White
             QtGui.QColor(255, 0, 0, 255),  # Red
             QtGui.QColor(255, 128, 0, 255),  # Orange
             QtGui.QColor(230, 255, 0, 255),  # Light Green/Yellow
             QtGui.QColor(0, 255, 0, 255),  # Green
             QtGui.QColor(0, 128, 255, 255),  # Light Blue
             QtGui.QColor(255, 0, 255, 255)]  # Purple
ALLBRUSHES = [pyqtgraph.mkBrush(color) for color in ALLCOLORS]
CIRCLE_POINTS = [
    np.cos(np.linspace(0, 2 * np.pi, 100)),
    np.sin(np.linspace(0, 2 * np.pi, 100))
]
EYE_RADIUS = 12
IPD = 64.0
PUPIL_OFFSET = 8.7
CORNEA_RADIUS = 7.8
CORNEA_OFFSET = 5.7
IRIS_OFFSET = (CORNEA_OFFSET ** 2 + EYE_RADIUS ** 2 - CORNEA_RADIUS ** 2) / (2 * CORNEA_OFFSET)
IRIS_RADIUS = np.sqrt(EYE_RADIUS ** 2 - IRIS_OFFSET ** 2)
PUPIL_RADIUS = 3.0


def offset_circle(radius, normal, offset):
    ''' return points corresponding to a offset circle with a surface normal '''
    face_angle = np.arctan2(normal[1], normal[0])
    stretch = np.diag([normal[2], 1])
    rot = np.array([[np.cos(face_angle), -np.sin(face_angle)],
                    [np.sin(face_angle), np.cos(face_angle)]])
    trans = rot @ stretch @ rot.T
    transpoints = trans @ CIRCLE_POINTS
    return transpoints * radius + normal[0:2, np.newaxis] * offset


class MainWindow(QtGui.QMainWindow):  # pylint: disable=too-few-public-methods
    ''' Main pyqtgraph Gui window '''
    refresh_rate = 30
    what_to_show = WhatToShow.VERGENCE

    def __init__(self, parent=None, show_error=False):
        super().__init__(parent)
        self.frontend = FrontendData()
        if show_error:
            self.what_to_show = WhatToShow.ERROR
        # Create Gui Elements
        canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(canvas)

        # button
        recenterbutton = QtGui.QPushButton('Recenter')
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(recenterbutton)
        canvas.addItem(proxy)
        recenterbutton.clicked.connect(self.frontend.trigger_recenter)
        canvas.nextRow()

        # scatterplots
        plots = []
        self.irisdatas = [[], []]
        self.pupildatas = [[], []]
        titles = ['Top View', 'Front View']
        for view in range(2):
            plots.append(canvas.addPlot(title=titles[view]))
            plots[-1].plot(x=CIRCLE_POINTS[0] * EYE_RADIUS - IPD / 2,
                           y=CIRCLE_POINTS[1] * EYE_RADIUS)
            plots[-1].plot(x=CIRCLE_POINTS[0] * EYE_RADIUS + IPD / 2,
                           y=CIRCLE_POINTS[1] * EYE_RADIUS)
            for _eye in range(N_TRACKERS):
                self.irisdatas[view].append(plots[-1].plot())
                self.pupildatas[view].append(plots[-1].plot())
            plots[-1].setAspectLocked()
            plots[-1].setMouseEnabled(False, False)
            canvas.nextRow()

        if self.what_to_show == WhatToShow.ERROR:
            plots.append(canvas.addPlot(title='Model Error', bottom='Time'))
            plots[-1].setRange(QtCore.QRectF(-3, 0, 3, 0.1))
            plots[-1].setLimits(xMin=-3, xMax=0, yMin=0, yMax=0.1)
        else:
            plots.append(canvas.addPlot(title='Vergence angle [deg]', bottom='Time'))
            plots[-1].setRange(QtCore.QRectF(-3, 0, 3, 40))
            plots[-1].setLimits(xMin=-3, xMax=0, yMin=0, yMax=40)

        self.eplotdata = plots[-1].plot()

        canvas.ci.layout.setRowStretchFactor(1, 4)
        canvas.ci.layout.setRowStretchFactor(2, 4)
        canvas.ci.layout.setRowStretchFactor(3, 1)

        # Start
        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._draw)
        self._drawtimer.start(1000 / self.refresh_rate)

    def _draw(self):
        offsets = [IPD / 2, -IPD / 2]
        for view in range(2):
            gaze_angles = self.frontend.get_gaze_angles(view)
            for eye in range(2):
                normal = angles2vector(gaze_angles[eye])
                xlist, ylist = offset_circle(IRIS_RADIUS, normal, IRIS_OFFSET)
                self.irisdatas[view][eye].setData(x=xlist + offsets[eye], y=ylist)
                xlist, ylist = offset_circle(PUPIL_RADIUS, normal, PUPIL_OFFSET)
                self.pupildatas[view][eye].setData(x=xlist + offsets[eye], y=ylist)
        if self.what_to_show == WhatToShow.ERROR:
            self.eplotdata.setData(**self.frontend.get_error_data())
        else:
            self.eplotdata.setData(**self.frontend.get_vergence_data())

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()


def main():
    ''' App entrypoint '''
    parser = argparse.ArgumentParser(description='Show eye rotations and vergence/error outputs')
    parser.add_argument('--error', default=False, action='store_true')

    args = parser.parse_args(sys.argv[2:])

    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow(show_error=args.error)
    mainwindow.show()
    sys.exit(app.exec_())
