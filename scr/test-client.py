import socket

def run_client(host, port):
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Устанавливаем соединение с сервером
        client_socket.connect((host, port))
        
        while True:
            # Вводим сообщение для отправки серверу
            message = input("Введите сообщение ('q' для выхода): ")
            
            if message == 'q':
                # Выходим из цикла, если пользователь ввел 'q'
                break
            
            # Отправляем сообщение серверу
            client_socket.sendall(message.encode())
            
            # Принимаем ответ от сервера
            data = client_socket.recv(1024)
            
            print(f"Ответ от сервера: {data.decode()}")
    finally:
        # Закрываем соединение
        client_socket.close()

# Пример использования
host = 'localhost'
port = 12345
run_client(host, port)
