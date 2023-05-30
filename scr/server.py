# Сервер
# Это та чать, которая отправляет задачи
# на другие компьютеры. Здесь же происходит рапределение задач на подзадачи.


# <============= Импорты библиотек =============>
import socket
import threading


def create_connect(ip:str, port:int):
    sock = socket.socket()
    sock.connect((ip, port))

    
create_connect(socket.gethostbyname_ex(socket.gethostname())[-1][-1], 9999)