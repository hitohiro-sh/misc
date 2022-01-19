
def solve3(cur_weight, max_step, cache):

    
    if (cur_weight, max_step) in cache:
        return cache[(cur_weight, max_step)]

    cnt = 0
    for next_step in range(1, max_step+1):
        if cur_weight - next_step == 0:
            cnt += 1
        elif cur_weight - next_step > 0:
            cnt += solve3(cur_weight - next_step, next_step-1, cache)
        else:
            break

    cache[(cur_weight, max_step)] = cnt
    return cnt


def solution(n):
    cache = {}

    ret2 = solve3(n, n - 1, cache)
    return ret2


print(1, solution(3))
print(2, solution(5))
print(200, solution(200))
