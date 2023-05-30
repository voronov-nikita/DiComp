# Клиент
# Получает файлы и зaдачи, которые должен обраюотать
# Здесь же происходит отправка результатов вычислений обратно на сервер.


# <============= Импорты библиотек =============>
import socket
import threading


def accept_connect(ip:str, port:int):
    while True:
        sock = socket.socket()
        sock.bind((ip, port))
        sock.listen()
        conn, addr = sock.accept()
        print(conn, addr)


k = accept_connect(socket.gethostbyname_ex(socket.gethostname())[-1][-1], 9999)
print(k)
