# сервер
# Здесь будет приниматься вся информация и происходить вычисления
# потом данные отправляються обратно клиенту


import socket
import subprocess
from threading import Thread
import os


IP:str = socket.gethostbyname(socket.gethostname())
PORT:int = 12345

SOCKET_SPEED:int = 4096


COUNT_CONNECT:int = 0
USING_PYPY:bool = True


class NewThread(Thread):
    def __init__(self, client_socket, count_connect:int):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.count_connect:int = count_connect

    # сделать запись с полученными данными
    def write_task(self, number:int, data:bytes):
        with open(f"new{number}.txt", 'wb') as file:
            file.write(data)


    # выполняет задачу и возвращает данные в байтовом формате
    def doind_task(self, file_name:str, isPypy:bool=False) -> bytes:
        if isPypy:
            output = subprocess.check_output(['pypy', file_name])
        else:
            output = subprocess.check_output(['python', file_name])
        print("OUT:", output[:-4], "\n")
        return output[:-4]


    def run(self):
        while True:
            # принимаем данные от клиента
            data = self.client_socket.recv(SOCKET_SPEED)

            file_data = data

            if file_data:
                break

        self.write_task(self.count_connect, file_data)
        res = self.doind_task(f"new{self.count_connect}.txt", isPypy=USING_PYPY)
        self.client_socket.sendall(res)
        os.remove(os.path.abspath(f"new{self.count_connect}.txt"))
        self.client_socket.close()



class Server():
    def __init__(self, IP:str, PORT:int):
        self.IP = IP
        self.PORT = PORT


    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen()


        print("<" + "--"*10 + ">")
        print(f"SERVER IS RUN...\nIP: {self.IP}\nPORT: {self.PORT}\n")

        while True:
            # принимаем подключения
            client, adress = server_socket.accept()
            
            global COUNT_CONNECT

            COUNT_CONNECT += 1

            print(*adress)
            
            new_connect = NewThread(client_socket=client, count_connect=COUNT_CONNECT)
            new_connect.start()
    
        
if __name__=="__main__":
    server = Server(IP, PORT)
    server.run_server()
