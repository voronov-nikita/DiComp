from dicomp import Dicomp
from time import time

server = Dicomp()


@server.calculate(ip="192.168.8.105", port=12345, isReturn=True)
def one(a):
    for i in range(100):
        print(a)


def two(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


start = time()
print(one(100))
print(time() - start)