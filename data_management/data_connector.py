import pandas as pd
from ..model.table import Table
from ..model.insert_conf import InsertConf
from ..utils.message import print_message

def __build_in_folder_path(insert: InsertConf, name: str, posfix: str) -> str:
    semester = insert.semester
    if semester != "":
        semester = f'_{semester}'
    folder = insert.folder
    if folder == "":
        folder = name
    seq = ""
    if posfix == 'TRY.sql':
        seq = f'{insert.seq}_'
    path = f'./data/tables/{folder}/{insert.year}/{seq}{name}_{insert.year}{semester}_{posfix}'
    return path

def __build_data_csv_path(insert: InsertConf, name: str) -> str:
    return __build_in_folder_path(insert, name, 'DATA.csv')

def build_tmp_csv_path(insert: InsertConf, name: str, posfix: str = "") -> str:
    semester = insert.semester
    if semester != "":
        semester = f'_{semester}'
    if posfix != "":
        posfix = f".{posfix}"
    path = f'./data/tmp/{name}_{insert.year}{semester}_ERRORS{posfix}.csv.tmp'
    return path

def read_csv(table: Table, insert: InsertConf, temporal: bool = False, posfix = "") -> pd.DataFrame:
    if temporal:
        path = build_tmp_csv_path(insert, table.name, posfix)
    else:
        path = __build_data_csv_path(insert, table.name)
    csv = pd.read_csv(path, header=None, sep=";", names=table.column_names, encoding='utf8')
    print_message('CSV READED', csv)
    return csv

def build_try_sql_path(insert: InsertConf, name: str) -> str:
    return __build_in_folder_path(insert, name, 'TRY.sql')

def build_not_found_report_path(insert: InsertConf, name: str) -> str:
    return __build_in_folder_path(insert, name, 'NOT_FOUND.xlsx')

def write_pes_errors(err: set, insert: InsertConf, name: str):
    
    path = build_tmp_csv_path(insert, name)
    file = open(path, "w", encoding="utf-8")
    for key in err:
        file.write(f'{key}\n')
    file.close()

def __build_notfound_csv_path(insert: InsertConf, name: str) -> str:
    return build_tmp_csv_path(insert, name, '.NOTFOUND')

def write_not_found(err: set, insert: InsertConf, name: str):
    path = __build_notfound_csv_path(insert, name)
    file = open(path, "w", encoding="utf-8")
    for key in err:
        file.write(f'{key}\n')
    file.close()

def write_tmp_file(name: str, data: pd.DataFrame) -> str:
    path = f'./data/tmp/{name}.csv.tmp'
    data.to_csv(path, ';', index=False)
    return path

def read_equiv_table(name: str) -> pd.DataFrame:
    csv = pd.read_csv(f'./data/equivalences/{name}.csv', header=None, sep=";", names=['old', 'new'], encoding='utf8', dtype=str)
    print_message('CSV READED', csv)
    return csv

def read_not_found(insert: InsertConf, name: str) -> pd.DataFrame:
    path = __build_notfound_csv_path(insert, name)
    csv = pd.read_csv(path, sep=";", names=['DOCUMENTO', 'COD_PROGRAMA'], dtype=str)
    print_message("NOTFOUND READED", message=csv)
    return csv