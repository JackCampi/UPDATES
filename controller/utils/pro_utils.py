import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session

from ...utils.message import print_message, print_debug
from ..db_controller import get_carrer_in_pes

def __read_carrear_codes() -> pd.DataFrame:
    csv = pd.read_csv('./data/equivalences/PRO.csv', header=None, sep=";", names=['old', 'new'], encoding='utf8', dtype=str)
    print_message('CSV READED', csv)
    return csv

def __get_code(pro: pd.DataFrame,old: str):
    return  pro.loc[pro['old'].str.contains(old)]

#TODO: optimize
#TODO: chango for tables/equivalences/PRO
def fix_carrers(column : pd.Series) -> list:
    pro = __read_carrear_codes()
    print_debug(column)
    new_column = []
    for i in column.index:
        search = __get_code(pro, column.iloc[i])
        if search.empty:
            raise Exception(f"No career registered: {column.iloc[i]}")
        new_column.append(search['new'][search.index[0]])
    return new_column