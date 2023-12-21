''' embedded system info stream '''
import enum
import logging
import os
import struct
import sys

import numpy as np
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

import adhawkapi.frontend.internal as internalfrontendapi
import adhawkapi.internal as internalapi


# pylint: disable=wrong-import-position
# pylint: disable=no-member

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from adhawkguitools import RollingPlotData  # noqa: E402


class EmbeddedInfoType(enum.IntEnum):
    '''Enum representing set of blob types'''
    ALG_INFO = 1
    COM_INFO = 2
    SYSTEM_INFO = 3
    CPU_INFO = 4
    TROS_TRACKING_INFO = 5


class EmbeddedInfoParser:
    ''' Parses embedded info msgs. Can be used by other frontends '''

    @staticmethod
    def parse_embedded_info_msg(data):
        '''Parser for embedded info msgs'''

        # pylint: disable=too-many-locals
        msg_type = data[0]
        if msg_type == EmbeddedInfoType.ALG_INFO:
            timestamp, glints_accepted, glints_rejected, pupil_accepted, pupil_rejected, \
                gaze_successes, gaze_failures, pupil_successes, pupil_failures, \
                fusion_successes, fusion_failures = struct.unpack_from('<f4H6B', data, 1)
            return msg_type, {"timestamp": timestamp,
                              "glints_accepted": glints_accepted,
                              "glints_rejected": glints_rejected,
                              "pupil_accepted": pupil_accepted,
                              "pupil_rejected": pupil_rejected,
                              "gaze_successes": gaze_successes,
                              "gaze_failures": gaze_failures,
                              "pupil_successes": pupil_successes,
                              "pupil_failures": pupil_failures,
                              "fusion_successes": fusion_successes,
                              "fusion_failures": fusion_failures}

        if msg_type == EmbeddedInfoType.COM_INFO:
            timestamp, rx_count, tx_count, mainloop_tx_count = struct.unpack_from('<f3H', data, 1)
            return msg_type, {"timestamp": timestamp,
                              "rx_count": rx_count,
                              "tx_count": tx_count,
                              "mainloop_tx_count": mainloop_tx_count}

        if msg_type == EmbeddedInfoType.SYSTEM_INFO:
            timestamp, max_stack_usage, mainloop_work, interrupt_work, dropped_packets_queue_full, \
                dropped_packets_queue_busy, dropped_packets_spi, dropped_packets_oom, dropped_packets_length = \
                struct.unpack_from('<f3I5B', data, 1)
            return msg_type, {"timestamp": timestamp,
                              "max_stack_usage": max_stack_usage,
                              "mainloop_work": mainloop_work,
                              "interrupt_work": interrupt_work,
                              "dropped_packets_queue_full": dropped_packets_queue_full,
                              "dropped_packets_queue_busy": dropped_packets_queue_busy,
                              "dropped_packets_spi": dropped_packets_spi,
                              "dropped_packets_oom": dropped_packets_oom,
                              "dropped_packets_length": dropped_packets_length}

        if msg_type == EmbeddedInfoType.CPU_INFO:
            timestamp, pupil_pulse, glint_pulse, calculate_pupil, calculate_fused, calculate_filtered, \
                calculate_gaze, capture_pulse_main, capture_pulse_interrupt, send_stream_packet = \
                struct.unpack_from('<10f', data, 1)
            return msg_type, {"timestamp": timestamp,
                              "pupil_pulse": pupil_pulse,
                              "glint_pulse": glint_pulse,
                              "calculate_pupil": calculate_pupil,
                              "calculate_fused": calculate_fused,
                              "calculate_filtered": calculate_filtered,
                              "calculate_gaze": calculate_gaze,
                              "capture_pulse_main": capture_pulse_main,
                              "capture_pulse_interrupt": capture_pulse_interrupt,
                              "send_stream_packet": send_stream_packet,
                              }

        if msg_type == EmbeddedInfoType.TROS_TRACKING_INFO:
            timestamp, pulse_captured, queue_full, timer_overrun, unsupported_pd, glint_pw_filter, pupil_pw_filter = \
                struct.unpack_from('<fI5H', data, 1)
            return msg_type, {"timestamp": timestamp,
                              "pulse_captured": pulse_captured,
                              "queue_full": queue_full,
                              "timer_overrun": timer_overrun,
                              "unsupported_pd": unsupported_pd,
                              "glint_pw_filter": glint_pw_filter,
                              "pupil_pw_filter": pupil_pw_filter,
                              }

        logging.warning(f'Unknown embedded info msg type {msg_type}')
        return None


# Time in seconds to display on the graphs
GRAPH_HISTORY = 8

# Rate at which embedded will send embedded info messages (Hz)
EMBEDDED_RATE = 10

# Reset interval on TROS profiler in millisecond
TROS_RESET_INTERVAL_MS = (1 / EMBEDDED_RATE) * 100

SCALE_TO_SECOND = int(100 / TROS_RESET_INTERVAL_MS)


class FrontendData:
    ''' Handle the data aggregation '''

    def __init__(self):
        self._max_buffer_len = GRAPH_HISTORY

        self.com_info_history = RollingPlotData(['timestamps', 'rx_count', 'tx_count', 'mainloop_tx_count'],
                                                maxlen=self._max_buffer_len)
        self.sys_info_history = RollingPlotData(['timestamps', 'mainloop_usage', 'interrupt_usage', 'cpu_usage',
                                                 'dropped_packets_queue_full', 'dropped_packets_queue_busy',
                                                 'dropped_packets_spi', 'dropped_packets_oom',
                                                 'dropped_packets_length'], maxlen=self._max_buffer_len)
        self.alg_info_history = RollingPlotData(['timestamps', 'glints_accepted', 'glints_rejected',
                                                 'pupil_accepted', 'pupil_rejected',
                                                 'gaze_successes', 'gaze_failures',
                                                 'pupil_successes', 'pupil_failures',
                                                 'fusion_successes', 'fusion_failures'], maxlen=self._max_buffer_len)
        self.tros_tracking_history = RollingPlotData(['timestamps', 'pulse_captured', 'queue_full',
                                                      'timer_overrun', 'unsupported_pd',
                                                      'glint_pw_filter', 'pupil_pw_filter'],
                                                     maxlen=self._max_buffer_len)

        self.cpu_info = {}

        self._parser = EmbeddedInfoParser()
        self._internal_api = internalfrontendapi.InternalApi()
        self._internal_api.register_stream_handler(
            internalapi.PacketType.EMBEDDED_INFO, self._handle_embedded_info_data)
        self._internal_api.start(connect_cb=self._handle_connect)

    def _handle_alg_info_data(self, args):
        # logging.debug(f"glintsAccepted: {args['glints_accepted']}, glintsRejected: {args['glints_rejected']}, " \
        #               f"gazeSuccesses: {args['gaze_successes']}, gazeFailures: {args['gaze_failures']}")

        self.alg_info_history.append([args['timestamp'], args['glints_accepted'], args['glints_rejected'],
                                      args['pupil_accepted'], args['pupil_rejected'],
                                      args['gaze_successes'], args['gaze_failures'],
                                      args['pupil_successes'], args['pupil_failures'],
                                      args['fusion_successes'], args['fusion_failures']])

    def _handle_com_info_data(self, args):
        self.com_info_history.append([args['timestamp'], args['rx_count'], args['tx_count'],
                                      args['mainloop_tx_count']])

    def _handle_system_info_data(self, args):
        logging.debug(f"Max Stack Usage: {args['max_stack_usage']}, Main Loop Work: {args['mainloop_work']}, "
                      f"Interrupt work: {args['interrupt_work']}")

        # Convert from microseconds to seconds, then to a percent
        mainloop_usage = args['mainloop_work'] / 1e6 * 100
        interrupt_usage = args['interrupt_work'] / 1e6 * 100
        total_usage = mainloop_usage + interrupt_usage
        self.sys_info_history.append([args['timestamp'], mainloop_usage, interrupt_usage, total_usage,
                                      args['dropped_packets_queue_full'], args['dropped_packets_queue_busy'],
                                      args['dropped_packets_spi'], args['dropped_packets_oom'],
                                      args['dropped_packets_length']])

    def _handle_cpu_info_data(self, args):
        logging.debug(f"Pupil Pulse: {args['pupil_pulse']}, Glint Pulse: {args['glint_pulse']}, "
                      f"Calculate Pupil: {args['calculate_pupil']}, Calculate Fused: {args['calculate_fused']}, "
                      f"Calculate Filtered: {args['calculate_filtered']}, Calculate Gaze: {args['calculate_gaze']}, "
                      f"Pulse Main: {args['capture_pulse_main']}, Pulse Interrupt: {args['capture_pulse_interrupt']}, "
                      f"Send Stream: {args['send_stream_packet']}")
        self.cpu_info = {'pupil_pulse': args['pupil_pulse'],
                         'glint_pulse': args['glint_pulse'],
                         'calculate_pupil': args['calculate_pupil'],
                         'calculate_fused': args['calculate_fused'],
                         'calculate_filtered': args['calculate_filtered'],
                         'calculate_gaze': args['calculate_gaze'],
                         'capture_pulse_main': args['capture_pulse_main'],
                         'caputure_pulse_interrupt': args['capture_pulse_interrupt'],
                         'send_stream_packet': args['send_stream_packet']}

    def _handle_tros_tracking_info_data(self, args):
        self.tros_tracking_history.append([args['timestamp'], args['pulse_captured'], args['queue_full'],
                                          args['timer_overrun'], args['unsupported_pd'], args['glint_pw_filter'],
                                          args['pupil_pw_filter']])

    def _handle_embedded_info_data(self, data):
        msg_type, args = self._parser.parse_embedded_info_msg(data)

        if msg_type == EmbeddedInfoType.ALG_INFO:
            self._handle_alg_info_data(args)
        elif msg_type == EmbeddedInfoType.COM_INFO:
            self._handle_com_info_data(args)
        elif msg_type == EmbeddedInfoType.SYSTEM_INFO:
            self._handle_system_info_data(args)
        elif msg_type == EmbeddedInfoType.CPU_INFO:
            self._handle_cpu_info_data(args)
        elif msg_type == EmbeddedInfoType.TROS_TRACKING_INFO:
            self._handle_tros_tracking_info_data(args)

    def _handle_connect(self, error):
        if not error:
            self.alg_info_history.clear()
            self.com_info_history.clear()
            self.sys_info_history.clear()
            self.tros_tracking_history.clear()
            self._internal_api.enable_embedded_info(EMBEDDED_RATE, callback=(lambda *args: None))

    def shutdown(self):
        ''' Shutdown the port '''
        self._internal_api.shutdown()


class MainWindow(QtGui.QMainWindow):
    ''' Main pyqtgraph Gui window '''

    # pylint: disable=too-many-instance-attributes
    refresh_rate = 10

    def __init__(self, parent=None):
        # we are initializing UI.
        # pylint: disable=too-many-statements
        super().__init__(parent)
        self.frontend = FrontendData()

        # Create Gui Elements
        self._canvas = pyqtgraph.GraphicsLayoutWidget()
        self.setCentralWidget(self._canvas)

        self._tracker_plot = {}
        self._plots = []

        self._cpu_usage = self._canvas.addPlot(title='CPU Usage')
        self._cpu_usage_plot = self._cpu_usage.plot()
        self._cpu_usage_label = self._canvas.addLabel('')
        self._plots.append(self._cpu_usage)
        self._canvas.nextRow()

        self._com_info = self._canvas.addPlot(title='COM Info')
        self._com_info_plot = self._com_info.plot()
        self._com_info_label = self._canvas.addLabel('')
        self._plots.append(self._com_info)
        self._canvas.nextRow()

        self._dropped_packets = self._canvas.addPlot(title='Dropped Packets')
        self._queue_full_plot = self._dropped_packets.plot(pen=QtGui.QColor('white'))
        self._queue_busy_plot = self._dropped_packets.plot(pen=QtGui.QColor('yellow'))
        self._spi_plot = self._dropped_packets.plot(pen=QtGui.QColor('red'))
        self._oom_plot = self._dropped_packets.plot(pen=QtGui.QColor('blue'))
        self._length_plot = self._dropped_packets.plot(pen=QtGui.QColor('green'))
        self._dropped_label = self._canvas.addLabel('')
        self._plots.append(self._dropped_packets)
        self._canvas.nextRow()

        self._pulses = self._canvas.addPlot(title='Pulse Rate')
        self._glints_plot = self._pulses.plot(pen=QtGui.QColor('white'))
        self._pupil_plot = self._pulses.plot(pen=QtGui.QColor('yellow'))
        self._pulses_label = self._canvas.addLabel('')
        self._plots.append(self._pulses)
        self._canvas.nextRow()

        self._tros_tracking = self._canvas.addPlot(title='Tros Tracking')
        self._pulse_captured_plot = self._tros_tracking.plot(pen=QtGui.QColor('white'))
        self._tros_label = self._canvas.addLabel('')
        self._plots.append(self._tros_tracking)
        self._canvas.nextRow()

        self._alg = self._canvas.addPlot(title='Alg Rate')
        self._gaze_plot = self._alg.plot()
        self._pupil_plot = self._alg.plot()
        self._alg_label = self._canvas.addLabel('')
        self._plots.append(self._alg)
        self._canvas.nextRow()

        for plot in self._plots:
            plot.hideAxis('bottom')
            plot.setLimits(yMin=0)
            plot.enableAutoRange(axis='y')
            plot.setAutoVisible(y=True)

        # Start
        self._drawtimer = QtCore.QTimer()
        self._drawtimer.timeout.connect(self._draw)
        self._drawtimer.start(1000 / self.refresh_rate)

    @staticmethod
    def _get_samples_per_second(timestamps):
        if len(timestamps) <= 1:
            return 0

        time_deltas = np.diff([timestamps[0]] + timestamps)
        return int(round(1 / np.mean(time_deltas)))

    @classmethod
    def _get_x_vals(cls, timestamps):
        samples_per_second = cls._get_samples_per_second(timestamps)
        if not samples_per_second:
            return np.zeros(1)
        return np.array(timestamps[samples_per_second:])

    @classmethod
    def _get_y_vals(cls, timestamps, data):
        samples_per_second = cls._get_samples_per_second(timestamps)
        if not samples_per_second:
            return np.zeros(1)
        data = np.array(data)
        return data[samples_per_second:] * SCALE_TO_SECOND

    @classmethod
    def _get_normalized_val(cls, timestamps, data):
        samples_per_second = cls._get_samples_per_second(timestamps)
        if not samples_per_second:
            return 0
        if len(data) >= samples_per_second:
            return np.mean(data[-samples_per_second:]) * SCALE_TO_SECOND
        return 0

    def _draw_sys_info(self):
        data = self.frontend.sys_info_history.copy()
        if not data.timestamps:
            return
        self._cpu_usage.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))

        mainloop_usage = self._get_normalized_val(data.timestamps, data.mainloop_usage)
        interrupt_usage = self._get_normalized_val(data.timestamps, data.interrupt_usage)
        total_usage = mainloop_usage + interrupt_usage
        self._cpu_usage_label.setText(f'Total Usage: {total_usage:.1f}%<br>'
                                      f'Mainloop: {mainloop_usage:.1f}%<br>'
                                      f'Interrupts: {interrupt_usage:.1f}%<br>')

        self._cpu_usage_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                        'y': self._get_y_vals(data.timestamps, data.cpu_usage)})

    def _draw_alg_info(self):
        data = self.frontend.alg_info_history.copy()
        if not data.timestamps:
            return
        self._pulses.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))
        self._alg.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))

        glints_accepted = self._get_normalized_val(data.timestamps, data.glints_accepted)
        glints_rejected = self._get_normalized_val(data.timestamps, data.glints_rejected)
        pupil_accepted = self._get_normalized_val(data.timestamps, data.pupil_accepted)
        pupil_rejected = self._get_normalized_val(data.timestamps, data.pupil_rejected)
        self._pulses_label.setText(f'Glint Pulses Accepted: {glints_accepted:.0f}<br>'
                                   f'Glint Pulses Rejected: {glints_rejected:.0f}<br>'
                                   f'Pupil Pulses Accepted: {pupil_accepted:.0f}<br>'
                                   f'Pupil Pulses Rejected: {pupil_rejected:.0f}<br>')
        self._glints_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                     'y': self._get_y_vals(data.timestamps, data.glints_accepted)})
        self._pupil_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                    'y': self._get_y_vals(data.timestamps, data.pupil_accepted)})

        fusion_successes = self._get_normalized_val(data.timestamps, data.fusion_successes)
        fusion_failures = self._get_normalized_val(data.timestamps, data.fusion_failures)
        pupil_successes = self._get_normalized_val(data.timestamps, data.pupil_successes)
        pupil_failures = self._get_normalized_val(data.timestamps, data.pupil_failures)
        gaze_successes = self._get_normalized_val(data.timestamps, data.gaze_successes)
        gaze_failures = self._get_normalized_val(data.timestamps, data.gaze_failures)
        self._alg_label.setText(f'Fusion Successes: {fusion_successes:.0f}<br>'
                                f'Fusion Failures: {fusion_failures:.0f}<br>'
                                f'Pupil Successes: {pupil_successes:.0f}<br>'
                                f'Pupil Failures: {pupil_failures:.0f}<br>'
                                f'Gaze Successes: {gaze_successes:.0f}<br>'
                                f'Gaze Failures: {gaze_failures:.0f}')
        self._gaze_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                   'y': self._get_y_vals(data.timestamps, data.gaze_successes)})
        self._pupil_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                    'y': self._get_y_vals(data.timestamps, data.pupil_successes)})

    def _draw_com_info(self):
        data = self.frontend.com_info_history.copy()
        if not data.timestamps:
            return
        self._com_info.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))

        rx_count = int(self._get_normalized_val(data.timestamps, data.rx_count))
        tx_count = int(self._get_normalized_val(data.timestamps, data.tx_count))
        mainloop_tx_count = int(self._get_normalized_val(data.timestamps, data.mainloop_tx_count))
        self._com_info_label.setText(f'rx_count: {rx_count}<br>'
                                     f'interrupt_tx_count: {tx_count - mainloop_tx_count}<br>'
                                     f'main loop tx: {mainloop_tx_count}<br>')

        self._com_info_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                       'y': self._get_y_vals(data.timestamps, data.tx_count)})

    def _draw_dropped_info(self):
        data = self.frontend.sys_info_history.copy()
        if not data.timestamps:
            return
        self._dropped_packets.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))

        dropped_packets_queue_full = self._get_normalized_val(data.timestamps, data.dropped_packets_queue_full)
        dropped_packets_queue_busy = self._get_normalized_val(data.timestamps, data.dropped_packets_queue_busy)
        dropped_packets_spi = self._get_normalized_val(data.timestamps, data.dropped_packets_spi)
        dropped_packets_oom = self._get_normalized_val(data.timestamps, data.dropped_packets_oom)
        dropped_packets_length = self._get_normalized_val(data.timestamps, data.dropped_packets_length)
        self._dropped_label.setText(f'Queue Full: {dropped_packets_queue_full:.0f}<br>'
                                    f'Queue Busy: {dropped_packets_queue_busy:.0f}<br>'
                                    f'SPI: {dropped_packets_spi:.0f}<br>'
                                    f'OOM: {dropped_packets_oom:.0f}<br>'
                                    f'Length: {dropped_packets_length:.0f}<br>')

        self._queue_full_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                         'y': self._get_y_vals(data.timestamps, data.dropped_packets_queue_full)})
        self._queue_busy_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                         'y': self._get_y_vals(data.timestamps, data.dropped_packets_queue_busy)})
        self._spi_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                  'y': self._get_y_vals(data.timestamps, data.dropped_packets_spi)})
        self._oom_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                  'y': self._get_y_vals(data.timestamps, data.dropped_packets_oom)})
        self._length_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                     'y': self._get_y_vals(data.timestamps, data.dropped_packets_length)})

    def _draw_tros_tracking_info(self):
        data = self.frontend.tros_tracking_history.copy()
        if not data.timestamps:
            return
        self._tros_tracking.setRange(xRange=(data.timestamps[-1] - GRAPH_HISTORY, data.timestamps[-1]))

        pulse_captured = self._get_normalized_val(data.timestamps, data.pulse_captured)
        queue_full = self._get_normalized_val(data.timestamps, data.queue_full)
        timer_overrun = self._get_normalized_val(data.timestamps, data.timer_overrun)
        unsupported_pd = self._get_normalized_val(data.timestamps, data.unsupported_pd)
        glint_pw_filter = self._get_normalized_val(data.timestamps, data.glint_pw_filter)
        pupil_pw_filter = self._get_normalized_val(data.timestamps, data.pupil_pw_filter)
        self._tros_label.setText(f'Pulse captured: {pulse_captured:.0f}<br>'
                                 f'Queue full: {queue_full:.0f}<br>'
                                 f'Timer Overrun: {timer_overrun:.0f}<br>'
                                 f'Unsupported PD: {unsupported_pd:.0f}<br>'
                                 f'Glint PW Filter: {glint_pw_filter:.0f}<br>'
                                 f'Pupil PW Filter: {pupil_pw_filter:.0f}<br>')

        self._pulse_captured_plot.setData(**{'x': self._get_x_vals(data.timestamps),
                                             'y': self._get_y_vals(data.timestamps, data.pulse_captured)})

    def _draw(self):
        self._draw_sys_info()
        self._draw_alg_info()
        self._draw_com_info()
        self._draw_dropped_info()
        self._draw_tros_tracking_info()

    def closeEvent(self, _event):
        ''' Override QMainWindow.closeEvent '''
        self.frontend.shutdown()


def main():
    ''' App entrypoint '''
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
