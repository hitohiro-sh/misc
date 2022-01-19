
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


def cycle_ra(r, m2):
    list = []

    vs1 = r
    vs2 = m2
    #vs2 = tuple(flatten(m2))

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

    return list

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

from itertools import permutations
from math import factorial

class Perm:

    def __init__(self,size):
        self.size = size
        self.iter = permutations(range(size), size)
        self.cache = {}
        self.idx = 0
        self.iter_idx = 0


    def __iter__(self):
        size = self.size
        self.iter = permutations(range(size), size)
        self.idx = 0
        self.iter_idx = 0
        return self

    def next(self):
        if self.idx in self.cache:
            n = self.cache[self.idx]
            self.idx += 1
            return n 

        if self.iter_idx != self.idx:
            for _ in xrange(self.idx - self.iter_idx):
                next(self.iter)
            self.iter_idx = self.idx
        
        n = next(self.iter)
        self.cache[self.idx] = n
        self.iter_idx += 1 
        self.idx += 1
        return n

    def __next__(self):
        return self.next()

    def flash(self, n):
        self.idx += n



        

def solution(w, h, s):
    
    from math import factorial
    from collections import Counter
    

    d = cycle_pair_dict(w, h)

    total = 0

    r_size = h
    c_size = w

    #dic1 = {}

    cache = {} 
    cache2 = {}
    cache3 = {}

    def flash(iter, n):
        for _ in range(n):
            next(iter)

    c_perm = Perm(c_size)
    
    def calc(r_key_idx, row_iter, size):
        if size == 1:
            def calc_col(c_key_idx, col_iter, size, cycle_r_n):
                
                if size == 1:
                    _total = 0                    
                    c_p = next(col_iter,None)
                    if c_p in cache2:
                    #if False:
                        cycle_c_n = cache2[c_p]
                    else:
                        cycle_c = cycle_ra(range(c_size), c_p)    
                        cycle_c_n = tuple(sorted([len(v) for v in cycle_c]))
                        #cycle_c_n = tuple(len(v) for v in cycle_c)
                        cache2[c_p] = cycle_c_n
                    fix_cnt = 0
                    key = (cycle_r_n, cycle_c_n)
                    if key in cache3:
                        fix_cnt += cache3[key]
                    else:
                        for r in cycle_r_n:
                            _cnt = 0
                            for c in cycle_c_n:
                                _cnt += d[(r,c)]
                            fix_cnt += _cnt
                        cache3[key] = fix_cnt
                    _val = s ** fix_cnt
                    #print(_val)
                    _total += _val
                        
                    return _total
                else:
                    subtotal = [0,0]

                    f_size = factorial(size - 1)
                    for i in range(size):
                        if i < 2:
                            subtotal[i] = calc_col(c_key_idx + 1, col_iter, size - 1, cycle_r_n)
                        else:
                            if size == c_size:
                                break
                            #flash(col_iter, size - 1)
                            #flash(col_iter, f_size)
                            col_iter.flash(f_size)

                    total = subtotal[0] + (size - 1) * subtotal[1]
                    return total

            r_p = next(row_iter)
            cycle_r = cycle_ra(range(r_size), r_p)
            cycle_r_n = tuple(sorted([len(v) for v in cycle_r]))

            key = cycle_r_n
            if key in cache:
                return cache[key]
            #col_iter = permutations(range(c_size), c_size)
            col_iter = iter(c_perm)
            total = calc_col(0, col_iter, c_size, cycle_r_n)
            cache[key] = total
            return total
        else:
            subtotal = [0,0]
            
            f_size = factorial(size - 1)
            for i in range(size):
                if i < 2:
                    subtotal[i] = calc(r_key_idx + 1, row_iter, size - 1)
                else:
                    if size == r_size:
                        break
                    
                    row_iter.flash(f_size)
                    #flash(row_iter, f_size)
 
            total = subtotal[0] + (size - 1) * subtotal[1]
            return total

    #row_iter = permutations(range(r_size), r_size)
    row_iter = Perm(r_size)
    total = calc(0, row_iter, r_size)
    #print('total', total)
    G_len = factorial(w) * factorial(h)

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

print(3, solution(10, 5, 2))
print(3, solution(5, 11, 2))

#print(4, solution(5, 11, 20))
#print(3, solution(12, 5, 2))
#print(4, solution(5, 11, 20))
print(3, solution(12, 12, 2))