def solution(l):
    list = [([int(n) for n in v.split('.')],v) for v in l]
    list = [(sum([x * (100 ** (3-i)) for i,x in enumerate(v[0])]) + len(v[0]),v[0],v[1]) for v in list]

    list = sorted(list, key=lambda v: v[0])
    return ','.join([v[2] for v in list])



l = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]
print(solution(l))