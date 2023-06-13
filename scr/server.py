# Это по факту тот, кто принимает на вход какие-либо данные
# А потом выполняет определенную функцию с экземплярами этих данных
# И возвращает обратно ответ этой функции


import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()  # Получаем запрос от клиента
    # Выполняем вычисления на сервере
    result = perform_computation(request)
    # Отправляем результат клиенту
    client_socket.send(result.encode())
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Сервер запущен и ожидает подключений...")

    while True:
        client_socket, _ = server_socket.accept()
        print("Получено подключение от клиента")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def perform_computation(request):
    # Выполняем вычисления на сервере и возвращаем результат
    # В этом примере просто удваиваем полученное число
    number = int(request)
    result = number * 2
    return str(result)

if __name__ == '__main__':
    start_server()
