from client import save_send_file, init


init(ip="192.168.8.101", port=12345)

@save_send_file
def one(n, b):
    return n + b


# @save_send_file
def two():
    return 2


def five():
    return 5

print(one(b=10, n=50))
# print(two())
