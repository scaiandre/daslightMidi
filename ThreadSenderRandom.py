from ThreadSenderBase import ThreadSenderBase
from constants import OUTPUT_PORT_NAME
from constants import FADER_VALUES


import mido


import random
import threading
import time
from time import gmtime, strftime

from utils import select_different_random_value


class ThreadSenderRandom(ThreadSenderBase):

    def run(self):
        with mido.open_output(OUTPUT_PORT_NAME) as outport:
            while not self.is_stopped():
                fader_value = -1
                while not self.is_stopped() and not self.is_paused():
                    sleep_timer = random.uniform(0.2, 4)
                    fader_value = select_different_random_value(FADER_VALUES, fader_value)
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Set next value:", sleep_timer, fader_value)
                    midi_fader_value = int(fader_value / 2)
                    outport.send(mido.Message('control_change', channel=0, control=3, value=midi_fader_value))
                    if fader_value % 2 != 0:
                        outport.send(mido.Message('control_change', channel=0, control=4, value=127))
                    self.sleep_with_stop_and_pause(sleep_timer)
                    if self.is_paused():
                        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Pausing")
                        outport.send(mido.Message('note_on', channel=0, note=61))
                self.sleep_with_stop(1)
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Leaving thread")