Draws a Peano Curve using the method described in Giuseppe Peano's paper from 1890, A space-filling curve. See [https://en.wikipedia.org/wiki/Space-filling_curve](https://en.wikipedia.org/wiki/Space-filling_curve). 

Clone and install dependencies:

1. Install Python v3.11.0 with tkinter support. Turtle requires tkinter but system tkinter is deprecated and fails, but system insists on using it anyway, so reinstall current Python version with tkinter support.

	```
	brew uninstall tcl-tk
	brew install tcl-tk
	pyenv install 3.11.0
	```

2. Install pysinewave (current version works correctly with stereo channels):

	```
	pip install pysinewave
	```

3. Install rtmidi, a Python wrapper for a C library to send MIDI messages over IAC virtual port.

	```
	pip install python-rtmidi
	```

4. Configure Audio MIDI Setup using IAC virtual port to receive MIDI messages from Python which are then passed to Ableton. MIDI is sent on channel 1 (X) and channel 2 (Y). Ableton must be configured to receive MIDI on IAC. (peanopiano.als is a local project configured correctly.)

Run! (interactive)

```
python peano.py
```

or pass arguments in the form:

```
python peano.py _n [1...10+] _precision [0..10+] _display [10..1000+] --screen_x [] --screen_y [] --sinewave || --midi
```

for example:

```
python peano.py 4 4 400 --sinewave
```

or:

```
python peano.py 4 4 400 --midi
``` 

or:

```
python peano.py 6 4 800 --screen_x 10 --screen_y 10 --midi
```

🐍s & 👧