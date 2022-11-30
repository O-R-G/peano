import os
from time import sleep
import sys
import random
import math
import turtle 

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
        T = T.ljust(_n * _precision, '0')   # ** fix **
        point = Point(T);
        points.append(point)
    print('')
    display = '.{} -------> (.{} , .{})'
    display_convert = '.{} -------> (.{} , .{})    ({:.' + str(_precision) + 'f} , {:.' + str(_precision) + 'f})'
    for point in points:
        # os.system('clear')
        print(display.format(point.T, point.X, point.Y))
        # print(display_convert.format(point.T, point.X, point.Y, from_base_fp(point.X,3), from_base_fp(point.Y,3)))
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
    return numbers

def init_display(_display, title):
    turtle.setup(_display + 4, _display + 8)  
    turtle.setworldcoordinates(0, 0, _display, _display)
    turtle.title(title)
    # turtle.tracer(2,0)      # speedup, draw every 2 frames
    # turtle.tracer(3,0)    # speedup, draw every 3 frames
    turtle.tracer(9,0)    # speedup, draw every 9 frames
    # turtle.tracer(81,0)    # speedup, draw every 9 frames
    # turtle.tracer(243,0)    # speedup, draw every 9 frames
    # turtle.tracer(0,0)    # speedup, draw every 9 frames
    # turtle.tracer(10,0)    # speedup, draw every 9 frames
    # turtle.tracer(20,0)    # speedup, draw every 9 frames
    return True

def draw_points(points, _display, previous, _count, points_extra):
    # turtle.tracer(3**(_count-1),0)    # close but not quite working correctly
    t = turtle.Pen()
    t.speed(0)
    t.pendown()
    t.hideturtle()
    if previous:
        t_previous = turtle.Pen()
        t_previous.hideturtle()
        t_previous.pencolor(1,1,1)
        t_previous.pensize(4)
        t_previous.speed(0)
        t_previous.pendown()
        t.goto(0,0)
        j = 1
    i = 0
    point_previous = Point('0')
    for point in points:
        if previous:
            if i % 3 == 0 and j < len(previous):
                x_previous = from_base_fp(previous[j].X,3) * _display
                y_previous = from_base_fp(previous[j].Y,3) * _display
                # t_previous.goto(x_previous,y_previous)
                j += 1
        x = from_base_fp(point.X,3) * _display
        y = from_base_fp(point.Y,3) * _display

        # ** fix ** calculate a more precise position on the line
        # using turtle functions position() and distance()
        # also erase previous dot?
        # or draw lines connecting red dots?
        for point_extra in points_extra:
            if from_base_fp(point_extra.T,3) >= from_base_fp(point_previous.T,3) \
            and from_base_fp(point_extra.T,3) <= from_base_fp(point.T,3):
                t.dot(_display / 50, 'red')
        t.goto(x,y)
        display = 'T -------> {})'
        os.system('clear')
        print(display.format(from_base_fp(point.T, 3)))
        point_previous = point
        i += 1
    return True

def main():
    # plot Peano curve of 3^n points using turtle graphics
    # arguments on command line or input interactive
    #
    # python peano.py 1 4 400
    # python peano.py

    _n = 0              # power of 3 used to generate _points
                        # '*' runs iteratively 3^n _points
    _precision = 4      # T _n significant digits multiplier
    _display = 100      # display h, w in px
    _points = 0         # number of (X,Y) points to generate
    _count = 0          # number of draw loops in iterative mode
    _extra = []         # additional (x,y) coordinates
    points_extra = []   # additional points to draw

    X = ''              # X to calc T in Number mode
    X_prime = ''        # X' to calc T in Number mode
    Y = ''              # Y to calc T in Number mode
    Y_prime = ''        # Y' to calc T in Number mode

    delay = .25 / 5
    welcome = 'P E A N O for 🐍s & 👧s'
    os.system('clear')
    for i in range(9):
        os.system('clear')
        print(welcome)
        print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
        sleep(delay)
    os.system('clear')
    sleep(delay)   

    if sys.argv[1:]:
        _n = sys.argv[1] 
        _precision = int(sys.argv[2])
        _display = int(sys.argv[3])
        print(sys.argv[1:])
    else:    
        _n = input('Points (3^n): ') or '1'
        _precision = int(input('Precision: ') or '4')            
        _display = int(input('Display: ') or '400')
        if _n == '+':
            print('Extra points (. to exit):')
            while X != '.':
                X = input('X : ') or '100000'
                Y = input('Y : ') or '100000'                    
                if X != '.' and Y != '.':
                    _extra.append({'x':X, 'y':Y})
    display = init_display(_display, welcome)

    if _n == '*' or _n == '+':
        # draw extra points
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
                    draw = draw_points(points, _display, previous, _count, points_extra)
            else:    
                draw = draw_points(points, _display, previous, _count, points_extra)
            previous = points
            _count += 1
    else:
        _points =  3 ** int(_n)  
        points = generate_points(int(_n), _points, _precision)
        draw = draw_points(points, _display, False, _count, points_extra)
        turtle.done()
    exit()

main()
