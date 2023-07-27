import multiprocessing


def task():
    k = 0
    print(k)
    return k


for i in range(3):
    process = multiprocessing.Process(target=task)
    process.run()
    