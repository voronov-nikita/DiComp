# **Индивидуальный проект** 
### Метод распределения вычислений



![image](doc/thrid.png)



<br>

## **Content**
1. [About](/README.md#about)
2. [Description](/README.md#description)
3. [Useful Links](README.md#useful-links)
4. [More information](/README.md#more-information)
5. [Keywords](/README.md#keywords)


## **About**



## **Description**

Основной код описан в двух файлах в папке [scr](scr/). Код серверной части описан в файле [server.py](scr/server.py), а код клиентской части описан в файле [dicomp.py](scr/dicomp.py).

Для нормальной работы рекомендую прочитать документацию к проекту: [Documentation](doc/Documentation.md)



## **Useful Links**
1. python - [python.org](https://python.org)
   
2. pypi - [pypi.org](https://pypi.org/)
   
3. Курс "Параллельные и распределенные вычисления" - [youtube.com](https://youtube.com/playlist?list=PLJOzdkh8T5krFksX90QkuntWC6vflDZZU)
    > Материал представлен на русском языке от канала [Компьютерные науки](https://www.youtube.com/@user-th3jq9rw7b). Лекции читает О.В.Сухолов. Курс отпределен как куср-[ШАД](https://academy.yandex.ru/dataschool) - Школа Анализа Данных от кампании [Яндекс](https://ru.wikipedia.org/wiki/%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81). ВНИМАНИЕ! В курсе представлены решения на Java, рекомендуется знать его.

4. Что такое распределение вычислений - [ru.wikipedia.org](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)
   
5. 



## **More Information**

Реализация _**метода распределения вычислений**_ обычно выполняется на быстрых и _стандартных_ языках программирования, такие как Java или C/C++. Однако, на данный момент, изучение нового языка программирования немного нецелесообразно, в связи с этим, реализация будет на более понятном и изученном мной языке - Python. Python так же поддерживает многопоточность, что важно для реализации метода.

При раюоте были использованы библиотеки python:

1. threading -> для многопоточности сервера;
2. os -> для удаления временных файлов программы;
3. inspect -> для получения исходного кода декорируемой функции;
4. socket -> для обьединения серверной и клиентской частей;
5. subprocess -> для выполнения полученного кода и получения данных из терминала.

<br>

***23.06.2023*** - первый масштабный прогресс! 

Теперь вычислени происходят. 

Я заметил, что присутсвует какой-то странный вывод от сервера, позже я заметил ту деталь, которую мог незаметить только слепой: моя функция не вызывается!?! поэтому выводилась пустота, теперь осталось самая малость, сделать так, чтобы можно было один раз отправить полный файл, теперь это более понятно как сделать, только объеденить две функции у клиента.

<br>

**05.08.2023** - исправлены многие ошибки, такие как:
1. Ошибка с вычислением маленьких чисел
2. Ошибка с возвращением ошибок
3. Ошибка с вызовом функции несколько раз;

Код на сервере теперь работает куда быстрее за счет возможности использования *Pypy*; 

Сервер теперь многопоточен, что позволит одновременно вычислять несколько задач;



## **Keywords**
1. **Flow (Поток)** - наименьшая единица обработки, исполнение которой может быть назначено ядром операционной системы.
2. **Process (Процесс)** - это выполняющаяся программа. Один или несколько потоков выполняются в контексте процесса.
3. **Cluster (Кластер)** -  группа компьютеров, объединённых высокоскоростными каналами связи, представляющая с точки зрения пользователя единый аппаратный ресурс.
4. **Parallel computing (Параллельные вычисления)** - способ организации компьютерных вычислений, при котором программы разрабатываются как набор взаимодействующих вычислительных процессов, работающих параллельно (одновременно).

<br>


###### 13.08.2023 - last global change.

![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
