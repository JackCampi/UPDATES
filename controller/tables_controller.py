from ..data_management.tables_columns import read_columns_data, save_columns_data
from ..model.table import Table
from pydantic import Json

def get_all():
    return read_columns_data()

def insert_table(table: Table):
    all = get_all()
    all[table.name] = {
        "COLUMNS_NAMES" : table.column_names,
        "COLUMNS_TYPES" : table.column_types
    }
    save_columns_data(all)

def table_exists(name: str) -> Json:
    all = get_all()
    if name in all:
        return all[name]
    else:
        None