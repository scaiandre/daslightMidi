import mido
import threading
import time
import random
import keyboard
from time import gmtime, strftime

# Replace these with the names of your virtual MIDI ports created in loopMIDI
BASE_PORT_NAME='RandomDasLight'
INPUT_PORT_NAME = BASE_PORT_NAME + 'Return 1'
OUTPUT_PORT_NAME = BASE_PORT_NAME + 'Control 1'

# Conditions for starting and stopping the sender thread
START_CONDITION = {'note': 60, 'channel': 0, 'type': 'note_on', 'velocity': 1, 'time': 0}  # Example: Note C4 on
STOP_CONDITION = {'note': 60, 'channel': 0, 'type': 'note_on', 'velocity': 0, 'time': 0}  # Example: Note C4 on

FADER_VALUES = [26, 33, 37, 39, 40, 49]

def select_random_value(array):
    """Selects a random value from the given array."""
    if not array:  # Check if the array is empty
        return None  # Or raise an error or another appropriate response
    return random.choice(array)

def select_different_random_value(array, currentvalue):
    """Selects a random value from the given array differing from passed."""
    if not array:  # Check if the array is empty
        return None  # Or raise an error or another appropriate response
    while True:
        nextvalue = random.choice(array)
        if nextvalue != currentvalue:
            return nextvalue
            
    
# This class will manage the sending thread, ensuring it is a singleton
class MessageSender(threading.Thread):
    _instance = None
    _lock = threading.Lock()
    _stop_signal = False
    _pause_signal = True

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MessageSender, cls).__new__(cls)
                cls._instance._stop_signal = False
                cls._instance._pause_signal = True
            return cls._instance

    def is_stopped(self):
        with self._lock:
            return self._stop_signal    

    def is_paused(self):
        with self._lock:
            return self._pause_signal    
    
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


def message_received(sender_thread, msg):
    if msg.dict() == START_CONDITION:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Start Condition")
        if sender_thread.is_alive():
            sender_thread.unpause()
    elif msg.dict() == STOP_CONDITION:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Stop Condition")
        if sender_thread.is_alive():
            sender_thread.pause()

def midi_listener(inport, sender_thread):
    for msg in inport.iter_pending():
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Captured midi message:", msg)
        message_received(sender_thread, msg)

def main():
    sender_thread = MessageSender()
    sender_thread.start()
    
    with mido.open_input(INPUT_PORT_NAME) as inport:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Listening for MIDI messages and keyboard input. Press 'x' to exit.")
        while True:
            midi_listener(inport, sender_thread)
            
            if keyboard.is_pressed('x'):  # If 'x' is pressed, exit the loop
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Exiting...")
                if sender_thread.is_alive():
                    sender_thread.stop()
                    sender_thread.join()  # Ensure the sender thread has finished
                break
            time.sleep(0.05)  # Short delay to prevent high CPU usage

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "Program interrupted.")
