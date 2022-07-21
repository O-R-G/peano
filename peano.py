import os
from time import sleep
import sys
import random
import math

class Point:
    def __init__(self, T):
        self.T = T
        self.X = self.calc_X() 
        self.Y = self.calc_Y(T)
    
    def calc_X(self):
        # calc digits of X (left to right) from T
        # following Peano's notation

        # T = 0 . a[1]a[2]a[3]...
        # X = 0 . b[1]b[2]b[3]...
        # Y = 0 . c[1]c[2]c[3]...

        # b[n] = k ^ (a[2] + a[4] ... a[2n-2]) a[2n-1]
        
        # with the exception that for arrays 0 is first member
        # so here all indices in Peano are shifted -1
        # but since range does not include the top value
        # when iterating, also 2n-2 --> 2n-1 and 2n-1 ---> 2n

        # T = 0 . a[0]a[1]a[2]...
        # X = 0 . b[0]b[1]b[2]...
        # Y = 0 . c[0]c[1]c[2]...

        # b[n] = k ^ (a[1] + a[3] ... a[2*n-1]) a[2*n]
    
        X = ''                                          # string
        a = list(self.T)                                # digits of T
        b = [0 for i in range(int(len(self.T) / 2))]    # digits of X

        # iterate through b (digits of X)

        print('T :', self.T)

        for n in range(len(b)):
            e = 0               # k exponent sum or how many times to repeat k()
            i = 0               # counter
    
            print('  n :', n)

            # sum exponents
            # or could have var for 2n-1 and check if greater than 0
            # although actually ranges in python always are positive, see
            # https://www.google.com/search?client=safari&rls=en&q=python+negative+value+for+range&ie=UTF-8&oe=UTF-8
            # so perhaps leave without the catch condition
            # maybe better name for k_sum_exp
            # here 2 * n not 2 * n - 1 because range doesnt ever get to top value
            # so putting 2 * n has the result of 2 * n - 1

            for i in range(2 * n):
                if i % 2 != 0:
                    e += int(a[i])
            
            ###############
            # ** k not quite working correctly, likely to do with repeats **
            ###############

            b[n] = k(int(a[2 * n]), e)

            X += str(b[n])      # better to iterate thru b[] to populate X? or shortcut 
                                # compress list to string like flatten

            print('    a[', 2 * n, '] :', a[2 * n])
            print('    e :', e)
            print('    k(', a[n], ',', e, ') :', b[n])
            
        print('X :', X)
        print('')
            
        # return X
        return 1

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
    for n in range(number_of_points):
        T = base(n, 3)
        T = T.rjust(length, '0')      # pad zeros start
        T = T.ljust(length * 2, '0')  # pad zeros end
        point = Point(T);
        points.append(point)

    # print('Calculating points ...')

    # print results

    # could rjust pad this or use tabs
    # print('T -------> ( X , Y )')
    # print('')
    # for point in points:
        #  os.system('clear')
    #    print('.', point.T, ' -------> (', point.X, ',', point.Y, ')')
    #    sleep(delay)
    # print('')

main()
