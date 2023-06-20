import socket
from threading import Thread


server_socket = socket.socket()

IP:str = "172.0.0.1"
PORT:int = 12345

server_socket.bind((IP, PORT))


server_socket.listen()



class NewTask(Thread):
    def __init__(self):
        pass



while True:
    # начинаем принимать соединения
    conn, addr = server_socket.accept()

    # выводим информацию о подключении
    print('connected:', addr)

    # получаем название файла
    name_f = (conn.recv(1024)).decode ('UTF-8')

    # открываем файл в режиме байтовой записи в отдельной папке 'sent'
    f = open(name_f,'wb')

    while True:

        # получаем байтовые строки
        l = conn.recv(1024)

        # пишем байтовые строки в файл на сервере
        f.write(l)

        if not l:
            break

    f.close()
    conn.close()

    print('File received')

sock.close()