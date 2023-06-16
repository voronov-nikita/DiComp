# Решнение с использованием декораторов для упрощения использования
# Пускай теперь сам программист будет определять какую часть кода
# ему необходимо "ускорить", путем отправки файла дальше

import inspect

count_tasks = 0

def save_to_file(func):
    def wrapper(*args, **kwargs):
        global count_tasks
        # Получение исходного кода функции
        source_code = inspect.getsource(func)

        # Запись исходного кода в файл
        with open(f"task{count_tasks}.txt", "w") as file:
            file.write(source_code[14:])
        
        # Запись всех передаваемых данных для функции
        with open(f"value{count_tasks}", "w") as file:
            for elem in args:
                file.write(elem)
                file.write("\n")

        count_tasks+=1

        # Вызов функции
        result = func(*args, **kwargs)
        print(count_tasks)
        return result

    return wrapper
