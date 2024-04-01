# daslightMidi

https://forum.daslight.com/viewtopic.php?t=9014

I added some effort to my previous approach, to reach my goal of letting my Showlaser play its patterns in a random fashion while still having control on which of these are played.

So, I created a static scene, which contains the basic setup (Dimmer, X / Y positions etc.). Now, the idea is to set the pattern via MIDI in live mode.

For this,  I (ChatGPT) created a python application, that should control that specific fader via MIDI whenever that specific scene is started. 

For this, the program listens on a specific MIDI port that is triggered, when the scene is turned on. When this is detected, it starts ("unpauses") a thread, that then sends MIDI signals to change the "pattern" fader of my laser device in that scene. When the scene is stopped, the thread is set to paused again. As a last action the thread then sends another MIDI command to turn off the "pattern" fader of my laser device in that scene.

## Setup

### Install loopMidi

A big thank you to Tobias Erichsen!!! He created the wonderful loopMidi, which does 99.9 % of the heavy lifting:

https://www.tobias-erichsen.de/software/loopmidi.html

### Setup ports
See the screenshots in the ```docs``` folder.

### Configure MIDI in Daslight
See the screenshots in the ```docs``` folder.

### setup.cmd

```setup.cmd```

## Launch
```daslightMidi.cmd```

# Note of thanks to Tobias Erichsen
All of this is build on top of Tobias Erichsens work in loopMidi and virtualMidi (https://www.tobias-erichsen.de/software.html).