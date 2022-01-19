
def solve2(n, cur_weight, start_step, cache):

    
    if (cur_weight, start_step) in cache:
        return cache[(cur_weight, start_step)]

    cnt = 0
    for next_step in range(start_step,n):
        if cur_weight + next_step == n:
            cnt += 1
        elif cur_weight + next_step < n:
            cnt += solve2(n, cur_weight + next_step, next_step+1, cache)
        else:
            break

    cache[(cur_weight, start_step)] = cnt
    return cnt


def solution(n):
    cache = {}

    ret2 = solve2(n, 0, 1, cache)
    return ret2

print(1, solution(3))
print(2, solution(5))
print(200, solution(200))
