from multiprocessing import Process
from time import time


def f():
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(5):
                k +=  i*g*x
    print(k)
    

def f2():
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(5):
                k +=  i*g*x
    print(k)


if __name__ == '__main__':
    start = time()
    ls = [f, f2]
    print(ls)
    for i in ls:
        p = Process(target=i)
        p.start()
        p.join()
    print(time() - start)