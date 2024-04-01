import mido
import time
import keyboard
from time import gmtime, strftime

from ThreadSenderBpmSynced import ThreadSenderBpmSynced
from ThreadSenderRandom import ThreadSenderRandom
from constants import BPM_CONDITION_0, BPM_CONDITION_1, INPUT_PORT_NAME, START_CONDITION, STOP_CONDITION



# This class will manage the sending thread, ensuring it is a singleton
def message_received(sender_thread, msg):
    if msg.dict() == START_CONDITION:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), msg, "Start Condition")
        if sender_thread.is_alive():
            sender_thread.unpause()
    elif msg.dict() == STOP_CONDITION:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), msg, "Stop Condition")
        if sender_thread.is_alive():
            sender_thread.pause()
    elif msg.dict() == BPM_CONDITION_0 or msg.dict() == BPM_CONDITION_1:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), msg, "BPM sync, increment")
        if sender_thread.is_alive():
            sender_thread.inc_bpm()

def midi_listener(inport, sender_thread):
    for msg in inport.iter_pending():
        message_received(sender_thread, msg)

def main():
    sender_thread = ThreadSenderBpmSynced()
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
