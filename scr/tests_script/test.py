from dicomp import SaveData, Dicomp

sv = SaveData("data.txt")
server = Dicomp()


@server.calculate(ip="192.168.8.100", port=12345)
def one(a, b):
    res = 0
    for i in range(a):
        res += b
    return res

print(one(50, 10))