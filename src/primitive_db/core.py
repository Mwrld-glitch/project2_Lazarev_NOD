from .utils import load_metadata

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