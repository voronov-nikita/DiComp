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


NOT_SAVE:bool = True
SAVE_NAME:str = ""
        

class Dicomp():
    
    def __init__(self):
        self.IP:str = ""
        self.PORT:int = 0
        
        self.name_cache = "dicomp_cache"



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
                    
                    # вернем финальное имя для того, чтобы определить
                    return finally_name
                


            # отправка файла на сервер
            def send_files(file_name:str, client_socket):
                
                result = None

                file = open(file_name, 'rb')

                file_line = file.read()

                # отправляем пакет данных
                client_socket.sendall(file_line)

                # очищаем клиента от лишних данных
                file.close()


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
                    
                    function_name_with_args = wrapper(*args, **kwargs)
                    
                    # Проверить наличие сохранения в файле
                    try:
                        with open(f"dicomp_cache/{SAVE_NAME}", 'r') as save_file:
                            for line in save_file:
                                if function_name_with_args in line:
                                    # сразу удалим временный файл
                                    os.remove(os.path.abspath(f"task{COUNT_TASKS}.txt"))
                                    # OUTPUT FOR CLIENT
                                    if isReturn:
                                        NOT_SAVE = False
                                        
                                        # отправим файл-пустышку, чтобы сервер отработал запрос
                                        send_files(f"dicomp_cache/empty.txt", client_socket=client_socket)
                                        client_socket.close()
                                        # срез нужен из-за экранирования \n
                                        return line.split("::")[1][:-1]
                                    else:
                                        NOT_SAVE = True
                                        # срез нужен из-за экранирования \n
                                        print(line.split("::")[1][:-1])
                                    
                                    client_socket.close()
                                    break
                    except PermissionError as e:
                        print(e)
                        pass
                    
                    send_files(f"task{COUNT_TASKS}.txt", client_socket=client_socket)
                    os.remove(os.path.abspath(f"task{COUNT_TASKS}.txt"))

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
        global SAVE_NAME
        self.name_time_dir:str = "dicomp_cache"
        self.file_name:str = file_name
        SAVE_NAME = file_name
        
        self.full_directory:str = f"{self.name_time_dir}/{self.file_name}"
        
        self.output_catcher = io.StringIO()
        self.output = None
        self.file_name_calling:str = ""
        
    
    def start_save(self) -> None:
        
        stack = inspect.stack()
        # The first element of stack - it`s function
        current_frame = stack[1]
        # Get file`s name our function 
        calling_filename = current_frame.filename
        self.file_name_calling = calling_filename
        
        self.original_stdout = sys.stdout
        sys.stdout = self.output_catcher


    def stop_save(self) -> None:
        
        sys.stdout = self.original_stdout
        output = self.output_catcher.getvalue()

        # Выводим перехваченный вывод
        self.output = output
        self.save_data_in_file()
    
    
    def check_replay(self) -> list:
        list_functions:list = []
        with open(self.full_directory, 'r') as file:
            for line in file:
                if line not in list_functions:
                    list_functions.append(line.split("::")[0])
        return list_functions
    
    
    def create_direcory(self) -> None:
        try:
            os.mkdir(self.name_time_dir)
            # создадим файл-пустышку для 
            with open(f"self.name_time_dir/{empty.txt}", 'w') as file:
                file.write("print(None)")
        except FileExistsError:
            pass
        
        
    def save_data_in_file(self) -> None:
        self.create_direcory()
        list_name_function:list = []
        try:
            with open(self.file_name_calling, 'r') as file:
                wr = False
                for line in file:
                    if "start_save" in line:
                        wr = True
                    elif "stop_save" in line:
                        wr = False
                        break

                    if wr and "start_save" not in line:
                        line = line.replace("print(", "")
                        list_name_function.append(line[:-2])
                        
            
            data = self.output
            count_saving:int = 0
            
            list_already_saved:list = self.check_replay()
            
            if NOT_SAVE:
                with open(self.full_directory, 'a') as file:
                    if list_name_function[count_saving] not in list_already_saved:
                        file.write(list_name_function[count_saving] + "::" + data)
                        count_saving += 1
                
            return "Successfully saved."
        except:
            return "Saving error."
        
    
    