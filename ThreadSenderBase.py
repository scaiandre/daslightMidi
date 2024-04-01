from constants import OUTPUT_PORT_NAME
from constants import FADER_VALUES


import mido


import random
import threading
import time
from time import gmtime, strftime

from utils import select_different_random_value


class ThreadSenderBase(threading.Thread):
    _instance = None
    _lock = threading.Lock()
    _stop_signal = False
    _pause_signal = True

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSenderBase, cls).__new__(cls)
                cls._instance._stop_signal = False
                cls._instance._pause_signal = True
            return cls._instance

    def is_stopped(self):
        with self._lock:
            return self._stop_signal

    def is_paused(self):
        with self._lock:
            return self._pause_signal


    def stop(self):
        with self._lock:
            self._stop_signal = True


    def pause(self):
        with self._lock:
            self._pause_signal = True


    def unpause(self):
        with self._lock:
            self._pause_signal = False


    def sleep_with_stop_and_pause(self, sleepSeconds):
        endTime = time.time() + sleepSeconds
        while time.time() < endTime and not self.is_stopped() and not self.is_paused():
            time.sleep(0.05)  # Check for stop signal at short intervals


    def sleep_with_stop(self, sleepSeconds):
        endTime = time.time() + sleepSeconds
        while time.time() < endTime and not self.is_stopped() and self.is_paused():
            time.sleep(0.05)  # Check for stop signal at short intervals