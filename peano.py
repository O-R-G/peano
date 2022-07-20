import os
from time import sleep
import sys
import random
import math

class Point:
    def __init__(self, T):		
        self.T = T
        self.X = self.calc_X(T) 
        self.Y = self.calc_Y(T)
    
    def calc_X(self, t):
        # requires implememtation
        t = k(0, 1)        
        return t

    def calc_Y(self, t):
        # requires implememtation
        t = k(1, 2)
        return t

def k(input, n):
    # k (complement)
    # mapping as defined by Peano
    # 0 -> 2, 1 -> 1, 2 -> 0
    # repeated n times, flipping output if n odd or even        
    output = input
    for x in range(n):
        output = 2 - output
    return output

def base(n, b):
    s = ''
    while n:
        s = str(n % b) + s
        n //= b
    # s = s.zfill(l)
    return s

def is_power_of_three(n):
    while (n % 3 == 0):
        n /= 3
    return n == 1

def main():
    # delay = .25
    delay = .001
    welcome = 'P E A N O for pythons and edens'
    os.system('clear')
    for i in range(3):
        os.system('clear')
        print(welcome)
        print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
        sleep(delay)
    os.system('clear')
    sleep(delay)

    # number_of_points must be a power of 3
    while True:
        number_of_points = int(input('Number of points: '),10)
        if not is_power_of_three(number_of_points):
            print('** Number of points must be a power of 3 **')
        else:
            break

    # generate T in loop of range(number_of_points)
    # and make points with T

    # length is number of significant digits of T required
    # to represent T in base 3 for a given number_of_points
    # pad out the string with two zeros on the end (?)
    # requires 2 * significant_digits (padded with zeros)
    # log base 3 of the number of points = significant_digits

    # in python, no decimals allowed except base 10 (!)
    # therefore, manually implement base 3 addition
    # for ex, 9 base 10 requires log (3) 9 = 2 digits

    # print('Generating T values ...')

    length = int(math.log(number_of_points, 3))
    print('Length :', length)

    points = []
    for i in range(number_of_points):
        T = base(i, 3)
        T = T.rjust(length, '0')      # pad zeros start
        T = T.ljust(length * 2, '0')  # pad zeros end
        point = Point(T);
        points.append(point)

    # print('Calculating points ...')

    # could rjust pad this or use tabs
    print('T -------> ( X , Y )')
    print('')
    for point in points:
        #  os.system('clear')
        print('.', point.T, ' -------> (', point.X, ',', point.Y, ')')
        sleep(delay*100)
    print('')

main()
