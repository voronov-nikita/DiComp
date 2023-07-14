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
    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket


    def run(self):
        while True:
            # принимаем данные от клиента
            data = self.client_socket.recv(SOCKET_SPEED)

            file_data = data

            if file_data:
                break

        write_task(self.count_connect, file_data)
        res = doind_task(f"new{self.count_connect}.txt")
        self.client_socket.sendall(res)
        os.remove(os.path.abspath(f"new{self.count_connect}.txt"))
        # COUNT_CONNECT -= 1



class Server():
    def __init__(self, IP:str, PORT:int):
        self.count_connect = 0
        self.IP = IP
        self.PORT = PORT

    # сделать запись с полученными данными
    def write_task(self, number:int, data:bytes):
        with open(f"new{number}.txt", 'wb') as file:
            file.write(data)
            


    # выполняет задачу и возвращает данные в байтовом формате
    def doind_task(self, file_name:str) -> bytes:
        output = subprocess.check_output(['python', file_name])
        print(output)
        return output



    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen()


        print("<" + "--"*10 + ">")

        while True:
            # принимаем подключения
            client, adress = server_socket.accept()

            self.count_connect += 1

            print(*adress)
            
            new_client = NewThread(client)
            new_client.start()
    
        
if __name__=="__main__":
    server = Server(IP, PORT)
    server.run_server()
