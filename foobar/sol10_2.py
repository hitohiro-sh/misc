from collections import Counter

def to_tuple(m):
    return tuple([tuple(row) for row in m])

def to_mat(vs, w, h):
    return tuple([vs[i*w:(i+1)*w] for i in range(h)])

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

def flatten(m):
    from itertools import chain

    return chain.from_iterable(m)


def create_cycle_dict(w, h):
    from itertools import permutations

    d = {}
    m = to_mat(range(w * h), w, h)

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

    prev_key1 = -1
    r_size = h
    c_size = w
    for r_p in permutations(range(r_size), r_size):
        _m2 = r_map(m, r_p)
        for c_p in permutations(range(c_size), c_size):
            m2 = t(r_map(t(_m2), c_p))

            code = cycle(m, m2)

            if code in d:
                d[code] += 1
            else:
                d[code] = 1
            
    return d

def solution(w, h, s):

    total = 0

    d = create_cycle_dict(w, h)

    def fix_cnt(key):
        #print('key', key)
        c_s = []
        for v in key:
            c_s.append(len(v))
        #print(sum(c_s))
        x = sum(Counter(c_s).values())
        #print('sum', x)
        return x

    G_len = 0
    total = 0
    for k, v in d.items():
        #print(k,v)
        G_len += v
        total += v * (s ** fix_cnt(k))

    
    return str(total // G_len)

print(1, solution(2, 2, 2))
print(2, solution(2, 3, 4))
print(2, solution(3, 2, 4))

print(3, solution(3, 3, 2))
print(4, solution(4, 3, 2))
print(5, solution(8, 1, 2))
print(4, solution(5, 5, 3))
#print(3, solution(12, 5, 2))