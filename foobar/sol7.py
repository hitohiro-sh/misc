
class Item:
    def __init__(self,cur_state, next_state, m, trace):
        self.cur_state = cur_state
        self.next_state = next_state
        if trace == None:
            self.trace = set()
        else:
            self.trace = set(trace)
        self.trace.add(cur_state)
        self.trace.add(next_state)

    def has(self, state):
        return state in self.trace

def new_item(cur_state, next_state, m, trace=None):
    return Item(cur_state, next_state, m, trace)

def tr(starts, fins, m):
    size = len(m)
    queue = []

    def init_capacity(m_cap):
        for cur_state in range(size):
            in_cap = 0
            for state in range(size):
                if state != cur_state:
                    in_cap += m[state][cur_state]
            out_cap = 0
            for state in range(size):
                if state != cur_state:
                    out_cap += m[cur_state][state]
            if in_cap < out_cap:
                if in_cap > 0:
                    m_cap[cur_state] = in_cap
                else:
                    m_cap[cur_state] = out_cap
            else:
                if out_cap > 0:
                    m_cap[cur_state] = out_cap
                else:
                    m_cap[cur_state] = in_cap

    m_cap = [0] * size
    init_capacity(m_cap)

    # init
    for cur_state in starts:
        for next_state, n in enumerate(m[cur_state]):
            if n > 0:
                queue.append(new_item(cur_state, next_state, m))

    def proc_inout(item):
        cur_state = item.next_state
        in_cap = 0
        for state in range(size):
            if cur_state != state:
                if m[state][cur_state] > 0:
                    in_cap += m_cap[state]
        if in_cap < m_cap[state]:
            m_cap[state] = in_cap
        out_cap = 0
        for state in range(size):
            if cur_state != state:
                if m[cur_state][state] > 0:
                    out_cap += m_cap[state]
        if out_cap > 0 and out_cap < m_cap[state]:
            m_cap[state] = out_cap

    while len(queue) > 0:
        item = queue.pop(0)

        proc_inout(item)

        cur_state = item.next_state
        for next_state, n in enumerate(m[cur_state]):
            if n > 0:
                if not item.has(next_state):
                    queue.append(new_item(cur_state, next_state, m, item.trace))            

    return m_cap

def solution(entrances, exits, path):
    def f(ret):
        #print(ret)

        total = 0
        for state in exits:
            total += ret[state]

        in_set = set()
        for state in exits:
            for from_state in range(len(path)):
                if path[from_state][state] > 0:
                    in_set.add(from_state)
        in_total = 0
        for state in in_set:
            in_total += ret[state] 
        if in_total < total:
            total = in_total
        return total

    ret = tr(entrances, exits, path)

    return f(ret)

def print_mat(m):
    print('[')

    for row in m:
        print(row)
    print(']')

ret = solution([0, 1],
    [4,5],
    [[0, 0, 4, 6, 0, 0], 
     [0, 0, 5, 2, 0, 0], 
     [0, 0, 0, 0, 4, 4], 
     [0, 0, 0, 0, 6, 6], 
     [0, 0, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0]])

print(ret)

ret = solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
print(ret)
