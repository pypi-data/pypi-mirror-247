''' Event stream test '''

import time

import adhawkapi
import adhawkapi.frontend


class EventFrontend:
    ''' Event Frontend '''

    def __init__(self):
        self._api = adhawkapi.frontend.FrontendApi()
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)
        self._api.start(connect_cb=self._handle_connect)

    @staticmethod
    def _handle_events(event_type, timestamp, *args):

        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f'Got blink: {timestamp} {duration}')
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(f'Eye Close: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.EYE_OPENED:
            eye_idx = args[0]
            print(f'Eye Open: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.SACCADE:
            duration, magnitude = args
            print(f'Saccade: {timestamp} {duration, magnitude}')
        if event_type == adhawkapi.Events.TRACKLOSS_START:
            eye_idx = args[0]
            print(f'Trackloss Start: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.TRACKLOSS_END:
            eye_idx = args[0]
            print(f'Trackloss End: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.VALIDATION_SAMPLE:
            ref_x = args[0]
            ref_y = args[1]
            ref_z = args[2]
            gaze_x = args[3]
            gaze_y = args[4]
            gaze_z = args[5]
            vergence = args[6]
            precision = args[7]
            print(f'Validation Sample: {timestamp} {ref_x} {ref_y} {ref_z} {gaze_x} {gaze_y} {gaze_z} \
                  {vergence} {precision}')
        if event_type == adhawkapi.Events.VALIDATION_SUMMARY:
            mae = args[0]
            print(f'Validation Summary: {timestamp} {mae}')
        if event_type == adhawkapi.Events.EXTERNAL_TRIGGER:
            trigger_id = args[0]
            print(f'External event from trigger{trigger_id}, time: {timestamp}')

    def _handle_connect(self, error):
        if not error:
            self._api.set_stream_control(adhawkapi.PacketType.EXTENDED_GAZE, 500, callback=(lambda *args: None))
            self._api.set_stream_control(adhawkapi.PacketType.PER_EYE_GAZE, 500, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.TRACKLOSS_START_END, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.VALIDATION_RESULTS, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.EXTERNAL_TRIGGER, 1, callback=(lambda *args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.SACCADE, 1, callback=(lambda *args: None))
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

    def shutdown(self):
        ''' Shutdown '''
        self._api.stop_log_session(callback=lambda *args: None)
        self._api.shutdown()


def main():
    ''' App entrypoint '''
    frontend = EventFrontend()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()
