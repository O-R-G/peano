import os
from time import sleep
import sys
import random
import math
import turtle 

class Point:
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

def is_power_of_9(n):
    while (n % 9 == 0):
        n /= 9
    return n == 1

def k(input, n):
    # k complement defined by Peano
    # 0 -> 2, 1 -> 1, 2 -> 0
    # repeated n times, flips on n odd || n even
    output = input
    for x in range(n):
        output = 2 - output
    return output

def generate_points(_points, _precision):
    # generate T in loop of range(_points)
    # significant_digits is number of T digits required
    # to represent T in base 3 for a given number_of_points
    # requires 2 * significant_digits (padded with zeros)
    # log base 3 of the number of points = length,
    # for ex, 9 base 10 requires log (3) 9 = 2 digits
    # in python, no floating points allowed in base 3
    # therefore, all base 3 numbers in this program are 
    # represented without the leading '.' but implied to
    # fall in range 0 ... 1 required for Peano (Cantor set)
    # https://en.wikipedia.org/wiki/Cantor_set
    #
    # _points is always a power of 9 (specified in _detail)

    print('Generating T values ...')
    print('Calculating points ...')
    significant_digits = int(math.log(_points, 3))
    points = []
    for n in range(_points):
        T = to_base(n, 3)
        T = T.rjust(significant_digits, '0')
        T = T.ljust(significant_digits * _precision, '0')
        point = Point(T);
        points.append(point)
    print('')
    display = '.{} -------> (.{} , .{})'
    display_convert = '.{} -------> (.{} , .{})    ({:.' + str(_precision) + 'f} , {:.' + str(_precision) + 'f})'
    for point in points:
        print(display.format(point.T, point.X, point.Y))
        # print(display_convert.format(point.T, point.X, point.Y, from_base_fp(point.X,3), from_base_fp(point.Y,3)))
    print('')
    return points

def init_display(_display, title):
    turtle.setup(_display + 4, _display + 8)  
    # turtle.setup(_display + 4, _display + 8, 400, 200)
    turtle.setworldcoordinates(0, 0, _display, _display)
    turtle.title(title)
    return True

def draw_points(points, _display):
    t = turtle.Pen()
    t.speed(10)
    t.pendown()
    for point in points:
        x = from_base_fp(point.X,3) * _display
        y = from_base_fp(point.Y,3) * _display
        t.goto(x,y)
    return True

def main():
    # plot Peano curve of 9^n points using turtle graphics
    # arguments on command line or input interactive
    #
    # python peano.py 1 400 4
    # python peano.py

    _points = 0         # number of (X,Y) points to generate
    _detail = 0         # power of 9 to generate _points
                        # '*' runs iteratively 9^n _points
    _display = 100      # display h, w in px
    _precision = 4      # T significant_digits multiplier

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
        _detail = sys.argv[1] 
        _display = int(sys.argv[2])
        _precision = int(sys.argv[3])
        print(sys.argv[1:])
    else:    
        _detail = input('Detail: ') or '1'
        _display = int(input('Display: ') or '400')
        _precision = int(input('Precision: ') or '4')

    display = init_display(_display, welcome)

    if _detail == '*':
        # run iteratively
        for n in range(100):
            _points = 9 ** n            
            points = generate_points(_points, _precision)
            draw = draw_points(points, _display)   
    else:
        _points = 9 ** int(_detail)            
        points = generate_points(_points, _precision)
        draw = draw_points(points, _display)
        turtle.done()
    exit()

main()
