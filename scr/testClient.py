from dicomp import SaveData, Dicomp

sv = SaveData("data.txt")
server = Dicomp()


@server.calculate(ip="192.168.8.101", port=12345)
def one(a):
    ls=[]
    for i in range(a):
        ls.append([i] * i)
    return ls

