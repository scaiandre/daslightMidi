from ThreadSenderBase import ThreadSenderBase
from constants import OUTPUT_PORT_NAME
from constants import FADER_VALUES


import mido


import random
import threading
import time
from time import gmtime, strftime

from utils import select_different_random_value


class ThreadSenderBpmSynced(ThreadSenderBase):
    _bpm_count = 0
    _bpm_lock = threading.Lock()

    def inc_bpm(self):
        with self._bpm_lock:
            self._bpm_count += 1

    def run(self):
        with mido.open_output(OUTPUT_PORT_NAME) as outport:
            while not self.is_stopped():
                fader_value = -1
                while not self.is_stopped() and not self.is_paused():
                    start_bpm = self._bpm_count
                    sleep_bpm_count = random.randint(1, 3)
                    fader_value = select_different_random_value(FADER_VALUES, fader_value)
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Setting fader value for the next beats:", sleep_bpm_count, fader_value)
                    midi_fader_value = int(fader_value / 2)
                    outport.send(mido.Message('control_change', channel=0, control=3, value=midi_fader_value))
                    if fader_value % 2 != 0:
                        outport.send(mido.Message('control_change', channel=0, control=4, value=127))
                    while not self.is_stopped() and not self.is_paused() and (start_bpm + (sleep_bpm_count * 2)) > self._bpm_count:
                        self.sleep_with_stop_and_pause(0.05)
                    if self.is_paused():
                        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Pausing")
                        outport.send(mido.Message('note_on', channel=0, note=61))
                self.sleep_with_stop(0.2)
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Leaving thread")