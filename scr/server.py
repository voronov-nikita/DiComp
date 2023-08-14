# server
# All information will be received here and calculations will take place
# Then the data is sent back to the client


from threading import Thread
import subprocess
import socket
import signal
import os


IP:str = socket.gethostbyname(socket.gethostname())
PORT:int = 12345


SOCKET_SPEED:int = 4096
COUNT_CONNECT:int = 0
# if you use PYPY, then True
USING_PYPY:bool = True




class NewConnect(Thread):
    def __init__(self, client_socket, count_connect:int):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.count_connect:int = count_connect

    # make a record with the received data
    def write_task(self, number:int, data:bytes) -> None:
        with open(f"new{number}.txt", 'wb') as file:
            file.write(data)
            

    # performs the task and returns data in byte format
    def doind_task(self, file_name:str, isPypy:bool=False, otherInter:str=None) -> bytes:
        if isPypy:
            output = subprocess.check_output(['pypy', file_name]).decode()
        elif otherInter is not None:
            output = subprocess.check_output([otherInter.lower(), file_name]).decode()
        else:
            output = subprocess.check_output(['python', file_name]).decode()
        print("OUT:", output.encode()[:-2], "\n")
        return output.encode()[:-2]


    def run(self) -> None:
        while True:
            # we accept data from the client
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


    def kill_server(self, sig, frame):
        exit(0)

    # calling for the starting server
    def run_server(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen()


        print("<" + "--"*10 + ">")
        print(f"SERVER IS RUN...\nIP: {self.IP}\nPORT: {self.PORT}\n")

        # Установка обработчика сигнала SIGINT
        signal.signal(signal.SIGINT, self.kill_server)
        
        while True:
            # we accept connections
            client, adress = server_socket.accept()
            
            global COUNT_CONNECT

            COUNT_CONNECT += 1

            print(*adress)
            
            # starting a new thread
            new_connect = NewConnect(client_socket=client, count_connect=COUNT_CONNECT)
            new_connect.start()
    
        
if __name__=="__main__":
    server = Server(IP, PORT)
    server.run_server()
    
