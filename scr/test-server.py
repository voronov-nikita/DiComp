import socket

def run_server(host, port):
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Привязываем сокет к указанному хосту и порту
    server_socket.bind((host, port))
    
    # Запускаем прослушивание входящих соединений
    server_socket.listen()
    
    print("Сервер запущен. Ожидание подключений...")
    
    while True:
        # Принимаем входящее соединение
        client_socket, client_address = server_socket.accept()
        
        print(f"Установлено соединение с клиентом: {client_address[0]}:{client_address[1]}")
        
        try:
            while True:
                # Принимаем данные от клиента
                data = client_socket.recv(1024)
                
                if not data:
                    # Клиент закрыл соединение
                    break
                
                print(data.decode())
                # Обрабатываем полученные данные
                # В данном примере просто отправляем их обратно клиенту
                client_socket.sendall(data)
        finally:
            # Закрываем соединение с клиентом
            client_socket.close()

# Пример использования
host = 'localhost'
port = 12345
run_server(host, port)
