#
# Файл, хранящий в себе исходный код для организации блокчейн системы
# В файле представлены базовые и необходимые для организации действия при развертывании блокчейна
#

from threading import Thread
import configparser
import hashlib
import socket
import json
import time


# Описание конфигурации текущего файла
config = configparser.ConfigParser()
config.read('config.ini')

# Получение значений из файла конфигурации
HOST: str = config['BlockChain']['host']
PORT: int = int(config['BlockChain']['port'])


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


def handle_connection(client_socket, blockchain):
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        if request == "GET_CHAIN":
            response = json.dumps(
                [block.__dict__ for block in blockchain.chain])
            client_socket.send(response.encode())
        elif request == "ADD_BLOCK":
            data = client_socket.recv(1024).decode()
            data = json.loads(data)
            index = len(blockchain.chain)
            new_block = Block(index, time.time(), data,
                            blockchain.get_latest_block().hash)
            blockchain.add_block(new_block)
            client_socket.send("Block added successfully".encode())
    client_socket.close()


def start():
    blockchain = Blockchain()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server listening on port", PORT)

    while True:
        client_socket, address = server_socket.accept()
        print("Connection from", address)
        client_handler = Thread(target=handle_connection,
                                args=(client_socket, blockchain))
        client_handler.start()


if __name__ == "__main__":
    ex = start()
