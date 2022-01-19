from datetime import datetime

def f(x):
    if x < 1:
        return 1
    else:
        return f(x - 1) + f(x - 2)


def g(x):
    start = datetime.now()
    print(start)
    print(f(x))
    end = datetime.now()
    print(end)
    print(end - start)

    
