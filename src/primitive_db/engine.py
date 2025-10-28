import shlex

import prompt

from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .utils import load_metadata, save_metadata

DB_META_FILE = "db_meta.json"

def print_help():
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <таблица> values (<значения>) - создать запись")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> select from <таблица> [where условие] - прочитать записи")
    print("<command> update <таблица> set <столбец>=<значение> where <условие> -" 
          "обновить запись")
    print("<command> delete from <таблица> where <условие> - удалить запись")
    print("<command> info <таблица> - информация о таблице")
    print("<command> create_table <таблица> <столбцы> - создать таблицу")
    print("<command> list_tables - список таблиц")
    print("<command> drop_table <таблица> - удалить таблицу")
    print("<command> exit - выход")
    print("<command> help - справка\n")

def parse_where(condition_str):
    if "=" in condition_str:
        parts = condition_str.split("=", 1)
        col = parts[0].strip()
        val = parts[1].strip().strip('"\'')
        return {col: val}
    return None

def parse_set(condition_str):
    return parse_where(condition_str)

def run():
    print_help()
    
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
                print("Ошибка: Недостаточно аргументов")
                continue
            meta = load_metadata(DB_META_FILE)
            meta = create_table(meta, args[1], args[2:])
            save_metadata(DB_META_FILE, meta)
        elif command == "drop_table":
            if len(args) < 2:
                print("Ошибка: Недостаточно аргументов")
                continue
            meta = load_metadata(DB_META_FILE)
            meta = drop_table(meta, args[1])
            save_metadata(DB_META_FILE, meta)

        elif command == "insert":
            if len(args) >= 4 and args[1] == "into" and args[3] == "values":
                table_name = args[2]
                values_str = " ".join(args[4:])
                if values_str.startswith("(") and values_str.endswith(")"):
                    values_str = values_str[1:-1]
                values = [v.strip('",\'') for v in shlex.split(values_str)]
                meta = load_metadata(DB_META_FILE)
                meta = insert(meta, table_name, values)
                save_metadata(DB_META_FILE, meta)
            else:
                print("Формат: insert into <таблица> values (<значения>)")
        elif command == "select":
            if len(args) >= 3 and args[1] == "from":
                table_name = args[2]
                where_clause = None
                if len(args) > 4 and args[3] == "where":
                    where_str = " ".join(args[4:])
                    where_clause = parse_where(where_str)
                select(table_name, where_clause)
            else:
                print("Формат: select from <таблица> [where условие]")
       
        elif command == "update":
            if len(args) >= 6 and args[2] == "set" and "where" in args:
                table_name = args[1]
                set_index = args.index("set")
                where_index = args.index("where")
                
                set_str = " ".join(args[set_index+1:where_index])
                where_str = " ".join(args[where_index+1:]) 
                
                set_clause = parse_set(set_str)
                where_clause = parse_where(where_str)
                
                if set_clause and where_clause:
                    update(table_name, set_clause, where_clause)
            else:
                print("Формат: update <таблица> set <столбец>=<значение> " 
                      "where <условие>")

        elif command == "delete":
            if len(args) >= 5 and args[1] == "from" and args[3] == "where":
                table_name = args[2]  # users
                where_str = " ".join(args[4:])
                where_clause = parse_where(where_str)
                if where_clause:
                    delete(table_name, where_clause)
            else:
                print("Формат: delete from <таблица> where <условие>")
        elif command == "info":
            if len(args) >= 2:
                info(args[1])
            else:
                print("Формат: info <таблица>")
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
