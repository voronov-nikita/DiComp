from client import save_send_file

# @save_send_file
def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)


@save_send_file
def non(n):
    if n%2==0:
        return True
    return False


@save_send_file
def start():
    return True

fact(100)
non(4)
start()