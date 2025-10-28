from prettytable import PrettyTable

from .utils import load_metadata, load_table_data, save_table_data

DB_META_FILE = "db_meta.json"

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    
    all_columns = ["ID:int"] + columns
    
    valid_types = ["int", "str", "bool"]
    for col in all_columns:
        col_name, col_type = col.split(":")
        if col_type not in valid_types:
            print(f'Ошибка: Некорректный тип "{col_type}" в столбце "{col_name}".')
            return metadata
    
    metadata[table_name] = all_columns
    print(f'Таблица "{table_name}" успешно создана '
          f'со столбцами: {", ".join(all_columns)}')
    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables():
    meta = load_metadata(DB_META_FILE)
    if not meta:
        print("Нет таблиц")
    else:
        for table_name in meta:
            print(f"- {table_name}")
#3
def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    
    table_data = load_table_data(table_name)
    
    columns = metadata[table_name][1:]
    if len(values) != len(columns):
        print(f'Ожидается {len(columns)} значений, получено {len(values)}')
        return metadata
    
    new_id = len(table_data) + 1
    record = {"ID": new_id}
    
    for i, col in enumerate(columns):
        col_name, col_type = col.split(":")
        value = values[i]
        if col_type == "int":
            try:
                value = int(value)
            except ValueError:
                print(f'Ошибка: Значение "{value}" не может быть преобразовано в int')
                return metadata
        elif col_type == "bool":
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                print(f'Ошибка: Значение "{value}" не может быть преобразовано в bool')
                return metadata
        
        record[col_name] = value
    
    table_data.append(record)
    save_table_data(table_name, table_data)
    
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return metadata

def select(table_name, where_clause=None):
    table_data = load_table_data(table_name)
    
    if not table_data:
        print("Таблица пуста")
        return
    
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
        print("Нет данных, соответствующих условию")

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
        print("Записи для обновления не найдены")


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
        print("Записи для удаления не найдены")
        

def info(table_name):
    meta = load_metadata(DB_META_FILE)
    if table_name not in meta:
        print(f"Таблица {table_name} не существует")
        return
    
    table_data = load_table_data(table_name)
    columns = meta[table_name]
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(columns)}")
    print(f"Количество записей: {len(table_data)}")
    