import numpy as np




def stop(*func):
    ls=[10, 11, 12, 13, 14, 15]
    return func[0](ls) - func[1](ls)

print(stop(np.max, np.min))