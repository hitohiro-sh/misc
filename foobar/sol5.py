
def solve(n,cache):
    if n <= 2:
        return [n]
    else:
        # 3<=n
        if n in cache:
            return cache[n]
        else:
            ret = [n]
            #for step in range(n-1, 0, -1):
            for step in range(1, n):
                n2 = n - step
                ret2 = solve(n2,cache)
                for v in ret2:
                    if step > v:
                        ret.append(step)
            cache[n] = ret
            return ret

def solve2(n, cur, start, iter, max_iter, cache):
    if iter >= max_iter:
        return 0
    
    if (cur, start) in cache:
        return cache[(cur, start)]

    cnt = 0
    for next_step in range(start,n):
        if cur + next_step == n:
            cnt += 1
        elif cur + next_step < n:
            cnt += solve2(n, cur + next_step, next_step+1, iter+1, max_iter, cache)
        else:
            break

    cache[(cur, start)] = cnt
    return cnt


def solution(n):
    cache = {}

    ret2 = solve2(n, 0, 1, 0, int( (2 * n) ** 0.5 ), cache)
    return ret2


print(200, solution(200))
