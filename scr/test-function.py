import multiprocessing
from time import time


def f():
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(5):
                k +=  i*g*x
    print(k)
    

def f2():
    k=0
    for i in range(1000):
        for g in range(1000):
            for x in range(5):
                k +=  i*g*x
    print(k)


def run_process(func):
    return func()

if __name__ == '__main__':
    start = time()
    ls = [f, f2]
    print(ls)
    
    # Количество процессов, которые будут использованы
    num_processes = multiprocessing.cpu_count()

    # Создаем пул процессов
    pool = multiprocessing.Pool(processes=num_processes)
    
    processed_array = pool.map(run_process, ls)

    # Закрываем пул процессов
    pool.close()
    pool.join()
    
    print(time() - start)