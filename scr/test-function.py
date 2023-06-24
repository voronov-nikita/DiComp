from client import save_send_file


@save_send_file
def one(n):
    return n


# @save_send_file
def two():
    return 2


def five():
    return 5

print(one(1))
print(two())
