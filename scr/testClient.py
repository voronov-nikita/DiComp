from dicomp import Dicomp
from time import time

server = Dicomp()


@server.calculate(ip="192.168.8.105", port=12345)
def one(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


def two(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


start = time()

print(time() - start)