from dicomp import SaveData, Dicomp

sv = SaveData("data.txt")
server = Dicomp()


@server.calculate(ip="192.168.8.103", port=12345, isReturn=True)
def one(a):
    return a

# sv.start_save()

print(one(70))
print(one(10))
print(one(200))
print(one(400))
print(one(300))
print(one(300243243))

# sv.stop_save()