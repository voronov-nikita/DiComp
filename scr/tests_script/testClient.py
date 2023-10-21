from dicomp import SaveData, Dicomp

sv = SaveData("data.txt")
server = Dicomp()


@server.calculate(ip="192.168.8.100", port=12345)
def one(a):
    k=1
    for i in range(1, a):
        k *= i
    return k

print(one('a'))