from client import save_send_file


@save_send_file
def one():
    return 1


@save_send_file
def two():
    return 2


def five():
    return 5

one()
two()
five()