from dicomp import SaveData, Dicomp

sv = SaveData("data1.txt")
server = Dicomp()


@server.calculate(ip="192.168.8.103", port=12345, isReturn=True)
def one(a):
    return a

sv.start_save()
print(one(70))

sv.stop_save()