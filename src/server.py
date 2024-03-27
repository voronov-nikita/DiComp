# server
# All information will be received here and calculations will take place
# Then the data is sent back to the client


from threading import Thread
from datetime import datetime
import subprocess
import logging
import socket
import gzip
import os


IP:str = socket.gethostbyname(socket.gethostname())
PORT:int = 12345


SOCKET_SPEED:int = 4096
COUNT_CONNECT:int = 0
# if you use PYPY, then True
USING_PYPY:bool = False


class NewConnect(Thread):
    def __init__(self, client_socket, count_connect:int):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.count_connect:int = count_connect

    # make a record with the received data
    def write_task(self, number:int, data:bytes) -> None:
        with open(f"new{number}.txt", 'wb') as file:
            data = gzip.decompress(data)
            file.write(data)
            

    # performs the task and returns data in byte format
    def doind_task(self, file_name:str, isPypy:bool=False, otherInter:str=None) -> bytes:
        try:
            if isPypy:
                output = subprocess.check_output(['pypy', file_name]).decode()
            elif otherInter is not None:
                output = subprocess.check_output([otherInter.lower(), file_name]).decode()
            else:
                output = subprocess.check_output(['python', file_name]).decode()
            print("OUT:", output.encode()[:-2], "\n")
            return output.encode()[:-2]
        except:
            return "An error has occurred: check the correctness of the data types and compliance with the rules of writing code.".encode()


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
        
    
    def start(self):
        '''
        Start main components for server.
        '''
        self.logs("START")
        Thread(target=self.runServer, daemon=True).start()
        flag = True
        while flag:
            n = input(">> ")
            
            if n=="exit" or n == "Ex":
                print("Stopping server...")
                flag = False
                break
                
            elif n=="tasks" or n=="Ts":
                print(f"Connections: {COUNT_CONNECT}")
                logging.info(f"Connections: {COUNT_CONNECT}")
        input("Are you sure you want to suspend the server? [Enter]")
        self.logs("STOP")

    # calling for the starting server
    def runServer(self) -> None:
        '''
        The function starts the main components of the server and makes it workable.
        
        At the very beginning, it displays information about the IP address and 
        PORT of connection to the server's communication channel.
        
        '''
        
        print("<" + "--" * 10 + ">")
        print(f"SERVER IS RUN...\nIP: {self.IP}\nPORT: {self.PORT}\n")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen()
        
        while True:
            # we accept connections
            client, adress = server_socket.accept()
            self.logs("ADD", *adress)
            global COUNT_CONNECT

            COUNT_CONNECT += 1
            
            logging.info(f"Add new connect: {adress}")
            # starting a new thread
            new_connect = NewConnect(client_socket=client, count_connect=COUNT_CONNECT)
            new_connect.start()
            
    def logs(self, message:str, *any) -> None:
        '''
        Logging function for tracking errors and other concepts from the server side.
        
        It takes in the initial message for logs, then the data itself.
        '''
        fileLog = open("log.log", 'a')
        mainText:str = f"[{datetime.now()}] "
        
        if message == "START":
            fileLog.write(mainText + f"Starting the server...")
        elif message == "ADD":
            fileLog.write(mainText + f"Add new connect from {any};")
        elif message == "STOP":
            fileLog.write(mainText + f"Shutting down the server...")
        fileLog.write("\n")


if __name__=="__main__":
    server = Server(IP, PORT)
    server.start()
    
