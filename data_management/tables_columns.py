import json
from pydantic import Json
from ..model.table import Table

DATA_FILE_PATH = './data/tables.json'
COLUMNS_NAMES = "COLUMNS_NAMES"
COLUMNS_TYPES = "COLUMNS_TYPES"

def read_columns_data() -> Json:
    file = open(DATA_FILE_PATH)
    columns = json.load(file)
    file.close()
    return columns

def save_columns_data(data: Json):
    with open(DATA_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def get_table(name: str) -> Table:
    file = open(DATA_FILE_PATH)
    columns = json.load(file)
    file.close()

    if name in columns:
        return Table(
            name=name,
            column_names=columns[name][COLUMNS_NAMES],
            column_types=columns[name][COLUMNS_TYPES]
        )
    else:
        raise Exception("No table registered")