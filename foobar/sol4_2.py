
from fractions import Fraction
from fractions import gcd

class Matrix:
    def __init__(self, size=2):
        self.size = size
        self.mat = [[0 for _ in range(size)] for _ in range(size)]

    # set 2x2 array
    def set_mat(self, rows):
        self.size = len(rows)
        self.mat = [row[:] for row in rows]

    def set_int(self, v):
        for i in range(self.size):
            self.mat[i][i] = v

    def add(self, mat):
        size = self.size
        m2 = Matrix(self.size)
        for r in range(size):
            for c in range(size):
                m2.mat[r][c] = self.mat[r][c] + mat.mat[r][c]

        return m2

    def sub(self, mat):
        size = self.size
        m2 = Matrix(size)
        for r in range(size):
            for c in range(size):
                m2.mat[r][c] = self.mat[r][c] - mat.mat[r][c]

        return m2

    def mul(self, m2):
        ret = Matrix(self.size)
        for r in range(self.size):
            for c in range(self.size):
                for n in range(self.size):
                    ret.mat[r][c] += self.mat[r][n] * m2.mat[n][c]
        return ret

    def inv2(self):
        def mul_ij(m1, m2, i, j):
            r = 0
            size = m1.size
            for x in range(size):
                r += m1.mat[i][x] * m2.mat[x][j]
            return r

        def lu(m):
            size = m.size
            l = Matrix(size)
            u = Matrix(size)

            for i in range(size):
                l.mat[i][i] = 1
            for i in range(size):
                for j in range(size):
                    if i <= j:
                        # U
                        r = m.mat[i][j] - mul_ij(l, u, i, j)
                        u.mat[i][j] = r
                    else:
                        # L
                        r = (m.mat[i][j] - mul_ij(l, u, i, j)) / u.mat[j][j]
                        l.mat[i][j] = r
            return l, u

        def inv_l(l):
            size = l.size
            m = Matrix(size)
            u = Matrix(size)

            det = 1
            for i in range(size):
                det *= l.mat[i][i]

            for i in range(size):
                m.mat[i][i] = det
            
            for i in range(size):
                for j in range(size):
                    if i >= j:
                        r = (m.mat[i][j] - mul_ij(l, u, i, j)) / l.mat[i][i]
                        u.mat[i][j] = r

            for i in range(size):
                for j in range(size):
                    u.mat[i][j] = u.mat[i][j] / det
            return u

        l, u = lu(self)
        i_l = inv_l(l)
        i_u = inv_l(u.m_t()).m_t()
        return i_u.mul(i_l)
	    #mulm(i_u, i_l)

    def m_t(self):
        size = self.size
        t = Matrix(size)
        for i in range(size):
            for j in range(size):
                t.mat[j][i] = self.mat[i][j]
        return t

    def inv(self):
        det_v = self.det()
        m_inv = Matrix(self.size)
        for i in range(self.size):
            for j in range(self.size):
                m_inv.mat[i][j] = self.adj_ij(j, i) / det_v

        return m_inv

def prob(m):
    totals = [sum(row) for row in m]
    def f(v,t):
        if v > 0:
            return Fraction(v,t)
        else:
            return Fraction(0,1)

    m_prob = [[f(c,total) for c in row] 
                for (row,total) in zip(m,totals)]

    return m_prob

def solution(_mat):
    size = len(_mat)
    m_prob = prob(_mat)

    one = Matrix(size)
    one.set_int(1)

    m = Matrix(size)
    m.set_mat(m_prob)

    def find_fin_state(m):
        def is_fin(row):
            for c in row:
                if c != 0:
                    return False
            return True
        fin_state = []
        for i, row in enumerate(m):
            if is_fin(row):
                fin_state.append(i)
        return fin_state

    # m * inv(1 - m)
    try:
        ret = m.mul(one.sub(m).inv2())
    except:
        return [0,1]

    result = []

    def calc_gcd(vs):
        if len(vs) == 1:
            return vs[0]
        else:
            r = gcd(vs[0], vs[1])
            for v in vs[2:]:
                r = gcd(r, v)
        return r


    def calc_lcm(vs):
        def lcm(v1, v2):
            return v1 * v2 / gcd(v1, v2)
        if len(vs) < 1:
            return 1
        lcm_v = vs[0]
        for v in vs[1:]:
            lcm_v = lcm(lcm_v,v)

        return lcm_v

    result_n = []
    result_m = []
    _r_m = []
    for state in find_fin_state(_mat):
        result_n.append(ret.mat[0][state].numerator)
        result_m.append(ret.mat[0][state].denominator)
        if ret.mat[0][state].numerator > 0:
            _r_m.append(ret.mat[0][state].denominator)

    lcm = calc_lcm(_r_m)
    result = []
    for n,m in zip(result_n,result_m):
        result.append(n * (lcm // m))
    result.append(lcm)

    def all_zero(ret):
        for v in result[:-1]:
            if v > 0:
                return False
        return True
    if all_zero(result):
        result[0] = 1
    return result

ret = solution( [[0, 1, 0, 0, 0, 1], 
    [4, 0, 0, 3, 2, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]])
print(ret)

ret = solution( [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]] )
print(ret)

ret = solution( [
    [0, 2, 1], 
    [0, 1, 1], 
    [0, 0, 0]
    ] )
print(ret)

ret = solution( [
    [1, 1], 
    [0, 0], 
    ] )
print(ret)


ret = solution( [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], 
    [4, 0, 0, 3, 2, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
print(ret)

ret = solution([
    [0,0,0],
    [0,0,0],
    [0,0,0],
])

print(ret)

