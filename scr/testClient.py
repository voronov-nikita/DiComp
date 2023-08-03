from client import Xsay
from time import time

server = Xsay()


@server.calculate(ip="192.168.8.104", port=12345)
def one(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


@server.calculate(ip="192.168.8.104", port=12345)
def two(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


start = time()
k = int(one(10))
b = int(one(9))
print(k-b)
print(time() - start)