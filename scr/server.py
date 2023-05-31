# Сервер
# Это та чать, которая отправляет задачи
# на другие компьютеры. Здесь же происходит рапределение задач на подзадачи.


# <============= Импорты библиотек =============>
import socket
import threading


def create_connect(ip:str, port:int):
    sock = socket.socket()
    sock.connect((ip, port))

    
class Boss:
    def __init__(self):
        print("OK")