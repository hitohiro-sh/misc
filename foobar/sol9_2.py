


def to_str_mat(m):
    def f(v):
        if v:
            return '1'
        else:
            return '0'

    return '\n'.join([''.join([f(v) for v in row]) for row in m])

#def mat(m, x, y, r_size, c_size):
#    return m[x:x+r_size][y:y+c_size]

def new_mat(r_size, c_size):
    ret = [[None for _ in range(c_size)] for _ in range(r_size)]
    return ret
'''
def print_mat(m):
    def f(v):
        if v == None:
            return 'x'
        if v:
            return '1'
        else:
            return '0'
    print('[')
    print('\n'.join([''.join([f(v) for v in row]) for row in m]))
    print(']')
'''
def to_tuple(m):
    return tuple([tuple(row) for row in m])


def next_cell(g, i, j):
    r_size = len(g)
    c_size = len(g[0])

    cnt = 0
    flag = False
    if j+1 < c_size and i+1 < r_size:
        if g[i][j]:
            cnt += 1
        if g[i][j+1]:
            cnt += 1
        if g[i+1][j]:
            cnt += 1
        if g[i+1][j+1]:
            cnt += 1
        if cnt == 1:
            flag = True
    return flag

def next_mat(g):
    r_size = len(g)
    c_size = len(g[0])

    #return [ [has_one(i, j) for j in range(c_size)] for i in range(r_size) ]
    return [ [next_cell(g, i, j) for j in range(c_size)] for i in range(r_size) ]

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

# return True if rewrite True cell
def set_mat(m, m2, x, y):
    r_size = len(m2)
    c_size = len(m2[0])

    #print('x', x, 'y', y, r_size, c_size)
    #print_mat(m2)
    flag = False
    for i in range(r_size):
        for j in range(c_size):
            if m[x + i][y + j] != None:
                if m[x + i][y + j] != m2[i][j]:
                    flag = True
            m[x + i][y + j] = m2[i][j]

    return flag

def iter_bit(r_size, c_size):
    from itertools import product
    for bits in product([False, True], repeat=r_size * c_size):
        yield [list(bits[i * c_size:(i+1) * c_size]) for i in range(r_size)]
        #yield bits

def resize(g, r, c):
    ret = [[False for _ in range(c)] for _ in range(r)]
    for i in range(len(g)):
        for j in range(len(g[0])):
            ret[i][j] = g[i][j]
    return ret

def copy(g):
    return [row[:] for row in g]

def copy_int_mat(g):
    return g[:]

class Item:
    def __init__(self, m, x, y):

        #self.m = copy(m)
        self.m = m
        self.x = x
        self.y = y

def create_mat_dict(size):
    d = {}
    for mat in iter_bit(size+1, size+1):
        g = to_tuple(next_mat(mat))
        if g in d:
            d[g].append(mat)
        else:
            d[g] = [mat]


global next_dict
next_dict = {}

def next_int(x, y, size):
    if (x, y) in next_dict:
        return next_dict[(x,y)]

    mask = (1 << (size -1)) - 1

    v1 = x
    v2 = x >> 1
    v3 = y
    v4 = y >> 1

    def f1(v1, v2, v3, v4, i):
        cnt = 0
        '''
        if v1 & (1 << i) > 0:
            cnt += 1
        if v2 & (1 << i) > 0:
            cnt += 1
        if v3 & (1 << i) > 0:
            cnt += 1
        if v4 & (1 << i) > 0:
            cnt += 1
        '''
        cnt = (v1 >> i & 1)+(v2 >> i & 1)+(v3 >> i & 1)+(v4 >> i & 1)
        if cnt == 1:
            return (1 << i)
        else:
            return 0

    n = 1 << (size - 1)
    _v1 = 0
    for i in range(n):
        _v1 += f1(v1, v2, v3, v4, i)
    _v1 = _v1 & mask
    #if _v1 != _next_int(x, y, size):
    #    print(x,y,_v1, size, _next_int(x, y, size))
    next_dict[(x,y)] = _v1
    return _v1

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
        for j in range(n):
            v = next_int(i, j, size+1)
            if v in d:
                d[v].append( (i, j) )
            else:
                d[v] = [ (i, j) ]

    return d

def create_bit_dict2(size):
    d = {}

    n = 2 << size
    mask = (2 << size) - 1
    for i in range(n):
        for j in range(n):
            for k in range(n):
                v1 = next_int(i, j, size+1)
                v2 = next_int(j, k, size+1)
                if (v1,v2) in d:
                    d[(v1,v2)].append( (i, j, k) )
                else:
                    d[(v1,v2)] = [ (i, j, k) ]

    return d

def create_cell_dict(d):
    d2 = {}
    d2[True] = []
    d2[False] = []
    for k,v in d.items():
        d2[k[0][0]].extend(v)

    #print(d2)
    return d2


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
    #g = to_tuple(resize(g, r_size+1, c_size+1))
    r_size = len(g)
    c_size = len(g[0])

    g = tuple(int_mat(g))
    #print(g)
    # print(int_mat(g))
    #for row in g:
    #    print(row)
    #    print(to_int(row))
    #    print(to_bits(to_int(row), c_size))

    d = create_bit_dict(c_size-1)
    d2 = create_bit_dict2(c_size-1)
    #print(d2)
    #for k,v in d.items():
    #    print(k,v)

    queue = []

    global cnt
    cnt = 0
    
    #init
    queue.append(Item(new_int_mat(r_size), 0, 0))

    def next(item):
        global cnt
        m = item.m

        ret = []

        for m2 in d[g[item.y]]:
            
            _m = copy_int_mat(m)
            
            if set_int_mat(_m, m2, item.y):
                continue
            if next_cell_int(_m, item.y, c_size) != g[item.y] or \
                (item.y > 0 and next_cell_int(_m, item.y-1, c_size) != g[item.y - 1]) or \
                (item.y > 1 and next_cell_int(_m, item.y-2, c_size) != g[item.y - 2]):
                continue
            
            if (r_size - 2 == item.y):
                if True:
                    #global cnt
                    cnt += 1
                #pass
            if item.y + 3 < r_size:
                yield Item(_m, item.x, item.y + 2)
            elif item.y + 2 < r_size:
                yield Item(_m, item.x, item.y + 1)
 

    while len(queue) > 0:
        item = queue.pop()

        for item2 in next(item):
            queue.append(item2)
    return cnt

def solution(g):
    global next_dict
    next_dict = {}
    return tr(g)

'''
print_mat(next_mat([
    [False,True,False,False],
    [False,False,True,False],
    [False,False,False,True],
    [True,False,False,False]
]))
'''

print(1, solution([
    [True, True, False, True, False, True, False, True, True, False], 
    [True, True, False, False, False, False, True, True, True, False], 
    [True, True, False, False, False, False, False, False, False, True], 
    [False, True, False, False, False, False, True, True, False, False]]))

print(2, solution([
    [True, False, True], 
    [False, True, False], 
    [True, False, True]]))


print(3, solution([
    [True, False, True, False, False, True, True, True], 
    [True, False, True, False, False, False, True, False], 
    [True, True, True, False, False, False, True, False], 
    [True, False, True, False, False, False, True, False], 
    [True, False, True, False, False, True, True, True]]))




