'''
A demo frontend that does realtime saccade detection and reports some realtime eye movement statistics

'''

import argparse
import collections
import datetime
import math
import os
import pathlib
import pickle
import sys
import time

import numpy as np
import pandas as pd
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from scipy import signal
from scipy.spatial.transform import Rotation as R

import adhawkapi
import adhawkapi.frontend
from adhawkapi import errormsg

GAZE_RATE = 500
IMU_RATE = 100
LOGS_PATH = os.path.join('logs', 'frontend saccade')

# Colors for drawing the plots
ALLCOLORS = [QtGui.QColor(255, 255, 255, 255),  # White
             QtGui.QColor(255, 0, 0, 255),  # Red
             QtGui.QColor(255, 128, 0, 255),  # Orange
             QtGui.QColor(230, 255, 0, 255),  # Light Green/Yellow
             QtGui.QColor(0, 255, 0, 255),  # Green
             QtGui.QColor(0, 128, 255, 255),  # Light Blue
             QtGui.QColor(255, 0, 255, 255)]  # Purple

ALLBRUSHES = [pyqtgraph.mkBrush(color) for color in ALLCOLORS]


class AlignDelegate(QtGui.QItemDelegate):
    ''' Set the alignment for the Qtable '''

    def paint(self, painter, option, index):
        ''' Cverride the paint function '''
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtGui.QItemDelegate.paint(self, painter, option, index)


def overlap(start1, end1, start2, end2):
    """Does the range (start1, end1) overlap with (start2, end2)?"""
    return end1 >= start2 and end2 >= start1


def vector2angles(vector):
    ''' given a direction vector, return [yaw, pitch] in yx euler angles '''
    return np.array((np.arctan2(vector[0], np.sqrt(vector[1] ** 2 + vector[2] ** 2)),
                     np.arctan2(vector[1], -vector[2])))


class EventDetector:
    """ class for real-time eye movement event detection"""
    # pylint: disable=too-many-instance-attributes
    # we need to buffer the samples to be able to go back in time to detect the onset of some of the events
    _buffer_size = 700  # samples
    _savgol_window = 21

    # saccade detection
    _peak_velocity_threshold = 10
    _acc_threshold = 500
    _peak_velocity_threshold_high = 100
    _acc_threshold_high = 1000
    # minimum accepted interval between saccades
    _min_saccade_distance = 0.06  # second
    _max_saccade_duration = 0.4  # second
    _min_saccade_duration = 0.02  # second
    _min_saccade_mag = 0.3  # deg

    # smooth pursuit
    _min_sp_duration = 0.4  # second
    _sp_mean_win = 100  # samples
    _sp_peak_velocity_threshold = 15

    _imu_vel_threshold = 5  # deg/s
    _min_vor_duration = 0.5  # sec

    # combining per-eye events
    _max_per_eye_saccade_offset = 0.1  # seconds. maximum acceptable delay between the left and right saccade events
    _max_per_eye_sp_offset = 0.1  # seconds. maximum acceptable delay between the left and right saccade events

    def __init__(self, new_event_cb, debug_mode, raw_input=True):
        self._n_eyes = 2

        self._new_event_cb = new_event_cb
        self._debug_mode = debug_mode
        self._raw_input = raw_input
        if debug_mode:
            pathlib.Path(LOGS_PATH).mkdir(parents=True, exist_ok=True)

        # stage one buffer to compensate for the filter delay
        self._buffer_timestamp_lag = [collections.deque(maxlen=self._savgol_window),
                                      collections.deque(maxlen=self._savgol_window)]
        self._buffer_gaze_x_lag = [collections.deque(maxlen=self._savgol_window),
                                   collections.deque(maxlen=self._savgol_window)]
        self._buffer_gaze_y_lag = [collections.deque(maxlen=self._savgol_window),
                                   collections.deque(maxlen=self._savgol_window)]

        self._buffer_imu_timestamp_lag = collections.deque(maxlen=self._savgol_window)
        self._buffer_imu_ang_y_lag = collections.deque(maxlen=self._savgol_window)
        self._buffer_imu_ang_z_lag = collections.deque(maxlen=self._savgol_window)

        # main buffers
        self._buffer_timestamp = [collections.deque(maxlen=self._buffer_size),
                                  collections.deque(maxlen=self._buffer_size)]
        self._buffer_gaze_x = [collections.deque(maxlen=self._buffer_size),
                               collections.deque(maxlen=self._buffer_size)]
        self._buffer_gaze_y = [collections.deque(maxlen=self._buffer_size),
                               collections.deque(maxlen=self._buffer_size)]
        self._buffer_speed = [collections.deque(maxlen=self._buffer_size),
                              collections.deque(maxlen=self._buffer_size)]
        self._buffer_acc = [collections.deque(maxlen=self._buffer_size),
                            collections.deque(maxlen=self._buffer_size)]
        self._buffer_imu_timestamp = collections.deque(maxlen=100)
        self._buffer_imu_ang_y = collections.deque(maxlen=100)
        self._buffer_imu_ang_z = collections.deque(maxlen=100)
        self._buffer_imu_speed = collections.deque(maxlen=100)

        # saccade
        self._above_threshold_counter = np.zeros(self._n_eyes)
        self._last_saccade_offset = np.zeros(self._n_eyes)
        self._last_saccade_onset = np.zeros(self._n_eyes)
        self._temp_saccade_peak_vel = np.zeros(self._n_eyes)
        self._last_saccade_peak_vel = np.zeros(self._n_eyes)
        self._last_sp_onset = np.zeros(self._n_eyes)
        self._last_vor_onset = 0
        self._last_blink = [0, 0]
        self._last_eyeclosed = [0, 0]

        self._last_saccade_ends = np.zeros((2, 2))  # per-eye (timestamp, duration)
        self._last_sp_ends = np.zeros((2, 2))  # per-eye (timestamp, duration)

        self.debug_raw_data = []

    def update_gaze(self, timestamp, gaze_input):
        """handle new gaze sample, calculate velocity"""

        for trackerid in range(self._n_eyes):
            if self._raw_input:
                gaze_x, gaze_y = np.degrees(vector2angles(gaze_input[trackerid]))
            else:
                gaze_x, gaze_y = gaze_input[trackerid]
            self._buffer_timestamp_lag[trackerid].append(timestamp)
            self._buffer_gaze_x_lag[trackerid].append(gaze_x)
            self._buffer_gaze_y_lag[trackerid].append(gaze_y)

            if len(self._buffer_timestamp_lag[trackerid]) < self._savgol_window:
                continue

            # calculate speed to determine the saccade candidates
            savgol_coefs = signal.savgol_coeffs(window_length=self._savgol_window, polyorder=1, deriv=1,
                                                delta=1 / GAZE_RATE)
            derivx = savgol_coefs @ np.array(self._buffer_gaze_x_lag[trackerid])
            derivy = savgol_coefs @ np.array(self._buffer_gaze_y_lag[trackerid])
            speed = np.sqrt(derivx ** 2 + derivy ** 2)
            savgol_coefs = signal.savgol_coeffs(window_length=self._savgol_window, polyorder=2, deriv=2,
                                                delta=1 / GAZE_RATE)
            derivx = savgol_coefs @ np.array(self._buffer_gaze_x_lag[trackerid])
            derivy = savgol_coefs @ np.array(self._buffer_gaze_y_lag[trackerid])
            acc = np.sqrt(derivx ** 2 + derivy ** 2)

            self._buffer_timestamp[trackerid].append(
                self._buffer_timestamp_lag[trackerid][int(self._savgol_window / 2)])
            self._buffer_gaze_x[trackerid].append(self._buffer_gaze_x_lag[trackerid][int(self._savgol_window / 2)])
            self._buffer_gaze_y[trackerid].append(self._buffer_gaze_y_lag[trackerid][int(self._savgol_window / 2)])
            self._buffer_speed[trackerid].append(speed)
            self._buffer_acc[trackerid].append(acc)
            self._check_saccade(trackerid)

            if len(self._buffer_timestamp[trackerid]) == self._buffer_size:
                self.add_to_debug_log(['Gaze',
                                       trackerid,
                                       self._buffer_timestamp[trackerid][-1],
                                       self._buffer_gaze_x[trackerid][-1],
                                       self._buffer_gaze_y[trackerid][-1],
                                       self._buffer_speed[trackerid][-1],
                                       self._buffer_acc[trackerid][-1],
                                       ])

    def update_imu(self, timestamp, _ang_x, ang_y, ang_z):
        ''' Handle new imu sample and detect the VOR '''
        self._buffer_imu_timestamp_lag.append(timestamp)
        self._buffer_imu_ang_y_lag.append(ang_y)
        self._buffer_imu_ang_z_lag.append(ang_z)

        if len(self._buffer_imu_timestamp_lag) < self._savgol_window:
            return

        savgol_coefs = signal.savgol_coeffs(window_length=self._savgol_window, polyorder=1, deriv=1, delta=1 / IMU_RATE)
        derivy = savgol_coefs @ np.array(self._buffer_imu_ang_y_lag)
        derivz = savgol_coefs @ np.array(self._buffer_imu_ang_z_lag)
        speed = np.degrees(np.sqrt(derivy ** 2 + derivz ** 2))

        self._buffer_imu_timestamp.append(self._buffer_imu_timestamp_lag[int(self._savgol_window / 2)])
        self._buffer_imu_ang_y.append(self._buffer_imu_ang_y_lag[int(self._savgol_window / 2)])
        self._buffer_imu_ang_z.append(self._buffer_imu_ang_z_lag[int(self._savgol_window / 2)])
        self._buffer_imu_speed.append(speed)

        if len(self._buffer_imu_timestamp) == self._buffer_imu_timestamp.maxlen:
            self.add_to_debug_log(['IMU',
                                   self._buffer_imu_timestamp[-1],
                                   self._buffer_imu_ang_y[-1],
                                   self._buffer_imu_ang_z[-1],
                                   self._buffer_imu_speed[-1],
                                   ])

        vor = self._buffer_imu_speed[-1] > self._imu_vel_threshold
        if self._last_vor_onset and not vor:
            offset_timestamp = self._buffer_timestamp[0][-1]
            duration = offset_timestamp - self._last_vor_onset

            if duration > self._min_vor_duration:
                self.add_to_debug_log(['VOR', offset_timestamp, duration])
                self._new_event_cb('VOR', offset_timestamp, offset_timestamp - self._last_vor_onset)
                # reset the sp
                self._last_sp_onset[0] = 0
                self._last_sp_onset[1] = 0
            self._last_vor_onset = 0

        elif not self._last_vor_onset and vor and self._buffer_timestamp[0]:
            # start of vor
            self._last_vor_onset = self._buffer_timestamp[0][-1]

    def update_blink(self, event_type, timestamp, *args):
        ''' Handle the new blink events '''
        if event_type == adhawkapi.Events.BLINK:
            self._last_blink = (timestamp, args[0])
            self._last_saccade_ends = np.zeros((2, 2))
            self.add_to_debug_log(['Blink', timestamp, args[0]])
        elif event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            self._last_eyeclosed[eye_idx] = timestamp
            self.add_to_debug_log(['EyeClosed', args[0], timestamp])

    def add_to_debug_log(self, line):
        ''' Add a new line to the debug log '''
        if self._debug_mode:
            self.debug_raw_data.append(line)

    def get_gaze_at_timestamp(self, eye, timestamp):
        ''' Return the gaze sample belonging to a given timestamp '''
        ind = np.argmax(np.array(self._buffer_timestamp[eye]) > timestamp)
        return self._buffer_gaze_x[eye][ind], self._buffer_gaze_y[eye][ind]

    def _handle_saccade_event(self, trackerid, timestamp=0, duration=0):
        self._last_saccade_ends[trackerid, :] = [timestamp, duration]

        # to stay on the safe side ignore the saccade that overlaps with the last blink
        range1 = (min(self._last_saccade_ends[0, 0] - self._last_saccade_ends[0, 1],
                      self._last_saccade_ends[1, 0] - self._last_saccade_ends[1, 1]),
                  max(self._last_saccade_ends[0, 0], self._last_saccade_ends[1, 0]))
        range2 = (self._last_blink[0] - self._last_blink[1],
                  self._last_blink[0])
        if (0 not in range1) and (0 not in range2) and overlap(*range1, *range2):
            self._last_saccade_ends = np.zeros((2, 2))
            return

        if abs(self._last_saccade_ends[0, 0] - self._last_saccade_ends[1, 0]) < self._max_per_eye_saccade_offset:
            offset = (self._last_saccade_ends[0, 0] + self._last_saccade_ends[1, 0]) / 2
            duration = (self._last_saccade_ends[0, 1] + self._last_saccade_ends[1, 1]) / 2

            gx_onset, gy_onset = self.get_gaze_at_timestamp(0, offset - duration)
            gx_offset, gy_offset = self.get_gaze_at_timestamp(0, offset)
            saccade_magnitude_0 = math.sqrt((gx_onset - gx_offset) ** 2 + (gy_onset - gy_offset) ** 2)
            gx_onset, gy_onset = self.get_gaze_at_timestamp(1, offset - duration)
            gx_offset, gy_offset = self.get_gaze_at_timestamp(1, offset)
            saccade_magnitude_1 = math.sqrt((gx_onset - gx_offset) ** 2 + (gy_onset - gy_offset) ** 2)
            mag = (saccade_magnitude_0 + saccade_magnitude_1) / 2

            # reject small saccades that happen right after a blink (could be made due to noise)
            mag_min = 3  # deg
            temporal_offset = 0.6  # second
            if (mag < mag_min) and (0 < (offset - duration - self._last_blink[0]) < temporal_offset):
                return

            self._new_event_cb('Saccade', offset, duration, mag)
            self.add_to_debug_log(['Saccade', 2, offset, duration])
            self._last_saccade_ends = np.zeros((2, 2))

    def _handle_sp_event(self, trackerid, timestamp=0, duration=0):

        self._last_sp_ends[trackerid, :] = [timestamp, duration]

        if abs(self._last_sp_ends[0, 0] - self._last_sp_ends[1, 0]) < self._max_per_eye_sp_offset:
            offset = (self._last_sp_ends[0, 0] + self._last_sp_ends[1, 0]) / 2
            duration = (self._last_sp_ends[0, 1] + self._last_sp_ends[1, 1]) / 2

            self._new_event_cb('SP', offset, duration)
            self.add_to_debug_log(['SP', 2, offset, duration])
            self._last_sp_ends = np.zeros((2, 2))

    def _check_saccade(self, eye):
        # pylint: disable=too-many-return-statements, too-many-branches, too-many-statements
        current = self._buffer_timestamp[eye][-1]

        # sp
        if len(self._buffer_speed[eye]) > self._sp_mean_win:
            vel_mean = np.mean(np.array(self._buffer_speed[eye])[-self._sp_mean_win::])
            self.add_to_debug_log(['Speed_mean',
                                   eye,
                                   current,
                                   vel_mean
                                   ])
            in_sp = vel_mean > self._sp_peak_velocity_threshold
        else:
            return
        if in_sp and not self._last_sp_onset[eye]:
            self._last_sp_onset[eye] = current
        elif not in_sp and self._last_sp_onset[eye]:
            duration = current - self._last_sp_onset[eye]
            if (duration > self._min_sp_duration) and (not self._last_vor_onset):
                self.add_to_debug_log(['SP', eye, current, duration])
                self._handle_sp_event(eye, current, duration)
            self._last_sp_onset[eye] = 0

        if (in_sp and self._last_sp_onset[eye] and (
                current - self._last_sp_onset[eye]) > self._min_sp_duration) or self._last_vor_onset:
            peak_velocity_threshold = self._peak_velocity_threshold_high
            acc_threshold = self._acc_threshold_high
        else:
            peak_velocity_threshold = max(self._peak_velocity_threshold, vel_mean)
            acc_threshold = self._acc_threshold

        above_threshold = self._buffer_speed[eye][-1] > peak_velocity_threshold

        too_close_to_last_saccade = (self._buffer_timestamp[eye][-1] - self._last_saccade_offset[
            eye]) < self._min_saccade_distance

        if (not too_close_to_last_saccade) and above_threshold and (not self._last_saccade_onset[eye]):
            self._above_threshold_counter[eye] += 1

            if self._above_threshold_counter[eye] < 3:  # make sure there are more than n samples above the threshold
                return

            # wait for peak vel before searching for onset
            if not self._last_saccade_peak_vel[eye]:
                self._detect_peak_vel(eye)
                return
            onset = self._find_saccade_onset(eye, peak_velocity_threshold)
            if onset is None:
                return
            self._last_saccade_onset[eye] = onset

        elif self._last_saccade_onset[eye] and self._last_saccade_peak_vel[eye]:  # find saccade offset

            # this won't happen if it's a real saccade.
            if self._buffer_speed[eye][-1] > self._last_saccade_peak_vel[eye]:
                self._cancel_saccade(eye, 'speed went down and up again after detected peak velocity')
                return
            if self._check_saccade_duration(eye) and \
                    (self._buffer_speed[eye][-1] < ((peak_velocity_threshold + self._last_saccade_peak_vel[eye]) / 2)) \
                    and (self._buffer_acc[eye][-1] < acc_threshold):

                offset_timestamp = self._buffer_timestamp[eye][-1]
                duration = offset_timestamp - self._last_saccade_onset[eye]

                self._last_saccade_onset[eye] = 0
                self._temp_saccade_peak_vel[eye] = 0
                self._last_saccade_peak_vel[eye] = 0
                self._above_threshold_counter[eye] = 0
                # double check and make sure that gaze has moved during the saccade
                xy_onset = self.get_gaze_at_timestamp(eye, self._last_saccade_onset[eye])
                deltax = self._buffer_gaze_x[eye][-1] - xy_onset[0]
                deltay = self._buffer_gaze_y[eye][-1] - xy_onset[1]
                if math.sqrt(deltax ** 2 + deltay ** 2) < self._min_saccade_mag:
                    self._cancel_saccade(eye, 'saccade rejected (no gaze movements)')

                    return

                # reject saccade if it overlaps with a blink
                if (self._last_eyeclosed[eye] < offset_timestamp) and (
                        self._last_eyeclosed[eye] > (offset_timestamp - duration - 0.2)):
                    self._cancel_saccade(eye, 'saccade rejected (blink)')
                    return

                self.add_to_debug_log(['Saccade', eye, offset_timestamp, duration])
                self._handle_saccade_event(eye, offset_timestamp, duration)
                self._last_saccade_offset[eye] = offset_timestamp

        else:
            self._last_saccade_onset[eye] = 0
            self._temp_saccade_peak_vel[eye] = 0
            self._above_threshold_counter[eye] = 0

    def _find_saccade_onset(self, eye, peak_velocity_threshold):
        # go back (100 ms) in time and find the first local velocity minimum when:
        back_dt = 0.2  # ms
        acc_threshold = self._acc_threshold
        if self._last_vor_onset:
            acc_threshold = 5 * self._acc_threshold
        current = self._buffer_timestamp[eye][-1]
        onset = current
        counter = 0
        while current - onset < back_dt:
            counter += 1
            if len(self._buffer_timestamp[eye]) < counter:
                break
            onset = self._buffer_timestamp[eye][-counter]
            if onset <= self._last_saccade_offset[eye]:
                break
            check1 = self._buffer_speed[eye][-counter] < peak_velocity_threshold
            check2 = self._buffer_acc[eye][-counter] < acc_threshold
            # check3 = self._buffer_acc[eye][-counter + 1] >= acc_threshold
            if check1 and check2:
                return onset

        # local min not found
        self._above_threshold_counter[eye] = 0
        return None

    def _detect_peak_vel(self, eye):
        if self._buffer_speed[eye][-1] > self._temp_saccade_peak_vel[eye]:
            self._temp_saccade_peak_vel[eye] = self._buffer_speed[eye][-1]
        else:
            self._last_saccade_peak_vel[eye] = self._temp_saccade_peak_vel[eye]

    def _check_saccade_duration(self, eye):
        """reject very long or very short saccades"""
        offset_timestamp = self._buffer_timestamp[eye][-1]
        duration = offset_timestamp - self._last_saccade_onset[eye]
        if duration < self._min_saccade_duration:
            self._cancel_saccade(eye, 'saccade rejected (too short)')
            return False
        if duration > self._max_saccade_duration:
            self._cancel_saccade(eye, 'saccade rejected (too long)')
            return False
        if duration > 0.15:
            # check the peak velocity for long saccade.
            # this filter can be implemented in a better way by expecting all the saccades to follow a
            #  relationship between their magnitude and peak velocity
            if self._last_saccade_peak_vel[eye] < 100:
                self._cancel_saccade(eye, 'saccade rejected (not following main sequence)')
                return False

        return True

    def _cancel_saccade(self, eye, _reason):
        self._last_saccade_onset[eye] = 0
        self._above_threshold_counter[eye] = 0
        self._temp_saccade_peak_vel[eye] = 0
        self._last_saccade_peak_vel[eye] = 0

    def shutdown(self, postfix):
        ''' Perform any process needed before closing the detector '''
        if self._debug_mode:
            pickle.dump(self.debug_raw_data, open(os.path.join(LOGS_PATH, f'log_data_{postfix}.pkl'), 'wb'),
                        protocol=pickle.HIGHEST_PROTOCOL)


class Frontend:
    ''' Frontend communicating with the backend '''

    def __init__(self,
                 gaze_callback=lambda *_args: None,
                 imu_callback=lambda *_args: None,
                 blink_callback=lambda *_args: None,
                 pupil_callback=lambda *_args: None,
                 ):
        self._gaze_callback = gaze_callback
        self._imu_callback = imu_callback
        self._blink_callback = blink_callback
        self._pupil_callback = pupil_callback
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.TRACKER_STATUS, self._handle_tracker_status)
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)
        self._api.register_stream_handler(adhawkapi.PacketType.PER_EYE_GAZE, self._handle_gaze_data)
        self._api.register_stream_handler(adhawkapi.PacketType.IMU, (lambda *args: None))
        self._api.register_stream_handler(adhawkapi.PacketType.IMU_ROTATION, self._handle_imu_data)
        self._api.register_stream_handler(adhawkapi.PacketType.PUPIL_DIAMETER, self._handle_pupilsize_data)
        self._api.start(connect_cb=self._handle_connect)

    def shutdown(self):
        ''' Shutdown the port '''
        self._api.shutdown()

    def _handle_connect(self, error):
        if not error:
            self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.PER_EYE_GAZE, GAZE_RATE, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.IMU, IMU_RATE, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.IMU_ROTATION, 1, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.PUPIL_DIAMETER, GAZE_RATE, callback=(lambda *args: None))

    @staticmethod
    def _handle_tracker_status(status):
        print(f'tracker status received: {errormsg(status)}')

    def _handle_gaze_data(self, *data):
        self._gaze_callback(*data)

    def _handle_imu_data(self, *data):
        self._imu_callback(*data)

    def _handle_events(self, *data):
        self._blink_callback(*data)

    def _handle_pupilsize_data(self, *data):
        self._pupil_callback(*data)


class SaccadeFrontend(QtGui.QMainWindow):
    ''' Main class for visualizing the results '''
    # pylint: disable=too-many-instance-attributes
    _timeseries_plot_x_range = 10  # minutes
    _averaging_window = 5  # second

    event_types = ['Blink', 'Saccade', 'Fixation', 'VOR', 'SP']

    def __init__(self, debug_mode=False):
        super().__init__()

        self._debug_mode = debug_mode

        self._init_gui()

        self._imu_calibrated = False

        self._pupil_avg_data = []

        self._df_events = \
            pd.DataFrame(columns=['event_type', 'timestamp_end', 'timestamp_utc', 'duration', 'magnitude',
                                  'averaged'])

        # fps
        self._counter = 0
        self._fps = 0.
        self._lastupdate = time.time()
        self._lastupdate_gaze_timestamp = 0

        self._total_distance = 0

        self._time_start = time.perf_counter()
        self._last_gaze_timestamp = 0
        self._last_average_timestamp = 0

        self._saccade_detector = EventDetector(self._register_new_event, self._debug_mode)

        self._frontend = Frontend(
            gaze_callback=self._update_gaze,
            imu_callback=self._update_imu,
            blink_callback=self._update_blink,
            pupil_callback=self._update_pupil,
        )

        self._update()

        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._average)
        self._drawtimer.start(1e3 * self._averaging_window)

    def closeEvent(self, event):
        '''Override method to handle closed window event.'''
        super().closeEvent(event)
        self._handle_shutdown()

    def _init_gui(self):
        self.setWindowTitle("Adhawk realtime eye movement report")

        self.move(QtWidgets.QDesktopWidget().availableGeometry().center().x() - self.frameGeometry().center().x() * 1,
                  QtWidgets.QDesktopWidget().availableGeometry().center().y() - self.frameGeometry().center().y() * 1)

        self.canvas = pyqtgraph.GraphicsLayoutWidget()
        self.footnote_duration = QtGui.QLabel()
        self.footnote_total_distance = QtGui.QLabel()

        self.table = pyqtgraph.TableWidget()

        self._data = {
            'Total number': [0] * len(self.event_types),
            'Total time': [0] * len(self.event_types),
        }
        self._update_table_in_gui()
        self.table.setFormat('%0.2f')
        # g.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.table.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)
        self.table.setStyleSheet("color: white;"
                                 "selection-color: white;"
                                 "selection-background-color: gray;"
                                 "border-width: 1px;"
                                 "border-color: white;"
                                 "text-align:center;"
                                 "border-width: 2px;"
                                 "border-style: solid;"
                                 "padding: -1px;"
                                 #  "border-left: none;"
                                 # "border-top: none;"
                                 # "border-right: none;"
                                 # "border-bottom: none;"
                                 )
        self.table.setItemDelegate(AlignDelegate())
        self.table.horizontalHeader().setStyleSheet("font-weight: bold;"
                                                    "selection-color: white;"
                                                    "selection-background-color: gray;"

                                                    )
        self.table.verticalHeader().setStyleSheet("font-weight: bold;"
                                                  "selection-color: white;"
                                                  "selection-background-color: gray;"

                                                  )

        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())
        self.mainbox.layout().addWidget(self.table, 1)
        self.mainbox.layout().addWidget(self.canvas, 3)
        self.mainbox.layout().addWidget(self.footnote_duration, 0.5)
        self.mainbox.layout().addWidget(self.footnote_total_distance, 0.5)

        self.mainbox.setStyleSheet("color: white;"
                                   "background-color: black;"
                                   "selection-color: white;"
                                   "selection-background-color: gray;")

        self._setup_plots()

    def _setup_plots(self):
        # pylint: disable=attribute-defined-outside-init
        #  line plot
        self.average_rate = self.canvas.addPlot(title='Average rate', bottom='Time (min)', left='Rate (event/s)')
        self.average_rate.setMouseEnabled(x=False, y=False)
        self.average_rate.setRange(QtCore.QRectF(-self._timeseries_plot_x_range, 0, self._timeseries_plot_x_range, 3))
        self.average_rate.setLimits(xMin=self._timeseries_plot_x_range, xMax=0, yMin=0, yMax=3)
        self.average_rate.addLegend(colCount=len(self.event_types))
        self.plot_average_rate = {}
        for event_i, event in enumerate(self.event_types):
            if event == 'Fixation':
                continue
            self.plot_average_rate[event] = self.average_rate.plot(pen=pyqtgraph.mkPen(ALLCOLORS[event_i], width=3),
                                                                   symbolBrush=ALLBRUSHES[event_i],
                                                                   symbolSize=7,
                                                                   name=event,
                                                                   xdata=[], ydata=[]
                                                                   )

        self.canvas.nextRow()
        self.average_duration = self.canvas.addPlot(title='Average duration', bottom='Time (min)', left='Duration (ms)')
        self.average_duration.setMouseEnabled(x=False, y=False)
        self.average_duration.setRange(
            QtCore.QRectF(-self._timeseries_plot_x_range, 0, self._timeseries_plot_x_range, 1e3))
        self.average_duration.setLimits(xMin=self._timeseries_plot_x_range, xMax=0, yMin=0, yMax=1e3)
        self.average_duration.addLegend(colCount=len(self.event_types))
        self.plot_average_duration = {}
        for event_i, event in enumerate(self.event_types):
            self.plot_average_duration[event] = self.average_duration.plot(
                pen=pyqtgraph.mkPen(ALLCOLORS[event_i], width=3),
                symbolBrush=ALLBRUSHES[event_i],
                symbolSize=7,
                name=event,
                xdata=[], ydata=[]
            )

        self.canvas.nextRow()
        self.pupil_size = self.canvas.addPlot(title='Average pupil size', bottom='Time (min)', left='Size (relative)')
        self.pupil_size.setMouseEnabled(x=False, y=False)
        self.pupil_size.setRange(QtCore.QRectF(-self._timeseries_plot_x_range, 2, self._timeseries_plot_x_range, 4))
        self.pupil_size.setLimits(xMin=self._timeseries_plot_x_range, xMax=0, yMin=2, yMax=4)

        self.plot_pupil_size = self.pupil_size.plot(pen=pyqtgraph.mkPen(ALLCOLORS[event_i], width=3),
                                                    symbolBrush=ALLCOLORS[0],
                                                    symbolSize=7,
                                                    xdata=[], ydata=[]
                                                    )

    def _update_gaze(self, timestamp, xright, yright, zright, xleft, yleft, zleft):
        self._last_gaze_timestamp = timestamp
        self._saccade_detector.update_gaze(timestamp, [[xright, yright, zright], [xleft, yleft, zleft]])

    def _update_imu(self, timestamp, *rvec):
        if len(rvec) < 3:
            return
        self._imu_calibrated = np.all(np.isfinite(rvec))
        if not self._imu_calibrated:
            return
        imu_angles = np.array(R.from_rotvec(rvec).as_euler('xyz', degrees=False))
        imu_angles = np.unwrap(imu_angles)
        self._saccade_detector.update_imu(timestamp, *imu_angles)

    def _update_pupil(self, timestamp, rightpupil, leftpupil):
        self._saccade_detector.add_to_debug_log(['Pupil', timestamp, rightpupil, leftpupil])
        self._pupil_avg_data.append([timestamp, (rightpupil + leftpupil) / 2])

    def _update_blink(self, event_type, timestamp, *args):
        self._saccade_detector.update_blink(event_type, timestamp, *args)
        if event_type == adhawkapi.Events.BLINK:
            self._register_new_event('Blink', timestamp, args[0])

    def _register_new_event(self, event, timestamp, duration, magnitude=0):
        # fill up the gap between this event and the previous event with a fixation
        if len(self._df_events) and event == 'Saccade':
            self._df_events = self._df_events.append(
                {'event_type': 'Fixation',
                 'timestamp_end': timestamp - duration,
                 'timestamp_utc': pd.to_datetime(timestamp - duration, unit='s'),
                 'duration': timestamp - duration - self._df_events.timestamp_end.iloc[-1],
                 'magnitude': magnitude,
                 'averaged': False
                 }, ignore_index=True)

        self._df_events = self._df_events.append(
            {'event_type': event,
             'timestamp_end': timestamp,
             'timestamp_utc': pd.to_datetime(timestamp, unit='s'),
             'duration': duration,
             'magnitude': magnitude,
             'averaged': False
             }, ignore_index=True)

    def _update_table_in_gui(self):
        self.table.setData(self._data)
        self.table.setHorizontalHeaderLabels(self.event_types)

    def _update(self):
        now = time.time()
        deltat = (now - self._lastupdate)
        if deltat <= 0:
            deltat = 0.000000000001
        fps2 = 1.0 / deltat
        self._lastupdate = now
        self._fps = self._fps * 0.9 + fps2 * 0.1

        self.footnote_duration.setText(
            f'total duration: {datetime.timedelta(seconds=time.perf_counter() - self._time_start)}, '
            f'(fps: {self._fps:.2f})')

        df_events = self._df_events[self._df_events.timestamp_end > self._lastupdate_gaze_timestamp]
        if not df_events.empty:
            for event_i, event in enumerate(self.event_types):
                mask = df_events.event_type == event
                if event == 'Saccade':
                    self._total_distance += df_events[mask].magnitude.sum()
                    self.footnote_total_distance.setText(
                        f'total saccadic distance travelled: {self._total_distance:.2f} deg')
                self._data['Total number'][event_i] += len(df_events[mask])
                self._data['Total time'][event_i] += df_events[mask].duration.sum()
            self._update_table_in_gui()
            self._lastupdate_gaze_timestamp = self._df_events.timestamp_end.values[-1]

        QtCore.QTimer.singleShot(1, self._update)
        self._counter += 1

    def _average(self):

        for event in self.event_types:
            # rolling average frequency (k second window)
            data_table = self._df_events.loc[(self._df_events.event_type == event) & (~self._df_events.averaged), :]

            rate = len(data_table) / self._averaging_window
            duration = 0 if data_table.empty else data_table.duration.mean() * 1e3

            if event in self.plot_average_rate:
                xdata, ydata = self.plot_average_rate[event].getData()
                xdata = [] if xdata is None else list(xdata)
                ydata = [] if ydata is None else list(ydata)
                xdata = [xdata[0] - self._averaging_window / 60] + xdata if xdata else [0]
                ydata = ydata + [rate] if ydata else [rate]
                self.plot_average_rate[event].setData(xdata, ydata)

            if event in self.plot_average_duration:
                xdata, ydata = self.plot_average_duration[event].getData()
                xdata = [] if xdata is None else list(xdata)
                ydata = [] if ydata is None else list(ydata)
                xdata = [xdata[0] - self._averaging_window / 60] + xdata if xdata else [0]
                ydata = ydata + [duration] if ydata else [duration]
                self.plot_average_duration[event].setData(xdata, ydata)

        xdata, ydata = self.plot_pupil_size.getData()
        xdata = [] if xdata is None else list(xdata)
        ydata = [] if ydata is None else list(ydata)
        xdata = [xdata[0] - self._averaging_window / 60] + xdata if xdata else [0]
        newval = np.nanmean(np.array(self._pupil_avg_data)[:, 1]) if self._pupil_avg_data else 0
        ydata = ydata + [newval] if ydata else [newval]
        self.plot_pupil_size.setData(xdata, ydata)
        self._pupil_avg_data = []

        self._df_events['averaged'] = True
        if not self._debug_mode:
            self._df_events = \
                pd.DataFrame(columns=['event_type', 'timestamp_end', 'timestamp_utc', 'duration', 'magnitude',
                                      'averaged'])

    def _handle_shutdown(self):
        current = time.time()
        self._saccade_detector.shutdown(current)
        self._frontend.shutdown()
        if self._debug_mode:
            self._df_events.to_csv(os.path.join(LOGS_PATH, f'df_events_{current}.csv'), index=False)
        self.close()


def main():
    '''Main function'''
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create('Fusion'))

    parser = argparse.ArgumentParser(description='Adhawk real-time eye movement events demo')
    parser.add_argument('--debug', default=False, action='store_true',
                        help='Run the frontend in debug mode')
    args = parser.parse_args(sys.argv[2:])
    main_window = SaccadeFrontend(args.debug)
    main_window.show()
    sys.exit(app.exec_())
