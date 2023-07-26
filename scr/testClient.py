
import multiprocessing

def dec(func):
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        process.join()
    return wrapper