import os
from time import sleep
from pysinewave import SineWave
import sys
import argparse
import random
import math
import turtle 
import rtmidi

class Point:
    # paired (X,Y) coodinate developed from T
    # using Peano's construction

    # Peano's notation
    # T = 0 . a[1]a[2]a[3]...
    # X = 0 . b[1]b[2]b[3]...
    # Y = 0 . c[1]c[2]c[3]...
    # b[n] = k ^ (a[2] + a[4] ... a[2*n-2]) a[2*n-1]
    # c[n] = k ^ (a[1] + a[3] ... a[2*n-1]) a[2*n]
    
    # modified notation
    # T = 0 . a[0]a[1]a[2]...
    # X = 0 . b[0]b[1]b[2]...
    # Y = 0 . c[0]c[1]c[2]...
    # b[n] = k ^ (a[1] + a[3] ... a[2*n]) a[2*n]
    # c[n] = k ^ (a[0] + a[2] ... a[2*n+1]) a[2*n+1]

    def __init__(self, T):
        self.T = T
        self.X = self.calc_X() 
        self.Y = self.calc_Y()
    
    def calc_X(self):
        a = list(self.T)
        b = [0 for i in range(int(len(self.T) / 2))]
        for n in range(len(b)):
            e = 0                                       
            for i in range(2 * n):      
                if i % 2 != 0:
                    e += int(a[i])
            b[n] = k(int(a[2 * n]), e)
        X = ''.join(str(_) for _ in b)
        return X

    def calc_Y(self):
        a = list(self.T)
        c = [0 for i in range(int(len(self.T) / 2))]
        for n in range(len(c)):
            e = 0                                       
            for i in range(2 * n + 1):
                if i % 2 == 0:
                    e += int(a[i])
            c[n] = k(int(a[2 * n + 1]), e)
        Y = ''.join(str(_) for _ in c)
        return Y

class Number:
    # value T on real number line b/t 0 and 1
    # to produce (X,Y) in Peano's construction
  
    # Peano's notation
    # T = 0 . a[1]a[2]a[3]...
    # X = 0 . b[1]b[2]b[3]...
    # Y = 0 . c[1]c[2]c[3]...
    # a[2*n-1] = k ^ (c[1] + c[2] ... c[n-1]) b[n]
    # a[2*n] = k ^ (b[1] + b[2] ... b[n]) c[n]

    # modified notation
    # T = 0 . a[0]a[1]a[2]...
    # X = 0 . b[0]b[1]b[2]...
    # Y = 0 . c[0]c[1]c[2]...
    # a[2*n] = k ^ (c[0] + c[1] ... c[n-1]) b[n]
    # a[2*n+1] = k ^ (b[0] + b[1] ... b[n]) c[n]

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.T = self.calc_T()

    def calc_T(self):
        b = list(self.X)
        c = list(self.Y)
        a = [0 for i in range(int(len(self.X) * 2))]
        for n in range(len(b)):            
            e_b = 0     
            e_c = 0            
            for i in range(n):    
                e_b += int(c[i])
            a[2*n] = k(int(b[n]), e_b)
            for i in range(n+1):
                e_c += int(b[i])
            a[2*n+1] = k(int(c[n]), e_c)
        T = ''.join(str(_) for _ in a)
        return T

class MidiOutWrapper:
    # convenience wrapper for using rtmidi, channels 
    # see https://github.com/SpotlightKid/python-rtmidi/issues/38

    def __init__(self, midi, ch=1):
        self.channel = ch
        self._midi = midi

    def channel_message(self, command, *data, ch=None):
        """Send a MIDI channel mode message."""
        command = (command & 0xf0) | ((ch if ch else self.channel) - 1 & 0xf)
        msg = [command] + [value & 0x7f for value in data]
        self._midi.send_message(msg)

def to_base(n, b):
    # convert integer base 10 to base b 
    s = ''
    while n:
        s = str(n % b) + s
        n //= b
    return s

def from_base_fp(n_fp, b):
    # convert floating point base b to base 10 
    o = 0
    i = 0
    for fp in n_fp:
        i += 1
        o += int(fp) / (b ** i)
    return o

def is_power_of_3(n):
    while (n % 3 == 0):
        n /= 3
    return n == 1

def k(input, n):
    # k complement defined by Peano
    # 0 -> 2, 1 -> 1, 2 -> 0
    # repeated n times, flips on n odd || n even
    output = input
    for x in range(n):
        output = 2 - output
    return output

def generate_points(_n, _points, _precision):
    # generate T in loop of range(_points)
    # _n is number of T digits required to represent T
    # in base 3 for a given number_of_points
    # requires 2 * _n (padded with zeros)
    # log base 3 of the number of points = length,
    # also is equal to _n which is user input
    # for ex, 9 base 10 requires log (3) 9 = 2 digits
    # in python, no floating points allowed in base 3
    # therefore, all base 3 numbers in this program are 
    # represented without the leading '.' but implied to
    # fall in range 0 ... 1 required for Peano (Cantor set)
    # https://en.wikipedia.org/wiki/Cantor_set
    #
    # _points is always a power of 3 (specified in _n)

    print('Generating T values ...')
    print('Calculating points ...')

    points = []
    for n in range(_points):
        T = to_base(n, 3)
        T = T.rjust(_n, '0')
        T = T.ljust(_n * _precision, '0')   
        if len(T) % 2 != 0:             # T length must always be even
            T = T.ljust(len(T)+1, '0')  # to split into X and Y points
        point = Point(T);
        points.append(point)
    print('')
    display = '.{} -------> (.{} , .{})'
    display_convert = '.{} -------> (.{} , .{})    ({:.' + str(_precision) + 'f} , {:.' + str(_precision) + 'f})'
    for point in points:
        print(display.format(point.T, point.X, point.Y))
    print('')
    return points

def generate_numbers(_X, _Y):
    # generate T values for given points (_X,_Y)
    # all base 3 with no leading 0 or . (see above)
    # len(T) = 2 * len(_X) || 2 * len(_Y)

    print('Generating T values ...')
    
    numbers = []
    for n in range(len(_X)):
        number = Number(_X[n], _Y[n]);
        numbers.append(number)
    print('')
    display = '(.{} , .{}) -------> .{}'
    for number in numbers:
        print(display.format(number.X, number.Y, number.T))
        # print(display.format(from_base_fp(number.X, 3), from_base_fp(number.Y, 3), from_base_fp(number.T, 3)))
    print('')
    _proceed = input('Proceed? ') or 'y' 
    return numbers

def init_display(_display, title, _screen):
    turtle.setup(_display + 4, _display + 8, _screen[0], _screen[1])  
    turtle.setworldcoordinates(0, 0, _display, _display)
    turtle.title(title)
    return True

def init_midi(port):
    midi = rtmidi.MidiOut()
    available_ports = midi.get_ports()
    if available_ports:
        midi.open_port(0)
    else:
        midi.open_virtual_port("virtual port")
        # print("Error -- no MIDI port available")
    return midi

def stop_midi(midi):
    midi.close_port()
    del midi

def init_midi_notes(start_note, octaves):
    # build midi notes in a C major scale over octaves  
    # middle_c = 60, low C = 48 ... (1 octave = 12)
    # can start from any other note to switch key
    # remains in a major scale
    # notes[] is used as a lookup for point.X and point.Y
    # when triggering midi

    notes = []
    note = start_note
    notes.append(note)
    for _ in range(octaves):
        for n in range(7):
            if n == 3 or n == 6:
                note += 1
            else:
                note += 2
            notes.append(note)
    print(notes)
    return notes

def export_eps_numbered(_count):
    screen = turtle.getscreen()
    screen.getcanvas().postscript(file='out/peano-' + str(_count) + '.eps')
    return True

def draw_points(points, _display, previous, _count, points_extra, _speed, sinewave, midi, notes):
    export_eps = False                  # export sequenced .eps 
    point_previous = Point('0')         # init
    i = 0                               # counter

    # turtle.tracer(3**(_count-1),0)    # close but not quite working correctly
    t = turtle.Pen()
    t.speed(_speed)
    t.hideturtle()
    t.pendown()
    if not export_eps:
        t_extra = turtle.Pen()
        t_extra.speed(0)
        t_extra.hideturtle()
        t_extra.pencolor(0,0,1)
        t_extra.penup()
        if previous:
            t_previous = turtle.Pen()
            t_previous.hideturtle()
            t_previous.pencolor(1,1,1)
            t_previous.pensize(4)
            t_previous.speed(0)
            t_previous.pendown()
            t.goto(0,0)
            j = 1
        for point_extra in points_extra:
            X = from_base_fp(point_extra.X,3) * _display
            Y = from_base_fp(point_extra.Y,3) * _display
            t_extra.goto(X, Y)
            t_extra.dot()

    for point in points:
        if not export_eps:
            if previous:
                if i % 3 == 0 and j < len(previous):
                    x_previous = from_base_fp(previous[j].X,3) * _display
                    y_previous = from_base_fp(previous[j].Y,3) * _display
                    t_previous.goto(x_previous,y_previous)
                    j += 1
        x = from_base_fp(point.X,3) * _display
        y = from_base_fp(point.Y,3) * _display
        for point_extra in points_extra:
            T = from_base_fp(point_extra.T,3)
            _T = from_base_fp(point_previous.T,3)
            T_ = from_base_fp(point.T,3)
            if T > _T and T <= T_:
                t.pencolor(1,0,0)
                t.dot()
        t.goto(x,y)
        # t.dot()
        t.pencolor(0,0,0)
        # display = 'T -------> {})'
        # os.system('clear')
        # print(display.format(from_base_fp(point.T, 3)))
        point_previous = point

        # MIDI messages 
        # note_on: 0x90, note_off: 0x80, control_change: 0xB0 
        # channel_change: 0x80 | channelnumber
        
        # move to contained function?

        if midi:
            x_note = int(from_base_fp(point.X,3) * len(notes))
            y_note = int(from_base_fp(point.Y,3) * len(notes))
            midi.channel_message(0x90, notes[x_note], 112, ch=1)
            midi.channel_message(0x90, notes[y_note], 112, ch=2)
            sleep(0.125)
            midi.channel_message(0x80, notes[x_note], 0, ch=1)
            midi.channel_message(0x80, notes[y_note], 0, ch=2)
            sleep(0.0125)
        elif sinewave:
            x_pitch = from_base_fp(point.X,3) * 12 * 10 - 48
            y_pitch = from_base_fp(point.Y,3) * 12 * 10 - 48
            sinewave[0].set_pitch(x_pitch)
            sinewave[1].set_pitch(y_pitch) 
            sinewave[0].play()
            sinewave[1].play()
        i += 1
        
    if export_eps:
        export_eps_numbered(_count)
        t.clear()
    # t_extra.clear()
    return True

def main():
    # plot Peano curve of 3^n points using turtle graphics
    # arguments on command line or input interactive
    #
    # python peano.py 1 4 400 100 100
    # python peano.py

    _n = 0              # power of 3 used to generate _points
                        # '*' runs iteratively 3^n _points
    _precision = 4      # T _n significant digits multiplier
    _display = 100      # display h, w in px
    _points = 0         # number of (X,Y) points to generate
    _count = 0          # number of draw loops in iterative mode
    _extra = []         # additional (x,y) coordinates
    _X = ''             # X to calc T in Number mode
    _Y = ''             # Y to calc T in Number mode
    _screen_x = 0       # window offset
    _screen_y = 0       # window offset
    _speed = 0          # 0 (fast as possible) or 1 (slow) - 9 (fast)
    _sound = 'none'     # 'none', 'sinewave', 'midi'  

    welcome = 'P E A N O for 🐍s & 👧s'
    delay = .25 / 5     # opening sequence
    sinewave = None     # init using pysinewave
    midi = None         # init using rtmidi
    notes = None        # init midi notes

    # https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument('_n', help='number of points as power of 3')
    parser.add_argument('_precision', help='length of T, determines accuracy of (X,Y) values', type=int)
    parser.add_argument('_display', help='window size in px', type=int)
    parser.add_argument('--screen_x', help='window screen X position in px', type=int)
    parser.add_argument('--screen_y', help='window screen X position in px', type=int)
    parser.add_argument('--speed', help='turtle drawing speed, 0 (fast as possible), 1 (slow) - 9 (fast)', type=int)
    parser.add_argument('--sinewave', help='use rtmidi to generate midi data sent on virtual port', action='store_true')
    parser.add_argument('--midi', help='use rtmidi to generate midi data sent on virtual port', action='store_true')

    os.system('clear')
    for i in range(9):
        os.system('clear')
        print(welcome)
        print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
        sleep(delay)
    os.system('clear')
    sleep(delay)

    if sys.argv[1:]:
        args = parser.parse_args()
        _n = args._n
        _precision = args._precision
        _display = args._display
        if args.screen_x:
            _screen_x = args.screen_x
        if args.screen_y:
            _screen_y = args.screen_y
        if args.speed:
            _speed = args.speed
        if args.midi:
            _sound = 'midi'
        elif args.sinewave:
            _sound = 'sinewave'
    else:    
        _n = input('Points (3^n): ') or '*'
        _precision = int(input('Precision: ') or '4')            
        _display = int(input('Display: ') or '400')
        if _n == '+':
            print('Extra points (. to exit):')
            while _X != '.':
                _X = input('X : ') or '100000'
                _Y = input('Y : ') or '100000'                    
                if _X != '.' and _Y != '.':
                    _extra.append({'x':_X, 'y':_Y})
    _screen = (_screen_x, _screen_y)
    display = init_display(_display, welcome, _screen)

    # pysinewave
    # create sinewaves (panned to left and right)
    # using pysinewave module local version included in this repository
    # as it has support for channels and pip version does not
    # see https://github.com/daviddavini/pysinewave

    # python-rtmidi
    # https://github.com/SpotlightKid/python-rtmidi
    # python wrapper for C library to send MIDI messages over virtual port
    # using virtual port IAC, which is created in Audio Midi Setup
    # using Ableton Live to receive MIDI messages
    # MIDI is sent on channel 1 (X) and channel 2 (Y)
    # configure Live to receive from IAC as desired

    if _sound == 'midi':
        midi_port = init_midi(0)
        midi = MidiOutWrapper(midi_port)
        if midi:
            notes = init_midi_notes(48, 3)
    elif _sound == 'sinewave':
        left = SineWave(pitch = 12, pitch_per_second = 1000000, channels = 2, channel_side = "l")
        right = SineWave(pitch = 12, pitch_per_second = 1000000, channels = 2, channel_side = "r")
        sinewave = (left, right)

    if _n == '*' or _n == '+':
        # draw extra points
        points_extra = []
        if _n == '+':
            _x = [x['x'] for x in _extra]
            _y = [y['y'] for y in _extra]
            points_extra = generate_numbers(_x, _y)

        # run iteratively
        previous = []
        for n in range(1000):
            _points = 3 ** n            
            points = generate_points(n, _points, _precision)
            if _precision == 0:
                if _count % 2 == 0:
                    draw = draw_points(points, _display, previous, _count, points_extra, _speed, sinewave, midi, notes)
            else:
                draw = draw_points(points, _display, previous, _count, points_extra, _speed, sinewave, midi, notes)
            previous = points
            _count += 1
    else:
        _points =  3 ** int(_n)
        points = generate_points(int(_n), _points, _precision)
        points_extra = []
        draw = draw_points(points, _display, False, _count, points_extra, _speed, sinewave, midi, notes)
        turtle.done()
    stop_midi()
    exit()

main()
