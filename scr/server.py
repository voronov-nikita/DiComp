# сервер
# Здесь будет приниматься вся информация и происходить вычисления
# потом данные отправляються обратно клиенту


import socket
import subprocess
from threading import Thread
import os


IP:str = "192.168.8.104"
PORT:int = 12345

SOCKET_SPEED:int = 4096


class NewThread(Thread):
    def __init__(self, task_number:int):
        pass


# сделать запись с полученными данными
def write_task(number:int, data:bytes):
    with open(f"new{number}.txt", 'wb') as file:
        file.write(data)
        


# выполняет задачу и возвращает данные в байтовом формате
def doind_task(file_name:str) -> bytes:
    output = subprocess.check_output(['python', file_name])
    print(output)
    return output


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    count_connect:int = 0

    print("<" + "--"*10 + ">")

    while True:
        # принимаем подключения
        client, adress = server_socket.accept()

        count_connect += 1

        print(*adress)

        while True:
            # принимаем данные от клиента
            data = client.recv(SOCKET_SPEED)

            file_data = data

            if file_data:
                break

        write_task(count_connect, file_data)
        res = doind_task(f"new{count_connect}.txt")
        client.sendall(res)
        os.remove(os.path.abspath(f"new{count_connect}.txt"))
        count_connect -= 1
        


if __name__=="__main__":
    run_server()
