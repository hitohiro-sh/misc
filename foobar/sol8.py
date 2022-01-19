class Item:
    def __init__(self, start, end, delta, cur_limit, bunnys, rescued, trace):
        self.start_pos = start
        self.end_pos = end
        self.limit = cur_limit - delta
        self.delta = delta
        self.bunnys = set(bunnys)
        self.rescued = set(rescued)
        self.trace = set(trace)

    def pick(self, pos):
        #print("pick")
        self.bunnys.add(pos)

    def picked(self, pos):
        return pos in self.bunnys

    def visited(self, start, end):
        return (start, end) in self.trace

    def rescue(self):
        #print("rescue")
        self.rescued = self.rescued.union(self.bunnys)


    def __str__(self):
        return str( (self.start_pos, self.end_pos, self.limit, "b:", self.bunnys, "r:", self.rescued) )

def set_item(prev_item, to, m):

    return Item(prev_item.end_pos, 
        to, 
        m[prev_item.end_pos][to], 
        prev_item.limit, prev_item.bunnys, prev_item.rescued, prev_item.trace)

def init_item(start, end, delta, cur_limit):
    return Item(start, end, delta, cur_limit, set(), set(), set())


def tr(m, limit):
    size = len(m)
    if size < 2:
        return []
    queue = []

    # min_time matrix
    m_min = [[0 for _ in range(size)] for _ in range(size)]
    m_pre = [[-1 for _ in range(size)] for _ in range(size)]
    # return True if minus cycle
    def init_m_min(m_min, m_pre):
        def calc_min(src, m_min, m_pre):
            for pos in range(size):
                if pos != src:
                    m_min[src][pos] = 10000
            for _ in range(size - 1):
                for u in range(size):
                    for v in range(size):
                        if u != v and m_min[src][u] + m[u][v] < m_min[src][v]:
                            m_min[src][v] = m_min[src][u] + m[u][v]
                            m_pre[src][v] = u
            
            for u in range(size):
                for v in range(size):
                    if m_min[src][u] + m[u][v] < m_min[src][v]:
                        return True
            
            return False

            
        for src in range(size):
            if calc_min(src, m_min, m_pre):
                return True
        return False
    
    if init_m_min(m_min, m_pre):
        return [i+1 for i in range(size - 2)]

    


    def init_queue():
        cur_pos = 0
        for to_pos, time in enumerate(m_min[cur_pos]):
            if cur_pos != to_pos:
                queue.append(init_item(cur_pos, to_pos, time, limit))

    # init
    init_queue()


    rescued = set()


    def can_fin(item):
        if len(rescued) == size - 2:
            return True

        if item.limit < 0:
            for pos, time in enumerate(m_min[item.end_pos]):
                if item.end_pos != pos and item.limit - time >= 0:
                    return False
            return True
        return False

    # return True if rescued
    def proc(item):
        flag = False
        if item.end_pos not in [0, size-1]:
            if not item.picked(item.end_pos):
                # pick bunny
                item.pick(item.end_pos)
        elif item.end_pos == size - 1:
            if len(item.bunnys) > 0 and item.limit >= 0:
                # rescue bunny
                item.rescue()
                flag = True
        item.trace.add( (item.start_pos, item.end_pos) )
        return flag

    
    while len(queue) > 0:
        item = queue.pop()
        #print(str(item))

        
        if proc(item):
            # rescued
            if len(rescued) < len(item.rescued):
                rescued = item.rescued
            elif len(rescued) == len(item.rescued):
                if list(rescued) > list(item.rescued):
                    rescued = item.rescued
                #pass

        if can_fin(item):
            continue
        
        for pos, time in enumerate(m[item.end_pos]):
            if item.end_pos != pos and item.start_pos != pos and not item.visited(item.end_pos, pos):
                queue.append(set_item(item, pos, m_min))

    return rescued


def solution(times, times_limit):
    ret = tr(times, times_limit)

    return [x-1 for x in ret]

print("ans:")
print(1,solution([
    [0, 2, 2, 2, -1], 
    [9, 0, 2, 2, -1], 
    [9, 3, 0, 2, -1], 
    [9, 3, 2, 0, -1], 
    [9, 3, 2, 2, 0]], 1), [1, 2])

print("ans:")
print(2,solution([
    [0, 1, 1, 1, 1], 
    [1, 0, 1, 1, 1], 
    [1, 1, 0, 1, 1], 
    [1, 1, 1, 0, 1], 
    [1, 1, 1, 1, 0]], 3), [0, 1])

print("ans:")
print(3,solution([
    [0, -2, 9, 3],
    [1, 0, 9, 9],
    [9, 9, 0, 9],
    [9, 9, 9, 0]
]
, 0), [0, 1])

print("ans:")
print(4,solution([
    [0, -1, 9, 3],
    [1, 0, 9, 9],
    [9, 9, 0, 9],
    [9, 9, 9, 0]
]
, 0), [])

print("ans:")
print(5,solution([
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
, 0), [])

print("ans:")
print(6,solution([
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
, 2),[0])

print("ans:")
print(7,solution([
    [0, 1, 1, 1],
    [1, -1, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
, 2), [0,1])

print("ans:")
print(8,solution([
    [0, 9, 9, 9],
    [9, -1, 9, 9],
    [9, 9, 0, 9],
    [9, 9, 9, 0]
]
, 2), [0,1])

print("ans:")
print(9,solution([
    [0, 1],
    [1, 0]
]
, 2), [])

print("ans:")
print(10, solution([
    [-1, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
, 2), [0, 1])

print("ans:")
print(11, solution([
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
, 2), [0, 1])

print("ans:")
print(12, solution([
    [0, 0, 0, 0],
    [9, 0, 9, 1],
    [9, 9, 0, 1],
    [9, 0, 9, 0]
]
, 2), [0, 1])

print("ans:")
print(13, solution([
    [0, 9, 9],
    [9, -1, 9],
    [9, 9, 0]
]
, 2), [0])

print("ans:")
print(14, solution([
    [0, 9, 9],
    [9, 0, 9],
    [9, 9, -1]
]
, 2), [0])

print("ans:")
print(15, solution([
    [0, 9, 1, 9, 9],
    [9, 0, 9, 9, 1],
    [9, 1, 0, 9, 9],
    [9, 9, 9, 0, 9],
    [9, 9, 9, 0, 9]
]
, 3), [0, 1])

print("ans:")
print(16,solution([
    [0, 9, 9, 9, 9, 1], 
    [9, 0, 9, 1, 1, 9], 
    [9, 9, 0, 9, 9, 9], 
    [9, 9, 9, 0, 9, 2], 
    [9, 9, 9, 9, 0, 2],
    [9, -2, 9, 9, 9, 0]
    ], 5), [0, 2, 3])

print("ans:")
print(17,solution([
    [0, 1, 9, 9, 9, 9], 
    [9, 0, 1, 9, 9, 9], 
    [9, 9, 0, 1, 1, 9], 
    [9, 9, 9, 0, 9, 1], 
    [9, 9, 9, 9, 0, 1],
    [9, 1, 9, 9, 9, 0]
    ], 8), [0, 1, 2, 3])

print("ans:")
print(18,solution([
]
, 2), [])

print("ans:")
print(19, solution([
    [0, 9, 9],
    [9, 0, 9],
    [9, 9, 0]
]
, 2), [])

print("ans:")
print(20, solution([
    [0, 0, 9],
    [9, 0, 0],
    [9, 9, 0]
]
, 2), [0])

print("ans:")
print(21, solution([
    [0, 1, 2, 3, 4, 5, 6],
    [0, 0, 2, 3, 4, 5, 6],
    [0, 1, 0, 3, 4, 5, 6],
    [0, 1, 2, 0, 4, 5, 6],
    [0, 1, 2, 3, 0, 5, 6],
    [0, 1, 2, 3, 4, 0, 6],
    [0, 1, 2, 3, 4, 5, 0]
]
, 15), [0])
