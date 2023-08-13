# Documentation


**Dicomp** - это самописная библиотека Python, которая служит для некоторого ускорения кода на python путем распределения базовых вычислений по одному или нескольким серверам или процессорам.

>from dicomp import Dicomp


Чтобы подключиться к серверу, используйте функцию-декоратор из модуля Dicomp -> *@calculate*

1. Пример со стороны пользователя:
    ```python
    from dicomp import Dicomp

    # initializing the Dicomp object
    server = Dicomp()

    # this decorator takes in the values of the IP address and port to connect to the server on which the calculations will be performed.
    @server.calculate(ip="0.0.0.0", port=0)
    def function_one(a, b):
        # your code
        return a + b

    # Be sure to call the function
    function_one(10, 50)
    ```

2. Пример вывода с сервера:

    ```Bash
    SERVER IS RUN... 
    IP: 0.0.0.0
    PORT: 0

    192.168.0.0 523462
    OUT: b'60'

    ```



###### 11.08.2023 - last README.md change.