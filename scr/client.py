# Решнение с использованием декораторов для упрощения использования
# Пускай теперь сам программист будет определять какую часть кода
# ему необходимо "ускорить", путем отправки файла дальше

import inspect
import socket

COUNT_TASKS:int = 0
LEN_NAME_DECORATOR:int = len("@save_send_file ")


def save_send_file(func):
    # аодготовка файлов для сервера
    def wrapper(*args, **kwargs):
        global COUNT_TASKS
        # Получение исходного кода функции
        source_code = inspect.getsource(func)

        # запись 
        with open(f"task{COUNT_TASKS}.txt", "w") as file:
            file.write(source_code[LEN_NAME_DECORATOR:])
        

        with open(f"value{COUNT_TASKS}", "w") as file:
            for elem in args:
                file.write(str(elem))
                file.write("\n")

        COUNT_TASKS+=1


    # отправка файла на сервер
    def send_file(file_name:str, ip:str, port:int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))

        except:
            print("ERROR CONNECT")

    def get_result():
        return None


    # запуск всех состовляющих
    def run(*args, **kwargs):
        wrapper(*args, **kwargs)
        result = get_result()
        print(COUNT_TASKS)
        return result

    return run
