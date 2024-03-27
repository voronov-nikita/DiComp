import sys

sys.path.append("../")


from src.dicomp import SaveData, Dicomp

sv = SaveData("data.txt")
server = Dicomp()


@server.calculate(ip="172.27.16.1", port=12345)
def one(a):
    k=1
    for i in range(1, a):
        k *= i
    return k

print(one(10))