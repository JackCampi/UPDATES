import pandas as pd
from ..model.insert_conf import InsertConf
from ..data_management.data_connector import read_csv
from ..data_management.tables_columns import get_table
from .db_controller import insert_pes
from sqlalchemy.orm import Session
from ..schema.PES import PES
from ..utils.message import print_message

def insert_tmp_pes(insert: InsertConf, name: str, db: Session):
    table = get_table('PES')
    table.name = name
    pes = read_csv(table, insert, True, 'PES')

    bad_list = []
    good_list = []
    
    for i in pes.index:
        obj = PES(
            pfk_per = pes['pfk_per'][i],
            pfk_pro = pes['pfk_pro'][i],
            fk_pac = pes['fk_pac'][i],
            fk_ins = pes['fk_ins'][i],
            fk_noi = pes['fk_noi'][i],
            fk_ace = pes['fk_ace'][i],
            fk_sac = pes['fk_sac'][i],
            edad = pes['edad'][i],
            correo = pes['correo'][i]
        )
        res = insert_pes(db, obj)
        if res == -1:
            bad_list.append(str(pes["pfk_per"][i]))
        else:
            good_list.append(str(pes["pfk_per"][i]))
    
    print_message('GOOD PES INSERTMENT', "\n".join(good_list))
    print_message('BAD PES INSERTMENT', "\n".join(bad_list))
