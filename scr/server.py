# сервер
# Здесь будет приниматься вся информация и происходить вычисления
# потом данные отправляються обратно клиенту


import socket
import subprocess
import multiprocessing
import os


IP:str = "192.168.8.100"
PORT:int = 12345

SOCKET_SPEED:int = 4096


COUNT_CONNECT:int = 0


class Commands():
    def __init__(self, client_socket):
        self.client_socket = client_socket

    # сделать запись с полученными данными
    def write_task(self, number:int, data:bytes):
        with open(f"new{number}.txt", 'wb') as file:
            file.write(data)


    # выполняет задачу и возвращает данные в байтовом формате
    def doind_task(self, file_name:str) -> bytes:
        output = subprocess.check_output(['python', file_name])
        print(output)
        return output


    def run(self):
        global COUNT_CONNECT
        while True:
            # принимаем данные от клиента
            data = self.client_socket.recv(SOCKET_SPEED)

            file_data = data

            if file_data:
                break

        self.write_task(COUNT_CONNECT, file_data)
        res = self.doind_task(f"new{COUNT_CONNECT}.txt")
        self.client_socket.sendall(res)
        os.remove(os.path.abspath(f"new{COUNT_CONNECT}.txt"))
        # COUNT_CONNECT -= 1



class Server():
    def __init__(self, IP:str, PORT:int):
        self.IP = IP
        self.PORT = PORT


    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen()


        print("<" + "--"*10 + ">")
        print(f"SERVER IS RUN...\nIP: {self.IP}\nPORT: {self.PORT}")

        while True:
            # принимаем подключения
            client, adress = server_socket.accept()
            
            global COUNT_CONNECT

            COUNT_CONNECT += 1

            print(*adress)
            
            new_connect = Commands(client_socket=client)
            
            process = multiprocessing.Process(target=new_connect.run())
            process.start()
    
        
if __name__=="__main__":
    server = Server(IP, PORT)
    server.run_server()
