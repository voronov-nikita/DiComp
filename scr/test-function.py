from client import save_send_file


@save_send_file
def one(n, b):
    return n + b


# @save_send_file
def two():
    return 2


def five():
    return 5

print(one(b=10, n=50))
print(two())
