
def tr(x, y, g_x, g_y,step):

    while True:
        n = 1
        if (x, y) == (g_x, g_y):
            return step, True
        elif x < 1 or y < 1:
            return -1, False
        else:
            if x < y:
                # y = y - x
                if y % x != 0:
                    n = y // x
                else:
                    if x != 1:
                        n = y // x
                y = y - n * x
            else:
                # x = x - y
                if x % y != 0:
                    n = x // y
                else:
                    if y != 1:
                        n = x // y
                x = x - n * y
        step += n

def solution(x, y):
    #st = [1,1]

    ret = tr(int(x),int(y), 1, 1, 0)
    if not ret[1]:
        return 'impossible'
    #print(ret)
    return str(ret[0])

print(solution('2','1'))
print(solution('4','7'))
print(solution('4','2'))
print(solution('2','4'))
print(solution('1','1'))
print(solution('1','0'))
print(solution('156','1111'))
#print(solution(str(2 ** 250),str(2 ** 65)))


#print(str_lt('0','1'))
