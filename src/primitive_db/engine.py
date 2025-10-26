#новое
import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def welcome():
    print("Первая попытка запустить проект!\n\n***")
    
    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        command = prompt.string("Введите команду: ")
        if command == "help":
            continue
        elif command == "exit":
            break
        else:
            print("Неизвестная команда")
# новое
DB_META_FILE = "db_meta.json"

def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("Первая попытка запустить проект!")
    
    while True:
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        
        if not args:
            continue
            
        command = args[0]
        
        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "list_tables":
            list_tables()
        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Недостаточно аргументов для create_table")
                continue
            meta = load_metadata(DB_META_FILE)
            meta = create_table(meta, args[1], args[2:])
            save_metadata(DB_META_FILE, meta)
        elif command == "drop_table":
            if len(args) < 2:
                print("Ошибка: Недостаточно аргументов для drop_table")
                continue
            meta = load_metadata(DB_META_FILE)
            meta = drop_table(meta, args[1])
            save_metadata(DB_META_FILE, meta)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")