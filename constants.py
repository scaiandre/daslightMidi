# Replace these with the names of your virtual MIDI ports created in loopMIDI
BASE_PORT_NAME = 'RandomDasLight'
OUTPUT_PORT_NAME = BASE_PORT_NAME + 'Control 2'
INPUT_PORT_NAME = BASE_PORT_NAME + 'Return 0'

# Conditions for starting and stopping the sender thread
START_CONDITION = {'note': 60, 'channel': 0, 'type': 'note_on', 'velocity': 1, 'time': 0}  # Example: Note C4 on
STOP_CONDITION = {'note': 60, 'channel': 0, 'type': 'note_on', 'velocity': 0, 'time': 0}  # Example: Note C4 on

# Condition for incrementing the BPM value
BPM_CONDITION_0 = {'channel': 1, 'control': 1, 'type': 'control_change', 'value': 0, 'time': 0}  
BPM_CONDITION_1 = {'channel': 1, 'control': 1, 'type': 'control_change', 'value': 1, 'time': 0}  

FADER_VALUES = [6, 8, 9, 10, 11, 12, 15, 16, 16, 17, 18, 19, 20, 23, 26, 30, 33, 34, 35, 37, 39, 40, 46, 47, 49, 51, 52, 58, 65, 68, 127, 130, 151, 161, 162, 163, 166]
