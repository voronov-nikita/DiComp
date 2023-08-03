from client import Xsay
from time import time

server = Xsay()


@server.send_file(ip="192.168.8.104", port=12345)
def one(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


@server.send_file(ip="192.168.8.104", port=12345)
def two(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k

start = time()
print(one(5))
print(two(5))
print(time() - start)