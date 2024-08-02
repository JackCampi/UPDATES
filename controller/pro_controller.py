import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session

from ..utils.message import print_message
from .db_controller import get_carrer_in_pes
from ..data_management.data_connector import write_tmp_file
from ..controller.enrolled_controller import check_per_in_enrolled
from .utils.pro_utils import fix_carrers

def get_csv_carrers(db: Session, bytes: bytes, year: str) -> str:
    data_str = bytes.decode('utf-8')
    per = pd.read_csv(StringIO(data_str), names= ['per'], dtype= str)

    print_message('CSV READED', per)

    pro = []
    for i in per.index:
        pes_pro = get_carrer_in_pes(db, per['per'][i])
        pro.append(pes_pro)
    new_column = pd.DataFrame({'pro' : pro})
    per = pd.concat([per, new_column], axis=1)

    per = check_per_in_enrolled(year, 'PRO', per)
    
    print_message('PRO LOADED', per)

    return write_tmp_file('PRO', per)


#TODO: deprecated now tables/equivalences/PRO
def fix_pro_column(db: Session, bytes: bytes) -> str:
    data_str = bytes.decode('utf-8')
    pro = pd.read_csv(StringIO(data_str), names= ['pro'], dtype= str)
    
    print_message('CSV READED', pro)

    pro['pro'] = fix_carrers(pro["pro"])

    print_message('PRO LOADED', pro)

    return write_tmp_file('PRO_COLUMN', pro)

