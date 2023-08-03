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
      
    # NOT WORKED!!!
    def add_function(self, *args):
        self.other_functions = args

    # функция-декоратор для отправки файла на сервер и возвращению результата
    def send_file(self, ip:str, port:int):
        def new_send_file(func):
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
                    new_function_name:str = line[4:line.index(":")]
                    function_name:str = line[4:line.index(":")]
                    
                    # если аргументы к функции есть, то
                    # преобразовываем имя так, чтобы оно соответствовало
                    if len(kwargs) != 0:
                        function_name = function_name[function_name.index("(")+1:]
                        for key, value in kwargs.items():
                            if type(value) == str:
                                function_name = function_name.replace(key, f"'{value}'")
                            else:
                                function_name = function_name.replace(key, str(value))

                    if len(args) != 0:
                        time_function_name:str = function_name[:function_name.index("(")+1]
                        time_function_name += str(*args) + ")"
                        finally_name:str = time_function_name
                    
                    else:
                        finally_name:str = function_name
                        
                    file.write(f"print({finally_name})")
                


            # отправка файла на сервер
            def send_files(file_name:str):
                
                result = None

                file = open(file_name, 'rb')

                file_line = file.read()

                # отправляем пакет данных
                client_socket.sendall(file_line)

                # очищаем клиента от лишних данных
                file.close()
                os.remove(os.path.abspath(f"{file_name}"))


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
                client_socket.connect((ip, port))
                
                wrapper(*args, **kwargs)

                send_files(f"task{COUNT_TASKS}.txt")


                result = get_result()
                client_socket.close()
                return result

            return run
        return new_send_file

