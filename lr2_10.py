# Лабораторная работа №2, вариант 10
# Ограничение для поиска по автору: книги от 2018 года
# XML: словарь "Name - CharCode"

from csv import reader            # чтение csv-файла
from datetime import datetime     # текущая дата для файла с результатами поиска
import os                         # очистка экрана


# Открывает books.csv и возвращает таблицу (список строк) без заголовка
def open_table():
    try:
        # windows-1251 - кодировка файла, ; - разделитель столбцов
        with open('books.csv', 'r', encoding='windows-1251') as csvfile:
            table = list(reader(csvfile, delimiter=';'))
            table = table[1:]     # первая строка - заголовок, убираем её
            return table
    except FileNotFoundError:
        print('Файл не найден!')
        return 0


# Задание 1: считает записи, у которых название (столбец 1) длиннее 30 символов
def count_titles(table):
    flag = 0                      # счётчик подходящих записей
    for row in table:
        if len(row[1]) > 30:
            flag += 1
    print(f'Записей с названием длиннее 30 символов: {flag}')
    input('Нажмите Enter')


# Задание 2: поиск книг по автору (столбец 3) среди книг от 2018 года
def search(table):
    searchline = input('Введите автора: ')
    if searchline in ['0', '']:   # 0 или пустая строка - вернуться в меню
        return 0
    output = open('result.txt', 'w')     # результаты поиска сохраняем в файл
    output.write(f'Поиск от: {datetime.today()}\n\n')
    flag = 0                      # сколько книг найдено
    for row in table:
        # row[6] - дата поступления вида дд.мм.гггг, row[6][6:10] - это год
        if find_string(searchline, row[3]) != -1 and int(row[6][6:10]) >= 2018:
            print(row[1])         # выводим название книги
            output.write(f'{row[3]}. {row[1]} - {row[6][6:10]}\n')
            flag += 1
    if flag == 0:
        print('Ничего не найдено!')
    else:
        print(f'Найдено позиций: {flag}')
    input('Нажмите Enter')
    output.close()


# Ищет строку searchline в строке string без учёта регистра
# Возвращает номер позиции или -1, если ничего не найдено
def find_string(searchline, string):
    string = string.lower()
    index = string.find(searchline.lower())
    return index


# Задание 3: пишет в файл 20 библиографических ссылок
# Формат: <номер>. <автор>. <название> - <год>
def bibliography(table):
    output = open('bibliography.txt', 'w')
    for i in range(20):           # берём первые 20 записей из таблицы
        output.write(f'{i + 1}. {table[i][3]}. {table[i][1]} - {table[i][6][6:10]}\n')
    output.close()
    print('Список сохранён в файл bibliography.txt')
    input('Нажмите Enter')


# Задание 4: из currency.xml делает словарь "Name - CharCode"
# xml-файл читаем как обычный текст, нужные теги находим с помощью split
def xml_dict():
    with open('currency.xml', 'r', encoding='windows-1251') as file:
        text = file.read()
    result = {}                              # ключ - название валюты, значение - её код
    # делим текст на куски, в каждом куске - одна валюта (тег <Valute>)
    for part in text.split('<Valute')[1:]:   # [1:] - кусок до первой валюты не нужен
        # берём текст между <Name> и </Name>
        name = part.split('<Name>')[1].split('</Name>')[0]
        # берём текст между <CharCode> и </CharCode>
        charcode = part.split('<CharCode>')[1].split('</CharCode>')[0]
        result[name] = charcode
    print(result)
    input('Нажмите Enter')


# Главное меню, работает, пока не выбран пункт 0
while True:
    os.system('cls')              # очищаем экран
    if open_table() == 0:         # если books.csv не найден - выходим
        break
    print('Меню:\n1 - Названия длиннее 30 символов\n2 - Поиск по автору\n3 - Библиографические ссылки\n4 - Словарь Name - CharCode\n0 - Выход')
    menu = input('Выберите пункт меню: ')
    match menu:
        case '1':
            count_titles(open_table())
        case '2':
            search(open_table())
        case '3':
            bibliography(open_table())
        case '4':
            xml_dict()
        case '0':
            break
        case _:
            print('Нет пункта меню, нажмите Enter')
            input()
