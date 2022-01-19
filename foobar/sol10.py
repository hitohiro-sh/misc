
def to_tuple(m):
    return tuple([tuple(row) for row in m])

def to_mat(vs, w, h):
    return tuple([vs[i*w:(i+1)*w] for i in range(h)])

def sort_r(m):
    return sorted(m)


# find v after index r * i + j
# r * _i + _j > r * i + j
def find(m, v, i, j):

    r_size = len(m)
    c_size = len(m[0])
    for _i in range(i, i + 1):
        for _j in range(j, c_size):
            if m[_i][_j] == v:
                return _i, _j
    for _i in range(i + 1, r_size):
        for _j in range(c_size):
            if m[_i][_j] == v:
                return _i, _j
    return -1,-1

def find_vs(m, v):
    r_size = len(m)
    c_size = len(m[0])
    ret = []
    for _i in range(r_size):
        for _j in range(c_size):
            if m[_i][_j] == v:
                ret.append( (_i,_j) )
    #print(ret)
    return ret

def swap_row(m, i, i2):
    tmp = m[i]
    m[i] = m[i2]
    m[i2] = tmp

def swap_col(m, j, j2):
    r_size = len(m)
    for i in range(r_size):
        tmp = m[i][j]
        m[i][j] = m[i][j2]
        m[i][j2] = tmp


def swap(m, i, j, i2, j2):
    swap_row(m, i, i2)
    swap_col(m, j, j2)
    pass

# move v of m to i , j using row swap and col swap
def move(m, v, i, j):
    #r_size = len(m1)
    #c_size = len(m1[0])
    i2, j2 = find(m, v, i, j)
    if i2 < 0 or (i2, j2) == (i, j):
        return
    swap(m, i, j, i2, j2)

def to_list(m):
    return [list(row) for row in m]


def tr(m1, i, j, m2):
    r_size = len(m1)
    c_size = len(m1[0])
    if to_tuple(m1) == to_tuple(m2):
        return True
    else:
        if i == -1:
            return False
        if j < c_size - 1:
            next_i = i
            next_j = j + 1
        elif i < r_size - 1:
            next_i = i + 1
            next_j = 0
        else:
            next_i = -1
            next_j = -1
        for _i,_j in find_vs(m2, m1[i][j]):
            if (i, j) != (_i,_j):
                _m2 = to_list(m2)
                swap(_m2, i, j, _i,_j)
                if m1[0][0] != _m2[0][0]:
                    print(_m2)
                if tr(m1, next_i, next_j, _m2):
                    return True
        return False

def r_map(m, idxs):
    return [m[i][:] for i in idxs]

def equivalent(m1,m2):
    from itertools import permutations
    r_size = len(m1)
    c_size = len(m1[0])

    for r_p in permutations(range(r_size), r_size):
        _m2 = r_map(m2, r_p)
        for c_p in permutations(range(c_size), c_size):
            __m2 = t(r_map(t(_m2), c_p))
            if to_tuple(m1) == to_tuple(__m2):
                return True
    return False

# doesn't work
def equivalent2(m1,m2):
    _m2 = to_list(m2)
    r_size = len(m1)
    c_size = len(m1[0])
    return tr(m1, 0, 0, _m2)


def equivalent1(m1,m2):
    _m2 = to_list(m2)
    r_size = len(m1)
    c_size = len(m1[0])
    for i in range(r_size):
        for j in range(c_size):
            move(_m2, m1[i][j], i, j)
    if to_tuple(m1) == to_tuple(_m2):
        return True
    else:
        return False


# transpose
def t(m):
    r_size = len(m)
    c_size = len(m[0])

    m_t = [[0 for _ in range(r_size)] for _ in range(c_size)]
    for i in range(r_size):
        for j in range(c_size):
            m_t[j][i] = m[i][j]
    
    return to_tuple(m_t)
    

def solution(w, h, s):
    from itertools import product
    from itertools import combinations
    from itertools import combinations_with_replacement
    from itertools import permutations

    # key:   sort(seq)
    # value: mat
    d = {}
    #seqs = set()
    cnt = 0
    for vs in product(range(s), repeat=w * h):
    #for vs in combinations_with_replacement(range(s), w * h):
        #print(vs)
        #continue
        m2 = to_mat(vs, w, h)
        key = tuple(sorted(vs))
        if key in d:
            #m2 = t(sort_r(t(sort_r(m2))))
            flag = False
            for m in d[key]:
                if equivalent(m, m2):
                    
                    flag = True
                    break
                else:
                    pass
                    #print('m', m)
                    #print('m2', m2)
            if flag:
                continue
            
            d[key].append(m2)
        else:
            d[key] = []
            d[key].append(m2)
        cnt += 1


    return cnt

print(2, solution(2, 2, 2))
print(1, solution(2, 3, 4))
print(1, solution(3, 2, 4))
#print(1, solution(2, 3, 6))

print(3, solution(3, 3, 2))

print(4, solution(4, 3, 2))

print(5, solution(8, 1, 2))
#print(3, solution(3, 3, 2))
#print(2, solution(2, 2, 4))

#print(2, solution(12, 2, 12 * 2))

#print(3, solution(3, 4, 2))

