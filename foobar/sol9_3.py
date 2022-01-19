
def new_mat(r_size, c_size):
    ret = [[None for _ in range(c_size)] for _ in range(r_size)]
    return ret


def to_tuple(m):
    return tuple([tuple(row) for row in m])

def set_int_mat(m, m2, y):
    r_size = len(m2)

    flag = False
    for i in range(r_size):
        if m[y + i] != None:
            if m[y + i] != m2[i]:
                flag = True
                #return flag
        m[y + i] = m2[i]
    return flag



def resize(g, r, c):
    ret = [[False for _ in range(c)] for _ in range(r)]
    for i in range(len(g)):
        for j in range(len(g[0])):
            ret[i][j] = g[i][j]
    return ret


def copy_int_mat(g):
    return g[:]

class Item:
    def __init__(self, m, x, y):

        #self.m = copy(m)
        self.m = m
        self.x = x
        self.y = y
        self.cnt = 0


def next_int(x, y, size):
    mask = (1 << (size -1)) - 1

    v1 = x
    v2 = x >> 1
    v3 = y
    v4 = y >> 1

    return ((v1 & ~v2 & ~v3 & ~v4) | (~v1 & v2 & ~v3 & ~v4) | (~v1 & ~v2 & v3 & ~v4) | (~v1 & ~v2 & ~v3 & v4)) & mask

def next_cell_int(m, y, size):
    return next_int(m[y], m[y+1], size)

def next_int_mat(m, size):
    r_size = len(m)

    m_next = [0 for _ in range(r_size)]
    for i in range(r_size - 1):
        m_next[i] = next_cell_int(m, i, size)
    return m_next

def create_bit_dict(size):
    d = {}


    n = 2 << size
    mask = (2 << size) - 1
    for i in range(n):
        for j in range(i, n):
            v = next_int(i, j, size+1)
            
            if v in d:
                d[v].add( (i, j) )
                d[v].add( (j, i))
            else:
                d[v] = set([ (i, j), (j, i) ])

    return d

def to_bits(n, size):
    bits = []
    for i in range(size):
        if n & (1 << i) > 0:
            bits.append(True)
        else:
            bits.append(False)
    return bits

def to_int(bits):
    def f(b):
        if b:
            return 1
        else:
            return 0
    n = 0
    for i, b in enumerate(bits):
        n += f(b) << i
    n = n & (2 ** len(bits) - 1)
    return n

def transpose(m):
    r_size = len(m)
    c_size = len(m[0])
    m2 = new_mat(c_size, r_size)

    for i in range(r_size):
        for j in range(c_size):
            m2[j][i] = m[i][j]
    return m2

def int_mat(m):
    return [to_int(row) for row in m]

def new_int_mat(r_size):
    return [None for _ in range(r_size)]

def tr(g):
    r_size = len(g)
    c_size = len(g[0])
    g = to_tuple(transpose(resize(g, r_size+1, c_size+1)))

    r_size = len(g)
    c_size = len(g[0])

    g = tuple(int_mat(g))

    d = create_bit_dict(c_size-1)

    def next(item):
        global cnt
        m = item.m

        for m2 in d[g[item.y]]:
            
            _m = copy_int_mat(m)
            
            if set_int_mat(_m, m2, item.y):
                continue
            
            if (r_size - 2 == item.y):
                if True:
                    cnt += 1

            if item.y + 2 < r_size:
                yield Item(_m, item.x, item.y + 1)

    global cache
    cache = {}

    def df(item):
        global cache
        if (item.y, item.m[item.y]) in cache:

            return cache[(item.y, item.m[item.y])]
        global cnt
        cnt = 0
        for item2 in next(item):
            cnt += df(item2)

        cache[(item.y, item.m[item.y])] = cnt
        #pass
        return cnt
    
    item = Item(new_int_mat(r_size), 0, 0)
    cnt = df(item)

    return cnt

def solution(g):

    return tr(g)



print(1, solution([
    [True, True, False, True, False, True, False, True, True, False], 
    [True, True, False, False, False, False, True, True, True, False], 
    [True, True, False, False, False, False, False, False, False, True], 
    [False, True, False, False, False, False, True, True, False, False]]))

print(2, solution([
    [True, False, True], 
    [False, True, False], 
    [True, False, True]]))

print(2, solution([
    [False, False, False], 
    [False, False, False], 
    [False, False, False]]))


print(3, solution([
    [True, False, True, False, False, True, True, True], 
    [True, False, True, False, False, False, True, False], 
    [True, True, True, False, False, False, True, False], 
    [True, False, True, False, False, False, True, False], 
    [True, False, True, False, False, True, True, True]]))

print(4, solution([
    [True, True, False, True, False, True, False, True, True, False], 
    [True, True, False, False, False, False, True, True, True, False], 
    [True, True, False, False, False, False, False, False, False, True], 
    [False, True, False, False, False, False, True, True, False, False],
    [True, True, False, True, False, True, False, True, True, False], 
    [True, True, False, False, False, False, True, True, True, False], 
    [True, True, False, False, False, False, False, False, False, True], 
    [False, True, False, False, False, False, True, True, False, False]]))




