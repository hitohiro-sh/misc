
def to_tuple(m):
    return tuple([tuple(row) for row in m])

def to_mat(vs, w, h):
    return [vs[i*w:(i+1)*w] for i in range(h)]

# transpose
def t(m):
    r_size = len(m)
    c_size = len(m[0])

    m_t = [[0 for _ in range(r_size)] for _ in range(c_size)]
    for i in range(r_size):
        for j in range(c_size):
            m_t[j][i] = m[i][j]
    
    return to_tuple(m_t)

def r_map(m, idxs):
    return [m[i][:] for i in idxs]

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

# [1,2,3]
# [4,5,6]
# [7,8,9]
# =>
# [5,6,1]
# [8,9,4]
# [2,3,7]
def shift(m):
    r_size = len(m)
    c_size = len(m[0])    

    idxs = list(range(r_size))
    v = idxs.pop(0)
    idxs.append(v)

    m = r_map(m, idxs)

    idxs = list(range(c_size))
    v = idxs.pop(0)
    idxs.append(v)

    m = t(r_map(t(m), idxs))
    #print(m)
    return m

def flatten(m):
    from itertools import chain

    return chain.from_iterable(m)

def cycle(m, m2):

    list = []

    vs1 = tuple(flatten(m))
    vs2 = tuple(flatten(m2))

    fin_idx = set()
    for from_idx in vs1:
        if from_idx not in fin_idx:
            c = [from_idx]

            to_idx   = vs2[from_idx]

            while to_idx not in c:
                c.append(to_idx)
                fin_idx.add(to_idx)
                to_idx = vs2[to_idx]
            list.append(c)

    return to_tuple(list)


def cycle_pair_dict(w, h):
    d = {}
    r_size = h
    c_size = w
    for r in range(1, r_size+1):
        for c in range(1, c_size+1):
            m = to_mat(range(r * c), c, r)
            m2 = shift(m)
            cy = cycle(m, m2)
            #print(cy)
            d[(r,c)] = len(cy)
            
    return d

def solution(w, h, s):
    from itertools import permutations
    from math import factorial
    from collections import Counter
    

    d = cycle_pair_dict(w, h)

    total = 0

    r_size = h
    c_size = w

    #dic1 = {}

    cache = {} 
    cache2 = {}

    # row subtotal
    subtotal = [0, 0]

    cur_s_key = 0

    # col subtotal
    subtotal3 = {}

    G_len = factorial(w) * factorial(h)
    for r_p in permutations(range(r_size), r_size):
        s_key = r_p[0]
        
        if cur_s_key != s_key:
            if cur_s_key != 0:
                break

            cur_s_key = s_key
        
        cycle_r = cycle([range(r_size)], [r_p])
        cycle_r_n = tuple(sorted([len(v) for v in cycle_r]))
        
        key = (cycle_r_n,)
        if key in cache:
            _total = cache[key]
        else:
            _total = 0
            subtotal2 = [0, 0]
            cur_s_key2 = 0

            for c_p in permutations(range(c_size), c_size):
                if c_p in cache2:
                    cycle_c_n = cache2[c_p]
                else:
                    cycle_c = cycle([range(c_size)], [c_p])    
                    cycle_c_n = tuple(sorted([len(v) for v in cycle_c]))
                    cache2[c_p] = cycle_c_n
                s_key3 = (r_p[:3], c_p[:3])


                s_key2 = c_p[0]

                if cur_s_key2 != s_key2:
                    if cur_s_key2 != 0:
                        break

                    cur_s_key2 = s_key2

                fix_cnt = 0
                for r in cycle_r_n:
                    for c in cycle_c_n:
                        fix_cnt += d[(r,c)]
                if s_key3 not in subtotal3:
                    subtotal3[s_key3] = 0

                _val = s ** fix_cnt
                subtotal2[s_key2] += _val
                subtotal3[s_key3] += _val
                #_total += s ** fix

            _total = subtotal2[0] + (c_size - 1) * subtotal2[1]
            cache[key] = _total
        subtotal[s_key] += _total
        total += _total

    total = subtotal[0] + (r_size - 1) * subtotal[1]

    #for v in sorted(subtotal3.items()):
    #    print(v)

    return str(total // G_len)

print(1, solution(2, 2, 2))
print(1, solution(2, 3, 20))
print(2, solution(2, 3, 4))
print(2, solution(3, 2, 4))

print(3, solution(3, 3, 2))
print(4, solution(4, 3, 2))
print(5, solution(8, 1, 2))
print(5, solution(1, 8, 2))
print(4, solution(5, 5, 3))
print(3, solution(5, 10, 2))
#print(3, solution(10, 5, 2))
#print(3, solution(5, 11, 2))
#print(3, solution(12, 5, 2))