from prettytable import PrettyTable

from .decorators import confirm_action, handle_db_errors, log_time
from .utils import load_metadata, load_table_data, save_table_data

DB_META_FILE = "db_meta.json"

@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    
    all_columns = ["ID:int"] + columns
    
    valid_types = ["int", "str", "bool"]
    for col in all_columns:
        col_name, col_type = col.split(":")
        if col_type not in valid_types:
            raise ValueError
    
    metadata[table_name] = all_columns
    print(f'Таблица "{table_name}" успешно создана '
          f'со столбцами: {", ".join(all_columns)}')
    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise KeyError(table_name)
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

@handle_db_errors
def list_tables():
    meta = load_metadata(DB_META_FILE)
    if not meta:
        raise KeyError("таблиц")
    else:
        for table_name in meta:
            print(f"- {table_name}")

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise KeyError(table_name)
    
    table_data = load_table_data(table_name)
    
    columns = metadata[table_name][1:]
    if len(values) != len(columns):
        raise ValueError 
    
    new_id = len(table_data) + 1
    record = {"ID": new_id}
    
    for i, col in enumerate(columns):
        col_name, col_type = col.split(":")
        value = values[i]
        if col_type == "int":
            value = int(value)
        elif col_type == "bool":
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                raise ValueError
        
        record[col_name] = value
    
    table_data.append(record)
    save_table_data(table_name, table_data)
    
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return metadata


@handle_db_errors
@log_time
def select(table_name, where_clause=None):
    table_data = load_table_data(table_name)
    
    if not table_data:
        raise FileNotFoundError
    
    if where_clause:
        table_data = [
            record for record in table_data
            if all(str(record.get(col)) == str(val)
                   for col, val in where_clause.items())
        ]
    
    if table_data:
        pt = PrettyTable()
        pt.field_names = list(table_data[0].keys())
        for record in table_data:
            pt.add_row(list(record.values()))
        print(pt)
    else:
        raise ValueError

@handle_db_errors
def update(table_name, set_clause, where_clause):
    table_data = load_table_data(table_name)
    updated = False
    for record in table_data:
        match = True
        for col, val in where_clause.items():
            record_val = str(record.get(col, "")).strip()
            condition_val = str(val).strip()
            if record_val != condition_val:
                match = False
                break
        if match:
            for set_col, new_val in set_clause.items():
                record[set_col] = new_val
            updated = True
    
    if updated:
        save_table_data(table_name, table_data)
        print("Запись успешно обновлена")
    else:
        raise ValueError

@handle_db_errors
@confirm_action("удаление записей")
def delete(table_name, where_clause):
    table_data = load_table_data(table_name)
    
    new_data = []
    deleted_count = 0
    
    for record in table_data:
        match = True
        for col, val in where_clause.items():
            if str(record.get(col)) != str(val):
                match = False
                break
        
        if not match:
            new_data.append(record)
        else:
            deleted_count += 1
    
    if deleted_count > 0:
        save_table_data(table_name, new_data)
        print(f"Удалено записей: {deleted_count}")
    else:
        raise ValueError
        
@handle_db_errors
def info(table_name):
    meta = load_metadata(DB_META_FILE)
    if not meta or table_name not in meta:  
        raise KeyError(table_name)
    
    table_data = load_table_data(table_name)
    columns = meta[table_name]
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(columns)}")
    print(f"Количество записей: {len(table_data)}")
    