''' Diagnostic data viewer for AdHawk Backend

Requirements:
- Windows 10
- Python 3.6+
- Additional python packages: numpy PyQt5 pyqtgraph
  e.g. python -m pip install numpy PyQt5 pyqtgraph

Instructions:
- Run adhawkbackend.exe
- Run the application
  e.g python frontend_diag.py
- The tracking dots should appear on the plot. Each color represents a different detector.
- Click AutoTune button to search for a new coarse position.
- All the data displayed on the plot is outputted to logs/data_{timestamp}.csv

'''

import csv
import datetime
import os
import sys

import numpy as np
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

import adhawkapi
import adhawkapi.frontend


N_TRACKERS = 2  # Number of tracker modules
N_PHOTODIODES = 6  # Max number of photodiodes per tracker module


class FrontendData:
    ''' Handle the data aggregation from backend '''
    bufduration = 0.1  # glint buffer duration in seconds
    pulsebufsize = 120

    def __init__(self):
        datesuffix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        os.makedirs('logs', exist_ok=True)
        self._file = open(f'logs/data_{datesuffix}.csv', 'w', newline='')
        self._csvwriter = csv.writer(self._file, delimiter=',')
        self._csvwriter.writerow(['timestamp', 'tracker id', 'photodiode id', 'x', 'y'])

        self._et_data = np.zeros((N_TRACKERS, N_PHOTODIODES, 2))  # trackerid, pd_id, x/y
        self._et_data_count = np.zeros((N_TRACKERS, N_PHOTODIODES))
        self.fused_et_data = np.zeros((N_TRACKERS, 2))
        self.pupil_data = np.zeros((N_TRACKERS, 5))
        self.pulse_data = np.zeros((N_TRACKERS, 2, self.pulsebufsize))
        self.pulse_data_counter = np.zeros(N_TRACKERS, dtype=int)

        self.gaze_data = np.zeros(3)

        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.GLINT, self._handle_et_data)
        self._api.register_stream_handler(adhawkapi.PacketType.PULSE, self._handle_pulse_data)
        self._api.register_stream_handler(adhawkapi.PacketType.FUSE, self._handle_fused_data)
        self._api.register_stream_handler(adhawkapi.PacketType.PUPIL_ELLIPSE, self._handle_pupil_data)
        self._api.register_stream_handler(adhawkapi.PacketType.GAZE, self._handle_extended_gaze_data)
        self._api.start(connect_cb=self._handle_connect)

    def trigger_autotune(self):
        ''' Send autotune command to backend '''
        print("autotune")
        self._api.trigger_autotune(callback=(lambda *args: None))

    def _handle_fused_data(self, trackerid, _timestamp, xpos, ypos, _partial):
        self.fused_et_data[trackerid] = [xpos, ypos]

    def _handle_et_data(self, trackerid, timestamp, xpos, ypos, pd_id):
        if trackerid < N_TRACKERS and pd_id < N_PHOTODIODES:
            self._et_data[trackerid, pd_id] += [xpos, ypos]
            self._et_data_count[trackerid, pd_id] += 1
            self._csvwriter.writerow([timestamp, trackerid, pd_id, xpos, ypos])

    def _handle_pupil_data(self, trackerid, _timestamp, xpos, ypos, semimajor, semiminor, theta):
        if trackerid > 1:
            trackerid -= 2
        self.pupil_data[trackerid] = [xpos, ypos, semimajor, semiminor, theta]

    def _handle_pulse_data(self, trackerid, _timestamp, xphase1, xphase2, yphase1, yphase2, _pd_id):
        for xphase, yphase in ((xphase1, yphase1), (xphase2, yphase2)):
            self.pulse_data[trackerid, 0, self.pulse_data_counter[trackerid]] = np.cos(xphase)
            self.pulse_data[trackerid, 1, self.pulse_data_counter[trackerid]] = np.cos(yphase)
            self.pulse_data_counter[trackerid] = (self.pulse_data_counter[trackerid] + 1) % self.pulsebufsize

    def _handle_extended_gaze_data(self, _timestamp, xpos, ypos, zpos, _vergence):
        self.gaze_data[:] = xpos, ypos, zpos

    def _handle_gaze_data(self, xpos, ypos, zpos):
        self.gaze_data[:] = xpos, ypos, zpos

    def get_et_data(self):
        ''' Get the average of the current eyetracking data buffer '''
        et_data = np.nan_to_num(self._et_data / self._et_data_count[:, :, np.newaxis])
        self._et_data *= 0
        self._et_data_count *= 0
        return et_data

    def _handle_connect(self, error):
        if not error:
            streams = [
                adhawkapi.PacketType.GAZE,
                adhawkapi.PacketType.FUSE,
                adhawkapi.PacketType.GLINT,
                adhawkapi.PacketType.PUPIL_ELLIPSE
            ]
            for stream in streams:
                self._api.set_stream_control(stream, 120, callback=(lambda *args: None))

            self._api.set_stream_control(
                adhawkapi.PacketType.PULSE, 250, callback=(lambda *args: None))

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()
        self._file.close()


# Brushes for drawing the dots
ALLBRUSHES = [pyqtgraph.mkBrush(QtGui.QColor(255, 255, 255, 255)),  # White
              pyqtgraph.mkBrush(QtGui.QColor(255, 0, 0, 255)),      # Red
              pyqtgraph.mkBrush(QtGui.QColor(255, 128, 0, 255)),    # Orange
              pyqtgraph.mkBrush(QtGui.QColor(230, 255, 0, 255)),    # Light Green/Yellow
              pyqtgraph.mkBrush(QtGui.QColor(0, 255, 0, 255)),      # Green
              pyqtgraph.mkBrush(QtGui.QColor(0, 128, 255, 255)),    # Light Blue
              pyqtgraph.mkBrush(QtGui.QColor(255, 0, 255, 255))]    # Purple


class MainWindow(QtGui.QMainWindow):
    ''' Main pyqtgraph Gui window '''
    refresh_rate = 60
    angles = np.linspace(0, 2 * np.pi, 100)
    circle_points = np.array([np.cos(angles), np.sin(angles)])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frontend = FrontendData()

        # Create Gui Elements
        canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(canvas)

        autotunebutton = QtGui.QPushButton('AutoTune')
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(autotunebutton)
        canvas.addItem(proxy)
        canvas.nextRow()
        autotunebutton.clicked.connect(self.frontend.trigger_autotune)

        titles = ['Left Eye', 'Right Eye']
        # scatterplots
        plots = []
        self.plotdatas = []
        for i in range(N_TRACKERS):
            # glints
            plots.append(canvas.addPlot(title=titles[i]))
            self.plotdatas.append(plots[-1].plot(symbol='o'))
            plots[-1].setRange(QtCore.QRectF(-1, -1, 2, 2))
            plots[-1].setLimits(xMin=-1, xMax=1, yMin=-1, yMax=1)
        for i in range(N_TRACKERS):
            # fuse
            self.plotdatas.append(plots[i].plot(symbol='o', symbolBrush=ALLBRUSHES[0]))
        for i in range(N_TRACKERS):
            # pupil
            self.plotdatas.append(plots[i].plot())
        for i in range(N_TRACKERS):
            # pulses
            self.plotdatas.append(plots[i].plot(symbol='o', symbolBrush=ALLBRUSHES[0], symbolSize=3))
        canvas.nextRow()

        plots.append(canvas.addPlot(title='Gaze'))
        self.plotdatas.append(plots[-1].plot(symbol='o'))
        plots[-1].setRange(QtCore.QRectF(-1, -1, 2, 2))
        plots[-1].setLimits(xMin=-1, xMax=1, yMin=-1, yMax=1)

        # Start
        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._draw)
        self._drawtimer.start(1000 / self.refresh_rate)

    def _draw(self):
        et_data = self.frontend.get_et_data()
        for trid in range(N_TRACKERS):
            self.plotdatas[1 - trid].setData(
                x=et_data[trid, :, 0],
                y=et_data[trid, :, 1],
                connect=np.zeros(N_PHOTODIODES, bool),
                symbol='o',
                symbolBrush=[ALLBRUSHES[i + 1] for i in range(N_PHOTODIODES)]
            )
            self.plotdatas[1 - trid + N_TRACKERS].setData(
                x=[self.frontend.fused_et_data[trid, 0]],
                y=[self.frontend.fused_et_data[trid, 1]]
            )
            xpos, ypos, semimajor, semiminor, theta = self.frontend.pupil_data[trid]
            rotmat = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
            ellipse_data = [[xpos], [ypos]] + rotmat @ ([[semimajor], [semiminor]] * self.circle_points)
            self.plotdatas[1 - trid + 2 * N_TRACKERS].setData(
                x=ellipse_data[0],
                y=ellipse_data[1]
            )
            self.plotdatas[1 - trid + 3 * N_TRACKERS].setData(
                x=self.frontend.pulse_data[trid, 0],
                y=self.frontend.pulse_data[trid, 1],
                connect=np.zeros(self.frontend.pulsebufsize, bool)
            )
        self.plotdatas[-1].setData(
            x=[self.frontend.gaze_data[0]],
            y=[self.frontend.gaze_data[1]],
            connect=np.zeros(1, bool),
            symbol='o',
            symbolBrush=[ALLBRUSHES[0]]
        )

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()


def main():
    ''' App entrypoint '''
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
