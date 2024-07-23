import pandas as pd
from ..model.insert_conf import InsertConf
from ..data_management.data_connector import read_csv
from ..data_management.tables_columns import get_table
from .db_controller import insert_per
from sqlalchemy.orm import Session
from ..schema.PER import PER
from ..utils.message import print_message

def insert_tmp_per(insert: InsertConf, name: str, db: Session):
    table = get_table('PER')
    table.name = name
    per = read_csv(table, insert, True, 'PER')

    bad_list = []
    good_list = []
    
    for i in per.index:
        obj = PER(
            pk_pid = per['pk_pid'][i],
            pid_type = per['pid_type'][i],
            nombres = per['nombres'][i],
            apellidos = per['apellidos'][i]
        )
        res = insert_per(db, obj)
        if res == -1:
            bad_list.append(str(per["pk_pid"][i]))
        else:
            good_list.append(str(per["pk_pid"][i]))
        
    print_message('GOOD PER INSERTMENT', "\n".join(good_list))
    print_message('BAD PER INSERTMENT', "\n".join(bad_list))
