from client import save_send_file


@save_send_file
def one():
    print(1)
    return 1


# @save_send_file
def two():
    return 2


def five():
    return 5

print(one())
print(two(),
five())