import json
import os


def load_metadata(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_table_data(table_name):
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)