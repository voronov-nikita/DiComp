# Решнение с использованием декораторов для упрощения использования
# Пускай теперь сам программист будет определять какую часть кода
# ему необходимо "ускорить", путем отправки файла дальше


from threading import Thread
# >>> pip install inspect
import inspect
import socket
import sys
import io
import os


COUNT_TASKS:int = 0
SOCKET_SPEED:int = 4096
        

class Dicomp():
    
    def __init__(self):
        self.IP:str = ""
        self.PORT:int = 0


    # функция-декоратор для отправки файла на сервер и возвращению результата
    def calculate(self, ip:str, port:int, isReturn:bool=False) -> str:
        def new_send_file(func):

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
            def send_files(file_name:str, client_socket):
                
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
            def get_result(client_socket):
                result = None
                
                while True:
                    result_data = client_socket.recv(SOCKET_SPEED)
                    if result_data:
                        result = result_data.decode()
                        break

                return result


            # запуск всех состовляющих
            def run(*args, **kwargs):
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))
                    
                    wrapper(*args, **kwargs)

                    send_files(f"task{COUNT_TASKS}.txt", client_socket=client_socket)


                    result = get_result(client_socket=client_socket)
                    client_socket.close()
                    
                    # OUTPUT FOR CLIENT
                    if isReturn:
                        return result
                    else:
                        print(result)
                        
                except ConnectionRefusedError as error:
                    print("ConnectionRefusedError:\tFailed to connect to the server.")
                    sys.exit()

            return run
        return new_send_file


# Class for save the data from server.
# Now you don't need to send the same request again to get a response
class SaveData():
    def __init__(self, file_name:str):
        self.name_time_dir:str = "cache"
        self.file_name:str = file_name
    
    def create_direcory(self):
        os.mkdir(self.name_time_dir)
        
    
    def save(self):
        try:
            data = ""
            with open(self.file_name, 'w') as file:
                file.write(data)
                
            return "Successfully saved."
        except:
            return "Saving error."
        
    
    