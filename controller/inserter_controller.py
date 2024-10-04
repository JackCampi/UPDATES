import pandas as pd
from ..model.table import Table
from ..model.insert_conf import InsertConf
from ..data_management.data_connector import read_csv, build_try_sql_path
from ..data_management.tables_columns import get_table
from ..utils.message import print_message
from .utils.inserter_utils import build_statement


def run_inserter(name: str, insert: InsertConf, temporal: bool = False, posfix: str = "") -> str:
    if temporal:
        table = get_table(posfix)
        table.name = name
    else:
        table = get_table(name)
    csv = read_csv(table, insert, temporal, posfix)
    
    if temporal: 
        table.name = posfix
        if insert.folder == '' :
            insert.folder = name
    out = __build_inserts(table, insert, csv)
    return out



def __build_inserts(table: Table, insert: InsertConf, seq: pd.DataFrame) -> str:
    file_path = build_try_sql_path(insert, table.name)
    file = open(file_path, "w", encoding="utf-8")
    
    for i in seq.index:
        
        statement = build_statement(table, insert, seq.iloc[[i]])
        file.write(statement)
    file.close()
    print_message('INSERTER', f'FINITI: {table.name}')
    return file_path
