#
# Файл с использованием декораторов для упрощения использования
# Теперь пусть программист сам определяет, какую часть кода
# ему нужно "ускорить", отправив файл дальше
#

# >>> pip install inspect
import inspect
import socket
import gzip
import sys
import io
import os


COUNT_TASKS: int = 0
SOCKET_SPEED: int = 4096


NOT_SAVE: bool = True
SAVE_NAME: str = ""


class Dicomp():
    def __init__(self):
        self.IP: str = ""
        self.PORT: int = 0

        self.name_folder_cache = "dicomp_cache"

    # функция декоратора для отправки файла на сервер и возврата результата
    def calculate(self, ip: str, port: int, isReturn: bool = True, useSave: bool = True) -> str:
        '''
        Функция декоратора. 
        Вся основная логика происходит прямо здесь. 

        Вызовите этот метод перед вашей функцией, которую необходимо распространить.
        '''

        def new_send_file(func):

            # подготовка файлов для сервера
            def wrapper(*args, **kwargs):
                global COUNT_TASKS
                # Получение исходного кода функции
                source_code: str = inspect.getsource(func)

                LEN_NAME_DECORATE: int = len(
                    source_code[source_code.index("@"):source_code.index("def")])

                # записи задачи
                with open(f"task{COUNT_TASKS}.txt", "w") as file:
                    file.write(source_code[LEN_NAME_DECORATE:])

                    line = source_code.split('\n')[1]
                    new_function_name: str = line[4:line.index(":")]
                    function_name: str = line[4:line.index(":")]

                    # если у функции есть аргументы, то
                    # преобразуем имя так, чтобы оно соответствовало
                    if len(kwargs) != 0:
                        function_name = function_name[function_name.index(
                            "(")+1:]
                        for key, value in kwargs.items():
                            if type(value) == str:
                                function_name = function_name.replace(
                                    key, f"'{value}'")
                            else:
                                function_name = function_name.replace(
                                    key, str(value))

                    if len(args) != 0:
                        time_function_name: str = function_name[:function_name.index(
                            "(")+1]
                        for elems in range(len(args)):
                            if elems == len(args)-1:
                                if str(args[elems]).isalpha():
                                    time_function_name += "'" + \
                                        str(args[elems]) + "'"
                                else:
                                    time_function_name += str(args[elems])
                            else:
                                if str(args[elems]).isalpha():
                                    time_function_name += "'" + \
                                        str(args[elems]) + "',"
                                else:
                                    time_function_name += str(
                                        args[elems]) + ","
                        time_function_name += ")"
                        finally_name: str = time_function_name

                    else:
                        finally_name: str = function_name

                    file.write(f"print({finally_name})")

                    # вернем финальное имя
                    return finally_name

            # отправить файл на сервер
            def send_files(file_name: str, client_socket):

                file = open(file_name, 'rb')

                file_line = file.read()
                compressed_data = gzip.compress(file_line)

                # отправка сжатого файла для увеличения скорости
                client_socket.sendall(compressed_data)

                # очистка временных файлов
                file.close()

            # мы ожидаем сообщения от сервера до тех пор, пока оно не поступит, чтобы получить результат

            def get_result(client_socket):
                '''
                Функция, которая возвращает окончательное полученное сообщение.
                Когда данные перестанут поступать, функция автоматически вернет результат.
                '''

                result_data = b""

                while True:
                    data = client_socket.recv(SOCKET_SPEED)
                    if not data:
                        return result_data.decode()
                    result_data += data

            # подгрузка все компонетов для запуска

            def run(*args, **kwargs):
                try:
                    client_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))

                    function_name_with_args = wrapper(*args, **kwargs)

                    # Проверка на готовый файл с сохранением
                    try:
                        if useSave:
                            with open(f"{self.name_folder_cache}/{SAVE_NAME}", 'r') as save_file:
                                for line in save_file:
                                    if function_name_with_args in line:
                                        global NOT_SAVE
                                        NOT_SAVE = True
                                        # немедленное удаление временного файла
                                        os.remove(os.path.abspath(
                                            f"task{COUNT_TASKS}.txt"))
                                        # ВЫХОДНЫЕ ДАННЫЕ ДЛЯ КЛИЕНТА
                                        if isReturn:
                                            # мы отправим фиктивный файл, чтобы сервер обработал запрос
                                            send_files(
                                                f"{self.name_folder_cache}/empty.txt", client_socket=client_socket)
                                            client_socket.close()
                                            # срез необходим из-за экранирования \n
                                            return eval(line.split("::")[1][:-1])
                                        else:
                                            # срез необходим из-за экранирования \n
                                            print(line.split("::")[1][:-1])

                                        client_socket.close()
                                        break
                                    else:
                                        NOT_SAVE = False
                    except PermissionError:
                        pass
                    except FileNotFoundError:
                        pass

                    send_files(f"task{COUNT_TASKS}.txt",
                               client_socket=client_socket)
                    os.remove(os.path.abspath(f"task{COUNT_TASKS}.txt"))

                    result = get_result(client_socket=client_socket)
                    client_socket.close()

                    # ВЫХОДНЫЕ ДАННЫЕ ДЛЯ КЛИЕНТА
                    if isReturn:
                        try:
                            return eval(result)
                        except:
                            return result
                    else:
                        print(result[:-6])

                except ConnectionRefusedError as error:
                    print("ConnectionRefusedError:\tFailed to connect to the server.")
                    sys.exit()

            return run
        return new_send_file


# Класс для сохранения данных с сервера.
# Теперь вам не нужно повторно отправлять один и тот же запрос, чтобы получить ответ
class SaveData():
    def __init__(self, file_name: str):
        global SAVE_NAME
        self.name_time_dir: str = "dicomp_cache"
        self.file_name: str = file_name
        SAVE_NAME = file_name

        self.full_directory: str = f"{self.name_time_dir}/{self.file_name}"

        self.output_catcher = io.StringIO()
        self.output = None
        self.file_name_calling: str = ""

    def start_save(self) -> None:
        '''
        Функция начнет считывать все данные из консоли и
переводить их в интерпретатор.
        Значение берется из интерпретатора и записывается в переменную.

        Ничего не возвращает. 
        В своей конструкции требуется метод end_save().
        '''

        stack = inspect.stack()
        # Первый элемент стека - это функция
        current_frame = stack[1]
        # Получение имени файл для записи
        calling_filename = current_frame.filename
        self.file_name_calling = calling_filename

        self.original_stdout = sys.stdout
        sys.stdout = self.output_catcher

    def stop_save(self) -> None:

        sys.stdout = self.original_stdout
        output = self.output_catcher.getvalue()

        self.output = output
        self.save_data_in_file()

    def check_replay(self) -> list:
        try:
            list_functions: list = []
            with open(self.full_directory, 'r') as file:
                for line in file:
                    if line not in list_functions:
                        list_functions.append(line.split("::")[0])
            return list_functions
        except FileNotFoundError:
            return []

    # создает папку, в которую будут помещены все сохраненные файлы
    # + создает пустой файл
    def create_direcory(self) -> None:
        try:
            os.mkdir(self.name_time_dir)
            # создаем пустой файл
            with open(f"{self.name_time_dir}/empty.txt", 'w') as file:
                file.write("print(None)")
        except FileExistsError:
            pass

    def save_data_in_file(self) -> None:
        '''
        функция, которая реализует
        создание файла с сохраненными значениями функции или подключение к нему.
        '''
        self.create_direcory()
        list_name_function: list = []
        try:
            with open(self.file_name_calling, 'r') as file:
                wr = False
                for line in file:
                    if "start_save" in line:
                        wr = True
                    elif "stop_save" in line:
                        wr = False
                        break

                    if wr and "start_save" not in line and line != "\n":
                        line = line.replace("print(", "")
                        list_name_function.append(line[:-2])

            data = self.output.split("\n")

            list_already_saved: list = self.check_replay()
            if NOT_SAVE:
                # открыть файл на добавление (append)
                with open(self.full_directory, 'a') as file:
                    for elems in range(len(list_name_function)):
                        if list_name_function[elems] not in list_already_saved:
                            file.write(
                                list_name_function[elems] + "::" + data[elems] + "\n")

            print("Successfully saved.")
            return "Successfully saved."
        except:
            print("Saving Error.")
            return "Saving Error."
