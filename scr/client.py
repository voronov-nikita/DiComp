# Решнение с использованием декораторов для упрощения использования
# Пускай теперь сам программист будет определять какую часть кода
# ему необходимо "ускорить", путем отправки файла дальше


# >>> pip install inspect
import inspect
import socket
import threading
import os


COUNT_TASKS:int = 0
SOCKET_SPEED:int = 4096

IP:str=""
PORT:int=0


class Xsay():
    
    def __init__(self):
        self.IP:str = ""
        self.PORT:int = 0
        self.other_functions:list = []
    
    # функция для подключения к серверу
    def connect_server(self, ip:str, port:int):
        self.IP=ip
        self.PORT=port
        
    def add_function(self, *args):
        self.other_functions = args

    # функция-декоратор для отправки файла на сервер и возвращению результата
    def send_file(self, func):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # подготовка файлов для сервера
        def wrapper(*args, **kwargs):
            global COUNT_TASKS
            # Получение исходного кода функции
            source_code = inspect.getsource(func)
            
            LEN_NAME_DECORATE:int = len(source_code[source_code.index("@"):source_code.index("def")])

            # запись задачи 
            with open(f"task{COUNT_TASKS}.txt", "w") as file:
                file.write(source_code[LEN_NAME_DECORATE:])
                line = source_code.split('\n')[1]
                new_function_name = line[4:line.index(":")]
                function_name = line[4:line.index(":")]
                
                # если аргументы к функции есть, то
                # преобразовываем имя так, чтобы оно соответствовало
                if len(kwargs) != 0:
                    function_name = function_name[function_name.index("(")+1:]
                    for key, value in kwargs.items():
                        if type(value) == str:
                            function_name = function_name.replace(key, f"'{value}'")
                        else:
                            function_name = function_name.replace(key, str(value))


                elif len(args) != 0:
                    function_name = function_name[:function_name.index("(")+1]
                    function_name += str(args)[1:-1] + "))"
                
                finally_name = new_function_name[:new_function_name.index("(")+1] + function_name 
                file.write(f"print({finally_name})")
            

            COUNT_TASKS+=1


        # отправка файла на сервер
        def send_file(file_name:str):
            

            result = None

            file = open(file_name, 'rb')

            file_line = file.read()

            # отправляем пакет данных
            client_socket.sendall(file_line)

            # очищаем клиента от лишних данных
            file.close()
            os.remove(os.path.abspath(f"{file_name}"))
            
            # client_socket.close()



        # получить результат
        # здесь мы будем ждать сообщение от сервера до тех пор, пока оно не придет
        def get_result():
            result = None
            
            while True:
                result_data = client_socket.recv(SOCKET_SPEED)
                if result_data:
                    result = result_data.decode()
                    break

            return result


        # запуск всех состовляющих
        def run(*args, **kwargs):
            client_socket.connect((self.IP, self.PORT))
            wrapper(*args, **kwargs)

            for i in range(COUNT_TASKS):
                send_file(f"task{i}.txt")


            result = get_result()
            print("-"*10)
            print(f"Количество задействованных серверов: {COUNT_TASKS}")
            return result

        return run

