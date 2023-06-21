from client import save_send_file


@save_send_file
def one():
    print(2)
    return 2


# @save_send_file
def two():
    return 2


def five():
    return 5

print(one())
print(two(),
five())