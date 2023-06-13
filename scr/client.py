# Это по факту тот, кто отправляет входные данные
# И принимает ответ от "сервера" в виде результата функции

import socket

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))
    client_socket.send(request.encode())  # Отправляем запрос на сервер
    response = client_socket.recv(1024).decode()  # Получаем ответ от сервера
    print("Результат вычислений:", response)
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

if __name__ == '__main__':
    request = input("Введите число для вычислений: ")
    send_request(request)
