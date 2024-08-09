import pandas as pd
from ..model.table import Table
from ..model.insert_conf import InsertConf
from sqlalchemy.orm import Session
from ..data_management.tables_columns import get_table
from ..data_management.data_connector import read_csv, build_try_sql_path, write_pes_errors
from .db_controller import exists_in_pdc
from .utils.inserter_utils import build_statement
from ..utils.message import print_message


def run_pdc_inserter(name: str, insert: InsertConf, db: Session) -> str:
    table = get_table(name)
    csv = read_csv(table, insert)
    out = __build_inserts(table, insert, csv, db)
    return out

def __build_inserts(table: Table, insert: InsertConf, seq: pd.DataFrame, db: Session):
    file_path = build_try_sql_path(insert, table.name)
    file = open(file_path, "w", encoding="utf-8")
    
    PDC_ERRORS = set()

    for i in seq.index:
        if 'pfk_pdc' in table.column_names:
            k_per = 'pfk_pdc'
        elif 'fk_pdc' in table.column_names:
            k_per = 'fk_pdc'
        elif 'pfk_per' in table.column_names:
            k_per = 'pfk_per'
        else:
            k_per = 'fk_per'
        per = seq[k_per][i]
        if not exists_in_pdc(db, per):
            PDC_ERRORS.add(per)
        
        row = seq.iloc[[i]]   
        statement = build_statement(table, insert, row)
        file.write(statement)
    
    file.close()
    print_message('PDC INSERTER', f'FINITI: {table.name}')
    write_pes_errors(PDC_ERRORS, insert, table.name)
    return file_path