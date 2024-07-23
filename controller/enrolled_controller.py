import pandas as pd

from ..data_management.data_connector import build_tmp_csv_path, read_csv, write_not_found
from ..data_management.enrolled import load_enrolled
from ..model.insert_conf import InsertConf
from ..model.table import Table
from ..utils.message import print_message
from sqlalchemy.orm import Session
from .db_controller import get_carrer_in_pes

def run_enrolled_checker(name: str, insert: InsertConf, db: Session) -> str:
    table = Table(
        name=name, 
        column_names=['per', 'pro'], 
        column_types=['str', 'str'])
    csv = read_csv(table, insert, True)
    out = __build_files(table, insert, csv, db)
    return out

def __getFilter(pes, per, pro):
    print(per)
    doc_filter = pes.loc[pes['DOCUMENTO'].str.contains(per)]
    #doc_filter['COD_PLAN']=doc_filter['COD_PLAN'].values.astype(str)
    pro_filter = doc_filter.loc[doc_filter['COD_PLAN'].str.contains(pro)]

    return pro_filter

def __format_period(period: str)-> str:
    year, semester = period.split('-')
    semester = semester[:1]
    return f'{year}0{semester}'

def __get_age(date: str, year: str) -> str:
    birth = date.split('/')[0]
    return str(int(year) - int(birth))


def __build_PES(row: pd.DataFrame, pro : str) -> str:
    i = row.index[0]
    statement = f"{row['DOCUMENTO'][i]};{pro};"
    period = __format_period(row['PERIODO'][i])
    #79 corresponds to unal Bogota
    statement += f"{period};76;{row['COD_NODO_INICIO'][i]};"
    sac = row['COD_SUBACCESO'][i]
    #little assert for postgrade double degree
    statement += f"{row['COD_ACCESO'][i]};{sac if sac != '25' else 36};"
    age = __get_age(row['FECHA_NACIMIENTO'][i], period[:4])
    statement += f"{age};{row['CORREO'][i]}\n"

    return statement

def __get_doc_type(typo: str) -> str:
    if typo == 'C': return 'CC'
    elif typo == 'T': return 'TI'
    elif typo == 'P': return 'PS'
    elif typo == 'E': return 'CE'
    else: return 'OT'

def __build_PER(row: pd.DataFrame) -> str:
    i = row.index[0]
    statement = f"{row['DOCUMENTO'][i]};"
    typo = __get_doc_type(row['T_DOCUMENTO'][i])
    statement += f"{typo};{row['NOMBRES'][i]};"
    lastname = str(row['APELLIDO1'][i]) + str(row['APELLIDO2'][i])
    statement  += f'{lastname}\n'

    return statement


def __build_files(table: Table, insert: InsertConf, seq: pd.DataFrame, db: Session):
    pes_path = build_tmp_csv_path(insert, table.name, 'PES')
    per_path = build_tmp_csv_path(insert, table.name, 'PER')
    pes_file = open(pes_path, "w", encoding="utf-8")
    per_file = open(per_path, "w", encoding="utf-8")

    enrolled = load_enrolled(insert.year)
    
    PES_NOT_FOUND = set()

    for i in seq.index:

        per = str(seq['per'][i])
        pro = str(seq['pro'][i])
        filter = __getFilter(enrolled, per, pro)

        if filter.empty:
            pro = get_carrer_in_pes(db, per)
            if pro == -1:
                PES_NOT_FOUND.add(f'{per};{seq["pro"][i]}')
            continue
        
        pes = __build_PES(enrolled.iloc[[filter.index[0]]], pro)
        per = __build_PER(enrolled.iloc[[filter.index[0]]])

        pes_file.write(pes)
        per_file.write(per)

    pes_file.close()
    per_file.close()
    write_not_found(PES_NOT_FOUND, insert, table.name)
    print_message('ENROLLED CHECKER', f'FINITI: {table.name}')
    return {
        "PES" : pes_path,
        "PER" : per_path
    }

def check_per_in_enrolled(year: str, name: str, per: pd.DataFrame) -> pd.DataFrame:

    insert = InsertConf(year=str(year), seq="1")

    pes_path = build_tmp_csv_path(insert, name, 'PES')
    per_path = build_tmp_csv_path(insert, name, 'PER')
    pes_file = open(pes_path, "w", encoding="utf-8")
    per_file = open(per_path, "w", encoding="utf-8")

    enrolled = load_enrolled(year)
    for i in per.index:
        per_at_i = per['per'][i]
        pro_at_i = per['pro'][i]
        if pro_at_i == -1:
            filter = enrolled.loc[enrolled['DOCUMENTO'].str.contains(per_at_i)]
            if not filter.empty:
                pro = int(filter['COD_PLAN'][filter.index[0]])
                per.at[i, 'pro'] = pro

                pes = __build_PES(enrolled.iloc[[filter.index[0]]], pro)
                per_statement = __build_PER(enrolled.iloc[[filter.index[0]]])

                pes_file.write(pes)
                per_file.write(per_statement)
    
    pes_file.close()
    per_file.close()
    return per

        