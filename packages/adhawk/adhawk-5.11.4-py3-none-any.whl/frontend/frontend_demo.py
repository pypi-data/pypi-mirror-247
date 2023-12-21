''' Demo data stream '''
import os
import sys
import time

import numpy as np
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

import adhawkapi
import adhawkapi.frontend
import adhawkapi.frontend.internal as internalfrontendapi
from adhawkapi import defaults


N_TRACKERS = 2  # Number of tracker modules
N_PHOTODIODES = 6  # Max number of photodiodes per tracker module


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
    bufsize = 3000

    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self._timers = [OffsetTimer() for _ in range(3)]

        self._et_data = np.zeros((N_TRACKERS, N_PHOTODIODES, 2))  # trackerid, pd_id, x/y
        self._et_data_count = np.zeros((N_TRACKERS, N_PHOTODIODES))
        self.fused_et_data = np.zeros((N_TRACKERS, 2))

        self._et_data_buf = np.zeros((N_TRACKERS, N_PHOTODIODES, self.bufsize, 2))
        self._et_data_tbuf = np.zeros((N_TRACKERS, N_PHOTODIODES, self.bufsize))
        self._et_data_bufptr = np.zeros((N_TRACKERS, N_PHOTODIODES), dtype=int)

        # calibration error
        self._err_data_buf = np.zeros(250)
        self._err_data_tbuf = np.zeros(250)
        self._err_data_bufptr = 0

        self.gaze_data = np.zeros(3)

        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.CALIBRATION_ERROR, self._handle_error_data)
        self._api.register_stream_handler(adhawkapi.PacketType.GLINT, self._handle_et_data)
        self._api.register_stream_handler(adhawkapi.PacketType.FUSE, self._handle_fused_data)
        self._api.start(connect_cb=self._handle_stream_enable)

        self._internalapi = internalfrontendapi.InternalApi()
        self._internalapi.start()

    def _handle_error_data(self, timestamp, error):
        self._err_data_buf[self._err_data_bufptr] = error
        self._err_data_tbuf[self._err_data_bufptr] = timestamp
        self._err_data_bufptr = (self._err_data_bufptr + 1) % 250
        self._timers[2].timestamp = timestamp

    def _handle_fused_data(self, trackerid, _timestamp, xpos, ypos, _partial):
        self.fused_et_data[trackerid] = [xpos, ypos]

    def _handle_et_data(self, trackerid, timestamp, xpos, ypos, pd_id):
        if trackerid < N_TRACKERS and pd_id < N_PHOTODIODES:
            self._et_data[trackerid, pd_id] += [xpos, ypos]
            self._et_data_count[trackerid, pd_id] += 1

            self._et_data_bufptr[trackerid, pd_id] = (self._et_data_bufptr[trackerid, pd_id] + 1) % self.bufsize
            self._et_data_buf[trackerid, pd_id, self._et_data_bufptr[trackerid, pd_id]] = [xpos, ypos]
            self._et_data_tbuf[trackerid, pd_id, self._et_data_bufptr[trackerid, pd_id]] = timestamp
            self._timers[trackerid].timestamp = timestamp

    def _handle_stream_enable(self, error):
        if not error:
            streams = [
                adhawkapi.PacketType.CALIBRATION_ERROR,
                adhawkapi.PacketType.GLINT,
                adhawkapi.PacketType.FUSE
            ]
            for stream in streams:
                self._api.set_stream_control(stream, defaults.DEFAULT_RATE, callback=(lambda *args: None))

    def trigger_recenter(self):
        ''' Send recenter command to backend '''
        print("calibration recenter")
        self._api.recenter_calibration(0, 0, -1, callback=(lambda *args: None))

    def trigger_autotune(self):
        ''' Send autotune command to backend '''
        print("autotune")
        self._api.trigger_autotune(callback=(lambda *args: None))

    def get_et_data(self):
        ''' Get the average of the current eyetracking data buffer '''
        et_data = np.nan_to_num(self._et_data / self._et_data_count[:, :, np.newaxis])
        self._et_data *= 0
        self._et_data_count *= 0
        return et_data

    def get_series_data(self):
        ''' get data time series dictionaries '''
        xdata = []
        ydata = []
        for trackerid in range(N_TRACKERS):
            xdata.append([])
            ydata.append([])
            for pd_id in range(N_PHOTODIODES):
                order = np.concatenate((np.arange(self._et_data_bufptr[trackerid, pd_id], self.bufsize),
                                        np.arange(self._et_data_bufptr[trackerid, pd_id])))[10:-10]
                tdata = self._et_data_tbuf[trackerid, pd_id, order] - self._timers[trackerid].timestamp
                pdata = self._et_data_buf[trackerid, pd_id, order]
                cdata = np.append(np.diff(tdata) < 0.05, False)
                xdata[-1].append({
                    'x': tdata,
                    'y': pdata[:, 0],
                    'connect': cdata
                })
                ydata[-1].append({
                    'x': tdata,
                    'y': pdata[:, 1],
                    'connect': cdata
                })
        return xdata, ydata

    def get_error_data(self):
        ''' get error data time series dictionary '''
        order = np.concatenate((np.arange(self._err_data_bufptr, 250),
                                np.arange(self._err_data_bufptr)))
        tdata = self._err_data_tbuf[order] - self._timers[2].timestamp
        pdata = self._err_data_buf[order]
        cdata = np.append(np.diff(tdata) < 0.1, False)
        return {
            'x': tdata,
            'y': pdata,
            'connect': cdata
        }

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()
        self._internalapi.shutdown()


# Colors for drawing the plots
ALLCOLORS = [QtGui.QColor(255, 255, 255, 255),  # White
             QtGui.QColor(255, 0, 0, 255),      # Red
             QtGui.QColor(255, 128, 0, 255),    # Orange
             QtGui.QColor(230, 255, 0, 255),    # Light Green/Yellow
             QtGui.QColor(0, 255, 0, 255),      # Green
             QtGui.QColor(0, 128, 255, 255),    # Light Blue
             QtGui.QColor(255, 0, 255, 255)]    # Purple

ALLBRUSHES = [pyqtgraph.mkBrush(color) for color in ALLCOLORS]


class MainWindow(QtGui.QMainWindow):
    ''' Main pyqtgraph Gui window '''
    refresh_rate = 30

    def __init__(self, parent=None):
        # we are initializing UI.
        # pylint: disable=too-many-statements
        super().__init__(parent)
        self.frontend = FrontendData()

        # Create Gui Elements
        canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(canvas)

        # buttons
        self.pausebutton = QtGui.QPushButton('Pause')
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(self.pausebutton)
        canvas.addItem(proxy)
        self.pausebutton.clicked.connect(self._pause)

        recenterbutton = QtGui.QPushButton('Recenter')
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(recenterbutton)
        canvas.addItem(proxy)
        recenterbutton.clicked.connect(self.frontend.trigger_recenter)
        canvas.nextRow()

        autotunebutton = QtGui.QPushButton('Autotune')
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(autotunebutton)
        canvas.addItem(proxy)
        autotunebutton.clicked.connect(self.frontend.trigger_autotune)
        canvas.nextRow()

        titles = ['Left Eye', 'Right Eye']
        # scatterplots
        plots = []
        self.scatterdata = []
        self.scatterdata.append([])
        for i in range(N_TRACKERS):
            plots.append(canvas.addPlot(title=titles[i], left='X Position', bottom='Y Position'))
            self.scatterdata[-1].append(plots[-1].plot(symbol='o'))
            plots[-1].setRange(QtCore.QRectF(0, 0, 1, 1))
            plots[-1].setLimits(xMin=0, xMax=1, yMin=0, yMax=1)
        # fused plots
        self.scatterdata.append([])
        for i in range(N_TRACKERS):
            self.scatterdata[-1].append(plots[i].plot(symbol='o', symbolBrush=ALLBRUSHES[0]))
        canvas.nextRow()

        # x plots
        self.xplotdata = []
        for i in range(N_TRACKERS):
            self.xplotdata.append([])
            plots.append(canvas.addPlot(title=titles[i] + ' X', bottom='Time'))
            for j in range(N_PHOTODIODES):
                self.xplotdata[-1].append(plots[-1].plot(pen=ALLCOLORS[j + 1], symbolBrush=ALLBRUSHES[j + 1],
                                                         symbolPen=None, symbolSize=7))
            plots[-1].setRange(QtCore.QRectF(-3, 0, 3, 1))
            plots[-1].setLimits(xMin=-3, xMax=0, yMin=0, yMax=1)
        canvas.nextRow()

        # y plots
        self.yplotdata = []
        for i in range(N_TRACKERS):
            self.yplotdata.append([])
            plots.append(canvas.addPlot(title=titles[i] + ' Y', bottom='Time'))
            for j in range(N_PHOTODIODES):
                self.yplotdata[-1].append(plots[-1].plot(pen=ALLCOLORS[j + 1], symbolBrush=ALLBRUSHES[j + 1],
                                                         symbolPen=None, symbolSize=7))
            plots[-1].setRange(QtCore.QRectF(-3, 0, 3, 1))
            plots[-1].setLimits(xMin=-3, xMax=0, yMin=0, yMax=1)
        canvas.nextRow()

        plots.append(canvas.addPlot(title='Model Error', colspan=2, bottom='Time'))
        self.eplotdata = plots[-1].plot()
        plots[-1].setRange(QtCore.QRectF(-3, 0, 3, 0.1))
        plots[-1].setLimits(xMin=-3, xMax=0, yMin=0, yMax=0.1)

        canvas.ci.layout.setRowStretchFactor(0, 0)
        canvas.ci.layout.setRowStretchFactor(1, 0)
        canvas.ci.layout.setRowStretchFactor(2, 4)
        canvas.ci.layout.setRowStretchFactor(3, 2)
        canvas.ci.layout.setRowStretchFactor(4, 2)
        canvas.ci.layout.setRowStretchFactor(5, 1)

        # Start
        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._draw)
        self._drawtimer.start(1000 / self.refresh_rate)

    def _pause(self):
        if self._drawtimer.isActive():
            self._drawtimer.stop()
            self._draw(dots=True)
            self.pausebutton.setText("Resume")
        else:
            self._drawtimer.start()
            self.pausebutton.setText("Pause")

    def _draw(self, dots=False):
        et_data = self.frontend.get_et_data()
        x_data, y_data = self.frontend.get_series_data()
        for trid in range(N_TRACKERS):
            self.scatterdata[0][1 - trid].setData(
                x=et_data[trid, :, 0],
                y=et_data[trid, :, 1],
                connect=np.zeros(N_PHOTODIODES, bool),
                symbol='o',
                symbolBrush=[ALLBRUSHES[i + 1] for i in range(N_PHOTODIODES)]
            )
            self.scatterdata[1][1 - trid].setData(
                x=[self.frontend.fused_et_data[trid, 0]],
                y=[self.frontend.fused_et_data[trid, 1]]
            )
            for pd_id in range(N_PHOTODIODES):

                if dots:
                    x_data[trid][pd_id].update(symbol='o', pen=None)
                    y_data[trid][pd_id].update(symbol='o', pen=None)
                else:
                    x_data[trid][pd_id].update(symbol=None, pen=ALLCOLORS[pd_id + 1])
                    y_data[trid][pd_id].update(symbol=None, pen=ALLCOLORS[pd_id + 1])
                self.xplotdata[1 - trid][pd_id].setData(**x_data[trid][pd_id])
                self.yplotdata[1 - trid][pd_id].setData(**y_data[trid][pd_id])
        self.eplotdata.setData(**self.frontend.get_error_data())

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()


def main():
    ''' App entrypoint '''
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
