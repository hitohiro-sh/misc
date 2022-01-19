

import math

from fractions import Fraction

# n + (sqrt - 1) * n


def g(n):
    return int(math.floor(math.sqrt(2) * n * (n + 1) // 2))

def g2(n):
    return int(math.floor(math.sqrt(2) * n * n // 2))

def g3(n):
    return int(math.sqrt(2 * n * n))

def g4(n):
    return n * math.sqrt(2)

def h(n):
    return int(n * (n + 1) // 2)

def f(n):
    total = 0
    i = 0
    # cnt = 0
    sqrt2 = sqrt2_n(5)

    while i < n:
        #v = int(math.floor((i + 1) * math.sqrt(2)))
        v = int((i+1) * sqrt2)
        #if v - v2 == 2:
        #    cnt += 1
        total += v
        #print(total)
        #print(i+1, h(i+1), g(i+1), total, g2(i+1))
        
        i += 1

    return total



def sqrt2_n(n):
    a = Fraction(1)
    for _ in range(n):
        a = (a / 2) + (1 / a)

        #print(a)
    return a

def solution(s):
    v = f(int(s))
    
    #print(sqrt2_n(6) * (10 ** 100))

    return str(v)

print(1, solution('5'))
#print(1, solution('10'))
#print(1, solution('100'))
print(2, solution('77'))

print(2, solution('10000'))
print(2, solution(str(10 ** 8)))
#print(3, solution(str(10 ** 100)))
