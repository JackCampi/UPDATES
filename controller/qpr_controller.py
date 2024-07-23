import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session

from ..utils.message import print_message
from .db_controller import exists_in_qpr
from ..data_management.data_connector import write_tmp_file
from ..controller.enrolled_controller import check_per_in_enrolled


def check_csv_in_qpr(db: Session, bytes: bytes) -> str:
    data_str = bytes.decode('utf-8')
    seq = pd.read_csv(StringIO(data_str), names= ['qpr'], dtype= str)

    print_message('CSV READED', seq)

    QPR = set()
    for i in seq.index:
        if not exists_in_qpr(db, seq['qpr'][i]):
            QPR.add(seq['qpr'][i])
    

    data = pd.DataFrame({'qpr' : list(QPR)})
    
    print_message('PQR CHECK', data)

    return write_tmp_file('QPR', data)