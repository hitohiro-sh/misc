
from decimal import *

def sqrt2_n(n):
    getcontext().prec = 101
    a = Decimal(1)
    for _ in range(n):
        a = (a / 2) + (1 / a)

    return a

sqrt2 = sqrt2_n(10)
print('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157')
print(len('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157'))
print(sqrt2)

def sn(n):
    if n == 0:
        return 0

    def g(n):
        #return int (math.sqrt(n * n * 2) - n)
        return int(n * (sqrt2 - 1))

    y = g(n)
    x = n + y

    return x * (x + 1) // 2 - sn(y) - y * (y + 1)

def solution(s):
    #sqrt2 = sqrt2_n(15)
    #print(sqrt2)
    return str(sn(int(s)))

print(1, solution('5'))
print(2, solution('77'))
print(3, solution('10000'))
print(2, solution(str(10 ** 8)))
print(2, solution(str(10 ** 10)))
print(2, solution(str(10 ** 20)))
print(4, solution(str(10 ** 100)))

    