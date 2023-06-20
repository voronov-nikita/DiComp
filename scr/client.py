# Решнение с использованием декораторов для упрощения использования
# Пускай теперь сам программист будет определять какую часть кода
# ему необходимо "ускорить", путем отправки файла дальше

import inspect
import socket
import threading
import os


COUNT_TASKS:int = 0
LEN_NAME_DECORATOR:int = len("@save_send_file ")
SOCKET_SPEED:int = 4096

IP:str = "127.0.0.1"
PORT:int = 12345



def save_send_file(func):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # подготовка файлов для сервера
    def wrapper(*args, **kwargs):
        global COUNT_TASKS
        # Получение исходного кода функции
        source_code = inspect.getsource(func)

        # запись задачи
        with open(f"task{COUNT_TASKS}.txt", "w") as file:
            file.write(source_code[LEN_NAME_DECORATOR:])
        
        # соответсвующие значения для функций
        with open(f"value{COUNT_TASKS}.txt", "w") as file:
            for elem in args:
                file.write(str(elem))
                file.write("\n")

        COUNT_TASKS+=1


    # отправка файла на сервер
    def send_file(file_name:str):

        result = None

        try:
            client_socket.connect((IP, PORT))
            file = open(file_name, 'rb')

            file_line = file.read()

            # отправляем пакет данных
            client_socket.sendall(file_line)

            # очищаем клиента от лишних данных
            file.close()
            os.remove(f"/{file_name}")
            os.remove(f"/{file_name}")

            # Принимаем ответ от сервера
            data = client_socket.recv(SOCKET_SPEED)
            result = data

            while not data:
                result += data

            return result.decode()

        except:
            print("ERROR CONNECT")


    # получить результат
    # здесь мы будем ждать сообщение от сервера до тех пор, пока оно не придет
    def get_result():
        result = None
        while True:
            result_data = client_socket.recv(SOCKET_SPEED)
            if result_data:
                result = result_data.decode()
                break

        return result


    # запуск всех состовляющих
    def run(*args, **kwargs):
        wrapper(*args, **kwargs)

        for i in range(COUNT_TASKS):
            send_file(f"task{i}.txt")
            send_file(f"value{i}.txt")


        result = get_result()
        print(COUNT_TASKS)
        return result

    return run

