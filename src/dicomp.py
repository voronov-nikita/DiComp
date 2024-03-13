# Solution using decorators to simplify usage
# Now let the programmer himself determine which part of the code
# he needs to "speed up" by sending the file further


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
        
        self.name_folder_cache = "dicomp_cache"


    # a decorator function for sending a file to the server and returning the result
    def calculate(self, ip:str, port:int, isReturn:bool=True, useSave:bool=True) -> str:
        
        '''
        The decorator function. 
        All the basic logic happens right here. 
        
        Call this method before your function that needs to be distributed.
        '''
        
        def new_send_file(func):

            # preparing files for the server
            def wrapper(*args, **kwargs):
                global COUNT_TASKS
                # Getting the source code of the function
                source_code:str = inspect.getsource(func)
                
                LEN_NAME_DECORATE:int = len(source_code[source_code.index("@"):source_code.index("def")])

                # write a task
                with open(f"task{COUNT_TASKS}.txt", "w") as file:
                    file.write(source_code[LEN_NAME_DECORATE:])
                    
                    line = source_code.split('\n')[1]
                    new_function_name:str = line[4:line.index(":")]
                    function_name:str = line[4:line.index(":")]
                    
                    # if there are arguments to the function, then
                    # converting the name so that it matches
                    if len(kwargs) != 0:
                        function_name = function_name[function_name.index("(")+1:]
                        for key, value in kwargs.items():
                            if type(value) == str:
                                function_name = function_name.replace(key, f"'{value}'")
                            else:
                                function_name = function_name.replace(key, str(value))

                    if len(args) != 0:
                        time_function_name:str = function_name[:function_name.index("(")+1]
                        for elems in range(len(args)):
                            if elems == len(args)-1:
                                if str(args[elems]).isalpha():
                                    time_function_name += "'" + str(args[elems]) + "'"
                                else:
                                    time_function_name += str(args[elems])
                            else:
                                if str(args[elems]).isalpha():
                                    time_function_name += "'" + str(args[elems]) + "',"
                                else:
                                    time_function_name += str(args[elems]) + ","
                        time_function_name += ")"
                        finally_name:str = time_function_name
                    
                    else:
                        finally_name:str = function_name
                        
                    file.write(f"print({finally_name})")
                    
                    # вернем финальное имя
                    return finally_name


            # sending a file to the server 
            def send_files(file_name:str, client_socket):

                file = open(file_name, 'rb')

                file_line = file.read()

                # sending a data packet
                client_socket.sendall(file_line)

                # clearing the client of unnecessary data
                file.close()


            # we are waiting for a message from the server until it arrives to get the result
            def get_result(client_socket):
                '''
                A function that returns the final received message.
                When the data stops coming, the function will automatically return the result.
                '''
                
                result_data = b""
                
                while True:
                    data = client_socket.recv(SOCKET_SPEED)
                    if not data:
                        return result_data.decode()
                    result_data += data


            # launching all components
            def run(*args, **kwargs):
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))
                    
                    function_name_with_args = wrapper(*args, **kwargs)
                    

                    # Check if there is a save in the file
                    try:
                        if useSave:
                            with open(f"{self.name_folder_cache}/{SAVE_NAME}", 'r') as save_file:
                                for line in save_file:
                                    if function_name_with_args in line:
                                        global NOT_SAVE
                                        NOT_SAVE = True
                                        # immediately delete the temporary file
                                        os.remove(os.path.abspath(f"task{COUNT_TASKS}.txt"))
                                        # OUTPUT FOR CLIENT
                                        if isReturn:
                                            # we will send a dummy file so that the server will work out the request
                                            send_files(f"{self.name_folder_cache}/empty.txt", client_socket=client_socket)
                                            client_socket.close()
                                            # the slice is needed because of the \n escaping
                                            return eval(line.split("::")[1][:-1])
                                        else:
                                            # the slice is needed because of the \n escaping
                                            print(line.split("::")[1][:-1])
                                        
                                        client_socket.close()
                                        break
                                    else:
                                        NOT_SAVE = False
                    except PermissionError:
                        pass
                    except FileNotFoundError:
                        pass
                    
                    send_files(f"task{COUNT_TASKS}.txt", client_socket=client_socket)
                    os.remove(os.path.abspath(f"task{COUNT_TASKS}.txt"))

                    result = get_result(client_socket=client_socket)
                    client_socket.close()
                    
                    # OUTPUT FOR CLIENT
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
        '''
        The function will start reading everything from the console and 
        translating it to the interpreter.
        The value is taken from the interpreter and written to a variable.
        
        Returns nothing. 
        Requires the end_save() method in its construction.
        '''
        
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

        self.output = output
        self.save_data_in_file()
    
    
    def check_replay(self) -> list:
        try:
            list_functions:list = []
            with open(self.full_directory, 'r') as file:
                for line in file:
                    if line not in list_functions:
                        list_functions.append(line.split("::")[0])
            return list_functions
        except FileNotFoundError:
            return []
    
    # creates a folder where all the saves will be placed
    # + creates an empty file
    def create_direcory(self) -> None:
        try:
            os.mkdir(self.name_time_dir)
            # creates an empty file 
            with open(f"{self.name_time_dir}/empty.txt", 'w') as file:
                file.write("print(None)")
        except FileExistsError:
            pass
        
        
    def save_data_in_file(self) -> None:
        '''
        a function that implements
        the creation or connection to a file with stored function values.
        '''
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

                    if wr and "start_save" not in line and line != "\n":
                        line = line.replace("print(", "")
                        list_name_function.append(line[:-2])
                        
            
            data = self.output.split("\n")
            
            list_already_saved:list = self.check_replay()
            if NOT_SAVE:
                # open as append in file
                with open(self.full_directory, 'a') as file:
                    for elems in range(len(list_name_function)):
                        if list_name_function[elems] not in list_already_saved:
                            file.write(list_name_function[elems] + "::" + data[elems] + "\n")
            
            print("Successfully saved.")
            return "Successfully saved."
        except:
            print("Saving Error.")
            return "Saving Error."