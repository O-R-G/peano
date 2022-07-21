import os
from time import sleep
import sys
import random
import math

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

def base(n, b):
    s = ''
    while n:
        s = str(n % b) + s
        n //= b
    return s

def is_power_of_three(n):
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
    # significant_digits is number of T digits required
    # to represent T in base 3 for a given number_of_points
    # requires 2 * significant_digits (padded with zeros)
    # log base 3 of the number of points = length
    # for ex, 9 base 10 requires log (3) 9 = 2 digits
    # in python, no decimals allowed except base 10 
    # therefore, manually implement base 3 addition

    print('Generating T values ...')
    significant_digits = int(math.log(number_of_points, 3))
    points = []
    for n in range(number_of_points):
        T = base(n, 3)
        T = T.rjust(significant_digits, '0')      # pad start
        T = T.ljust(significant_digits * 2, '0')  # pad end
        point = Point(T);
        points.append(point)
    print('Calculating points ...')
    print('')
    for point in points:
        #  os.system('clear')
        print(point.T, ' -------> (', point.X, ',', point.Y, ')')
        sleep(delay)
    print('')

main()
