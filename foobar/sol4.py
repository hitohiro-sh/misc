
from fractions import Fraction

# trace
# 0: from_state
# 1: to_state
# 2: matrix
# 3: state_set

def init_trace(from_state, to_state, size):
    t = Trace(size)
    t.init(from_state, to_state)
    return t

class Trace:
    def __init__(self, size):
        self.size = size
        pass

    def init(self, from_state, to_state):
        size = self.size

        self.from_state = from_state 
        self.to_state = to_state
        self.init_state = from_state

        self.mat = [[0 for _ in range(size)] for _ in range(size)]
        self.mat[from_state][to_state] = True
        self.mat_trace = []
        self.mat_trace.append((self.to_state,self.mat))

        self.state_set = set()
        self.state_set.add(from_state)
        self.state_set.add(to_state)

    def copy_add(self, from_state, to_state):
        t = Trace(self.size)

        t.from_state = from_state
        t.to_state = to_state
        t.init_state = self.init_state

        t.mat = [row[:] for row in self.mat]
        t.mat[from_state][to_state] = True

        t.mat_trace = self.mat_trace[:]
        t.mat_trace.append( (t.to_state, t.mat) )

        t.state_set = set(self.state_set)
        t.state_set.add(from_state)
        t.state_set.add(to_state)

        return t
    
    def has(self, from_state, to_state):
        return self.mat[from_state][to_state]

def is_cycle(trace, to_state):

    if to_state in trace.state_set:
        return True
    else:
        return False

def is_mat_same(m1,m2):
    for (row1,row2) in zip(m1,m2):
        for (c1,c2) in zip(row1,row2):
            if c1 != c2:
                return False
    return True

def is_same(trace, from_state, to_state):
    t2 = trace.copy_add(from_state, to_state)
    #print('---')
    #print(t2.to_state)
    #print_mat(t2.mat)
    #print(trace.to_state)
    #print_mat(trace.mat)
    #print('---')
    for to_state,mat in trace.mat_trace:
        if t2.to_state == to_state:
            if is_mat_same(t2.mat, mat):
                return True
            else:
                continue
                #return False
            
    return False

def queue_item(cur_state, 
               next_state, 
               trace):
    prob = None
    return (cur_state, next_state, trace)

# sum (n/m)^k = n/(m-n)
def cycle_prob(frac):
    n = frac.numerator
    m = frac.denominator
    return Fraction(n,m-n)

def tr(mat):
    size = len(mat)
    #P(next|cur)
    mat_prob = [[0 for _ in range(size)] for _ in range(size)]

    normal_prob = [0 for _ in range(size)]
    #init step
    #P0(n|n)
    #for cur_state in range(size):
    #    mat_prob[cur_state][cur_state] = 1

    # init queue
    queue = []
    #P1(n|m)
    for cur_state in range(size):
        for next_state in range(size):
            prob = mat[cur_state][next_state]
            if prob != 0:
                #if is_cycle(trace, next_state):
                if cur_state == next_state:
                    prob = cycle_prob(prob)
                mat_prob[cur_state][next_state] += prob 
                trace = init_trace(cur_state, next_state, size)
                queue.append(
                        queue_item(cur_state, 
                                next_state, 
                                trace))
    
    def proc(cur_state,next_state):
        prob = mat_prob[cur_state][next_state]
        if is_cycle(trace, next_state):
            # P(cur|next) * P(next|cur)
            _prob = prob * mat_prob[next_state][cur_state]
            mat_prob[next_state][next_state] += cycle_prob(_prob)
            #_prob = prob * mat_prob[trace.init_state][cur_state]
            #mat_prob[trace.init_state][next_state] += _prob
        else:
            #Pn(next|cur) = Pn-1(next|cur) * P(cur)
            _prob = prob * mat_prob[trace.init_state][cur_state]
            mat_prob[trace.init_state][next_state] += _prob
        #print('p',prev_state,'c',cur_state,'n',next_state)
        #print_mat(mat_prob)

    while len(queue) > 0:
        (prev_state, 
        cur_state, 
        trace) = queue.pop(0)

        # proc(prev_state,cur_state)
        #print(prev_state,cur_state)

        for next_state, prob0 in enumerate(mat[cur_state]):
            #print(prob0)
            if prob0 != 0:
                # P(next|cur)
                # if True:

                #if not trace.has(cur_state, next_state):
                

                

                if not is_same(trace, cur_state, next_state):
                    
                    proc(cur_state, next_state)
                    
                    queue.append(
                        queue_item(cur_state, next_state,
                            trace.copy_add(cur_state,next_state)))
    
    return normal_prob,mat_prob

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

def prob(m):
    totals = [sum(row) for row in m]
    def f(v,t):
        if v > 0:
            return Fraction(v,t)
        else:
            return 0

    return [[f(c,total) for c in row] 
                for (row,total) in zip(m,totals)]

def solution(m):
    size = len(m)
    (n,m2) = tr(prob(m))

    return (n,m2,prob(m))


def print_mat(m):
    print('[')
    for row in m:
        print(row)
    print(']')


ret = solution( [[0, 1, 0, 0, 0, 1], 
    [4, 0, 0, 3, 2, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]])
print('---')
print_mat(ret[2])
#print_mat(ret[0])
print_mat(ret[1])

'''
ret = solution( [
    [0, 1, 0, 0, 0, 1], 
    [0, 0, 1, 0, 0, 1], 
    [0, 1, 0, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]])
print('---')
print_mat(ret[2])
#print_mat(ret[0])
print_mat(ret[1])
'''


ret = solution( [[0, 1, 0, 0, 0, 1], 
    [0, 0, 0, 3, 2, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]])
print('---')
print_mat(ret[2])
#print_mat(ret[0])
print_mat(ret[1])
