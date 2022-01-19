


def to_str_mat(m):
    def f(v):
        if v:
            return '1'
        else:
            return '0'

    return '\n'.join([''.join([f(v) for v in row]) for row in m])

def mat(m, x, y, r_size, c_size):
    return m[x:x+r_size][y:y+c_size]

def new_mat(r_size, c_size):
    ret = [[None for _ in range(c_size)] for _ in range(r_size)]
    return ret

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
    '''
    def has_one(i, j):
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
    '''
    #return [ [has_one(i, j) for j in range(c_size)] for i in range(r_size) ]
    return [ [next_cell(g, i, j) for j in range(c_size)] for i in range(r_size) ]

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

    '''
    for k, v in d.items():
        print('key:')
        print_mat(k)
        for m in v:
            print_mat(m)
    '''
    return d  

def create_cell_dict(d):
    d2 = {}
    d2[True] = []
    d2[False] = []
    for k,v in d.items():
        d2[k[0][0]].extend(v)

    #print(d2)
    return d2


def tr(g):
    r_size = len(g)
    c_size = len(g[0])
    g = to_tuple(resize(g, r_size+1, c_size+1))
    r_size = len(g)
    c_size = len(g[0])

    queue = []

    global cnt
    cnt = 0
    
    #init
    queue.append(Item(new_mat(r_size, c_size), 0, 0))

    d = create_mat_dict(1)
    cell_dict = create_cell_dict(d)

    #print(cell_dict)
    def next(item):
        m = item.m

        ret = []
        for m2 in cell_dict[g[item.x][item.y]]:
            
            _m = copy(m)
            
            if set_mat(_m, m2, item.x, item.y):
                continue
            if next_cell(_m, item.x, item.y) != g[item.x][item.y] or \
                (item.x > 0 and next_cell(_m, item.x-1, item.y) != g[item.x-1][item.y]) or \
                (item.y > 0 and next_cell(_m, item.x, item.y-1) != g[item.x][item.y-1]) or \
                (item.x > 0 and item.y > 0 and next_cell(_m, item.x-1, item.y-1) != g[item.x-1][item.y-1]):
                continue
            if (r_size - 2 == item.x and c_size - 2 == item.y):
                m_next = to_tuple(next_mat(_m))
                if g == m_next:
                    global cnt
                    cnt += 1
                #pass
            if item.y + 2 < c_size:
                yield Item(_m, item.x, item.y + 1)
                #ret.append(Item(_m, item.x, item.y + 1))
            elif item.y == c_size - 2:
                if item.x + 2 < r_size:
                    yield Item(_m, item.x + 1, 0)
                    #ret.append(Item(_m, item.x + 1, 0))
    
    global cache
    cache = {}
    def df(item):
        global cache
        if (item.x, item.y, to_tuple(mat(item.m, item.x, item.y, 2, 2))) in cache:
            #pass
            return cache[(item.x, item.y, to_tuple(mat(item.m, item.x, item.y, 2, 2)))]
        global cnt
        cnt = 0
        for item2 in next(item):
            cnt += df(item2)
        if cnt > 0:
            cache[(item.x, item.y, to_tuple(mat(item.m, item.x, item.y, 2, 2)))] = cnt
        #pass
        return cnt
    #queue.append(Item(new_mat(r_size, c_size), 0, 0))
    item = Item(new_mat(r_size, c_size), 0, 0)
    cnt = df(item)
    return cnt

    '''
    cnt = 0
    g = to_tuple(g)
    while len(queue) > 0:
        item = queue.pop(0)

        for item in next(item):
            queue.append(item)
    return cnt
    '''

def solution(g):
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


