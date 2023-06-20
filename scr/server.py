# сервер
# Здесь будет приниматься вся информация и происходить вычисления
# потом данные отправляються обратно клиенту


import socket
import subprocess
import sys
from threading import Thread


IP:str = "192.168.8.102"
PORT:int = 12345

SOCKET_SPEED:int = 4096


class NewThread(Thread):
    def __init__(self, task_number:int):
        pass


# сделать запись с полученными данными
def write_task(number:int, data:bytes):
    with open(f"new{number}.txt", 'wb') as file:
        file.write(data)


def doind_task(file_name:str):
    subprocess.run(["python", file_name])
    print(sys.__stdout__)


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
        doind_task(f"new{count_connect}.txt")



if __name__=="__main__":
    run_server()
