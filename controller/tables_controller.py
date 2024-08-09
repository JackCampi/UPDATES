from ..exception.equiv_error import EquivalenceError
from ..data_management.tables_columns import read_columns_data, save_columns_data
from ..model.table import Table
from ..model.tables_key_list import TableKeyList
from ..model.table_key import TableKey
from pydantic import Json
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO
from ..utils.message import print_message
from ..data_management.data_connector import write_tmp_file, read_equiv_table
from .db_controller import exists_key_in_table, get_changable_keys_in_table


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

def __get_code(pro: pd.DataFrame,old: str):
    return  pro.loc[pro['old'].str.contains(old)]

#TODO: maybe it'll work better with dics 
def __fix_column(column : pd.Series, name: str) -> list:
    pro = read_equiv_table(name)
    new_column = []
    for i in column.index:
        old = column.iloc[i] if not pd.isna(column.iloc[i]) else "NOPE"
        old = old.strip()
        search = __get_code(pro, str(old))
        if search.empty:
            raise EquivalenceError(name, old)
        new_column.append(search['new'][search.index[0]])
    return new_column
    
#TODO: db unused
def fix_column_with_equivalences(db: Session, bytes: bytes, name: str) -> str:
    data_str = bytes.decode('utf-8')
    column = pd.read_csv(StringIO(data_str), names= [name], dtype= str, sep=";")
    
    print_message('CSV READED', column)

    column[name] = __fix_column(column[name], name)

    print_message(f'{name} EQUIVALENCE LOADED', column)

    return write_tmp_file(f'{name}_COLUMN', column)

def fix_table_with_equivalences(db: Session, bytes: bytes, name: str, column_name: str) -> str:
    data_str = bytes.decode('utf-8')
    table = pd.read_csv(StringIO(data_str), dtype= str, sep=";")
    
    print_message('CSV READED', table)

    table[column_name] = __fix_column(table[column_name], name)

    print_message(f'{name} EQUIVALENCE LOADED', table)

    return write_tmp_file(f'{name}_COLUMN', table)

def check_table_keys(db: Session, bytes: bytes, name: str) -> str:
    data_str = bytes.decode('utf-8')
    table = pd.read_csv(StringIO(data_str), dtype= str, sep=";")
    print_message('CSV READED', table)

    check_column = []
    changes_column = []

    for index in table.index:
        keys = []
        for key in table.columns:
            keys.append(
                TableKey(name=key if not "ch_" in key else key[3:], value=table[key][index])
            )
        exists = exists_key_in_table(db, keys, name)
        check_column.append(exists)

        if not exists:
            keys = []
            for key in table.columns:
                if not "ch_" in key:
                    keys.append(
                        TableKey(name=key if not "ch_" in key else key[3:], value=table[key][index])
                    )
            changes_column.append(get_changable_keys_in_table(db, keys, name))
        
        else:
            changes_column.append("")
            

    table['check'] = check_column
    table['changes'] = changes_column
    print_message(f'{name} KEYS LOADED', table)

    return write_tmp_file(f'{name}_KEYS', table)
    