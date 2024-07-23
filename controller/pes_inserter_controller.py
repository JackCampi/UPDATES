import pandas as pd
from ..model.table import Table
from ..model.insert_conf import InsertConf
from ..data_management.data_connector import read_csv, build_try_sql_path, write_pes_errors
from ..data_management.tables_columns import get_table
from ..utils.message import print_message
from .utils.inserter_utils import build_statement
from sqlalchemy.orm import Session
from .db_controller import exists_in_pes, get_carrer_in_pes
from .enrolled_controller import run_enrolled_checker
from .inserter_controller import run_inserter
from .per_controller import insert_tmp_per
from .pes_controller import insert_tmp_pes

def run_pes_inserter(name: str, insert: InsertConf, db: Session, check_other_carrers: bool = True) -> str:
    table = get_table(name)
    csv = read_csv(table, insert)
    out = __build_inserts(table, insert, csv, db, check_other_carrers)
    return out

def __build_inserts(table: Table, insert: InsertConf, seq: pd.DataFrame, db: Session, check_other_carrers: bool) -> str:
    file_path = build_try_sql_path(insert, table.name)
    file = open(file_path, "w", encoding="utf-8")

    PES_ERRORS = set()

    for i in seq.index:

        k_per = 'pfk_per' if 'pfk_per' in table.column_names else 'fk_per'
        k_pro = 'pfk_pro' if 'pfk_pro' in table.column_names else 'fk_pro'
        per = seq[k_per][i]
        pro = str(seq[k_pro][i])
        key = f'{per};{pro}'

        if not exists_in_pes(db, per, pro):
            if check_other_carrers:
                pro = get_carrer_in_pes(db, per)
                if pro == -1:
                    PES_ERRORS.add(key)
                    continue
                else:
                    print(f'{per} was found in another career, so, changing register...')
            else:
                PES_ERRORS.add(key)
                continue
                            
        row = seq.iloc[[i]]
        row.at[i, k_pro] = int(pro)
        statement = build_statement(table, insert, row)
        file.write(statement)
    file.close()
    print_message('PES INSERTER', f'FINITI: {table.name}')
    write_pes_errors(PES_ERRORS, insert, table.name)
    return file_path

def run_complete_pes_inserter(name: str, insert: InsertConf, check_carrer: bool, db: Session):
    
    nseq = int(insert.seq) + 2

    #0. remove tmp data

    #1. we generate no-problem registers & pes errors
    insert.seq = "0"+str(+ nseq)
    run_pes_inserter(name, insert, db, check_carrer)

    #2. we check in enrolled students
    run_enrolled_checker(name, insert, db)

    #3. build PER statements

    insert.seq = "0"+str(nseq-2)
    per_path = run_inserter(name, insert, True, 'PER')

    #4. build PES statements

    insert.seq = "0"+str(nseq-1)
    pes_path = run_inserter(name, insert, True, 'PES')

    #5. insert PER

    insert_tmp_per(insert, name, db)

    #6. insert PES

    insert_tmp_pes(insert, name, db)

    #7. run again pes inserter & complete procedure

    insert.seq = "0"+str(nseq)
    final_path = run_pes_inserter(name, insert, db, check_carrer)

    return{
        "PER" : per_path,
        "PES" : pes_path,
        name : final_path
    }
