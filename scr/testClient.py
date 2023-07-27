from client import Xsay


server = Xsay()


@server.send_file(ip="192.168.8.100", port=12345)
def one(a):
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(a):
                k += i*g*x
    return k


@server.send_file(ip="192.168.8.100", port=12345)
def two():
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(5):
                k += i*g*x
    return k


print(one(5))
print(two(5))