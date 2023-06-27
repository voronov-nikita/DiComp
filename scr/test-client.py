from new import dec

@dec
def go(a, b):
    return int(a) + int(b)


print(go(b="10", a=100))

