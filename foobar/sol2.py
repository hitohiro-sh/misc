

def coord(v):
    y = v // 8
    x = v - 8 * y
    return x,y

def idx(c):
    return c[0] + 8 * c[1]

def next(v,dst):
    c = coord(v)
    c_d = coord(dst)

    
    if c[0] > c_d[0] and abs(c[0] - c_d[0]) > 1:
        c_move = [-1,-2]
    elif c[0] < c_d[0] and abs(c[0] - c_d[0]) > 1:
        c_move = [1,2]
    else:
        c_move = [-1,-2,1,2]

    moves = []
    if c[1] > c_d[1] and abs(c[1] - c_d[1]) > 1:
        for x in c_move:
            if abs(x) == 1:
                moves.append((x,-2))
            else:
                moves.append((x,-1))
    elif c[1] < c_d[1] and abs(c[1] - c_d[1]) > 1:
        for x in c_move:
            if abs(x) == 1:
                moves.append((x,2))
            else:
                moves.append((x,1))      
    else:
        for x in c_move:
            if abs(x) == 1:
                moves.append((x,2))
                moves.append((x,-2))
            else:
                moves.append((x,1))
                moves.append((x,-1))

    ns = []
    for (x,y) in moves:
        n = (c[0] + x,c[1] + y)
        if (0 <= n[0] and n[0] < 8) and (0 <= n[1] and n[1] < 8):
            #valid
            ns.append(idx(n))
    return ns

def tr_deplicated(src, dest, trace):
    if len(trace) >= 8:
        return 64

    min = 64
    
    for v in next(src,dest):
        if v == dest:
            #print(trace + [v])
            return len(trace)
        else:
            if v in trace:
                continue
            trace.append(v)
            n_step = tr_deplicated(v, dest, trace)
            trace.pop()
            if n_step < min:
                min = n_step
    return min

def tr(src, dest):
    if src == dest:
        return 0
    step = 1
    visited = []
    queue = next(src, dest)
    while queue:
        n_queue = []
        for v in queue:
            if v == dest:
                return step
            else:
                if v in visited:
                    continue
                visited.append(v)
                n_queue.extend(next(v, dest))
        step += 1
        queue = n_queue

    return -1

def solution(src, dst):
    return tr(src, dst)
    #return tr_deplicated(src, dst, [src])

print(solution(0, 1))
print(solution(19,36))
print(solution(47,63))
print(solution(0, 63))


print(solution(49, 56))
print(solution(54, 63))
print(solution(0, 0))
print(solution(3, 0))
