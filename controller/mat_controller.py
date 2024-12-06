from sqlalchemy.orm import Session
from ..exception.acc_error import ACCError
from ..utils.message import print_message,print_debug
from ..data_management.tables_columns import get_table
from ..data_management.data_connector import write_tmp_file, build_try_sql_path
from ..model.insert_conf import InsertConf
import pandas as pd
import numpy as np
from io import StringIO
from ..schema.PES_MATE import PES_MATE
from .db_controller import get_pes_mate, get_mat_first_group, exist_mat_first_group, get_mat_gr_no_pac
from .utils.inserter_utils import build_statement, replace_statement

def process_pes_mate_homogate(db: Session, bytes: bytes, insert : InsertConf) -> str:

    '''
    PES_MATE columns 

    pfk_per
    pfk_pac
    pfk_pro
    pfk_mat
    fk_grupo
    fk_dpa
    fk_ins
    tipologia
    tipo_asignatura
    calificacion_cuantitativa
    calificacion_cualitativa
    observaciones
    '''

    data_str = bytes.decode('utf-8')
    col = [
        'pac',
        'per',
        'mat',
        'acc',
        'tipo',
        'grad',
        'pro'
    ]
    mat = pd.read_csv(StringIO(data_str), names= col, dtype= str, sep=';')

    print_message('CSV READED', mat)

    eng = [
        '1000044',
        '1000045',
        '1000046',
        '1000047'
    ]
    statements = []
    courses = []
    dpa = 1
    acc = ''
    grade = ''
    tipo  = 'B'

    file_path = build_try_sql_path(insert, 'PES_MATE')
    file = open(file_path, "w", encoding="utf-8")
    table = get_table('PES_MATE')


    for i in mat.index:
        dpa = 1
        #ENGLISH
        if mat['mat'][i] in ['TODOS INGLES', 'Todos Ingles']:
            acc = 'Homologación'
            dpa = 39
            courses = eng
            grade = 'AP'
            tipo  = 'E'
        elif mat['mat'][i] in ['Ingles I 1000044', 'Ingles I 1000044']:
            acc = 'Homologación'
            dpa = 39
            courses = ['1000044']
            grade = 'AP'
            tipo  = 'E'
        elif mat['mat'][i] == 'ultimo ingles':
            acc = 'Homologación'
            dpa = 39
            courses = ['1000047']
            grade = 'AP'
            tipo  = 'E'
        elif mat['mat'][i] == 'segundo ingles':
            acc = 'Homologación'
            dpa = 39
            courses = ['1000045']
            grade = 'AP'
            tipo  = 'E'

        #OTHER 
        elif mat['acc'][i] in ['HOMOLOGAR', 'Homologacion']:
            acc = 'Homologación'
            try:
                tmp = int(mat['mat'][i])
                tmp+=1

                courses = [mat['mat'][i]]
                grade = mat['grad'][i]
                tipo  = mat['tipo'][i] if not pd.isna(mat['tipo'][i]) else 'B'
            except:
                raise ACCError(f'HOMO:{mat["mat"][i]} at {i}')
        elif mat['acc'][i] in ['CONVALIDAR', 'Convalidacion']:
            acc = 'Convalidación'
            try:
                tmp = int(mat['mat'][i])
                tmp+=1

                courses = [mat['mat'][i]]
                grade = mat['grad'][i]
                tipo  = mat['tipo'][i] if not pd.isna(mat['tipo'][i]) else 'B'
            except:
                raise ACCError(f'HOMO:{mat["mat"][i]} at {i}')
        elif mat['acc'][i] in [ 'EQUIVALER' , 'Equivalencia']:
            acc = 'Equivalencia'
            try:
                tmp = int(mat['mat'][i])
                tmp+=1

                courses = [mat['mat'][i]]
                grade = mat['grad'][i]
                tipo  = mat['tipo'][i] if not pd.isna(mat['tipo'][i]) else 'B'
            except:
                raise ACCError(f'HOMO:{mat["mat"][i]} at {i}')
        elif mat['acc'][i] in ['CANCELAR', 'Cancelada']:
            acc = 'Cancelada'
            try:
                tmp = int(mat['mat'][i])
                tmp+=1

                courses = [mat['mat'][i]]
                grade = 'nan'
                tipo  = mat['tipo'][i] if not pd.isna(mat['tipo'][i]) else 'B'
            except:
                raise ACCError(f'HOMO:{mat["mat"][i]} at {i}')
        elif mat['acc'][i] in ['anula']:
            acc = 'Anulada'
            try:
                tmp = int(mat['mat'][i])
                tmp+=1

                courses = [mat['mat'][i]]
                grade = 'nan'
                tipo  = mat['tipo'][i] if not pd.isna(mat['tipo'][i]) else 'B'
            except:
                raise ACCError(f'HOMO:{mat["mat"][i]} at {i}')
        else:
            raise ACCError(f'{mat["acc"][i]} at {i}')
        
        for course in courses:
            grade = str(grade).replace(',','')
            qual, quan = __get_grade(grade)
            info = [
                    mat['per'][i],
                    mat['pac'][i],
                    mat['pro'][i],
                    course,
                    1,
                    dpa,
                    76,
                    tipo.upper(),
                    acc,
                    quan,
                    qual,
                    None
                ]

            acc_tmp = info[8]
            info = __check_dpa(info, db)
            if info[8] == 'ERROR':
                info[8] = acc_tmp
                gr_statement, dpa = __create_gr(info,insert, db)
                file.write(gr_statement)
                info[5] = dpa
            statements.append(info)
            if __must_replace(info, db):
                statement = replace_statement(table, insert,pd.DataFrame([info], columns=table.column_names))
            else:
                statement = build_statement(table, insert, pd.DataFrame([info], columns=table.column_names))
            file.write(statement)

    file.close()
    data =pd.DataFrame(statements)
    print_message( 'PES MATE HOMO', data)
    return write_tmp_file('PES_MATE_HOMO', data)

def __create_gr(info: list, insert: InsertConf, db: Session) -> tuple:
    dpa = 1
    mat_oagr = get_mat_gr_no_pac(db, info[3])
    if not mat_oagr == None:
        dpa = mat_oagr.pfk_dpa
    table = get_table('MAT_OAGR')
    gr = [[
        info[3],
        dpa,
        info[1],
        '1',
        None,
        None
    ]]

    data = pd.DataFrame(gr, columns=table.column_names)
    return build_statement(table, insert, data), dpa

def __must_replace(info: list, db: Session) ->bool:

    '''
    0. must create
    1. must replace
    2. its ok
    '''
    acc_not_included = []
    if info[8] in ['Convalidación', 'Equivalencia', 'Homologación']:
        acc_not_included = ['Cancelada' , 'Anulada', 'Cursada']
    elif info[8] == 'Cancelada':
        acc_not_included = ['Convalidación', 'Equivalencia', 'Homologación', 'Anulada', 'Cursada']
    else:
        acc_not_included = ['Convalidación', 'Equivalencia', 'Homologación', 'Cancelada', 'Cursada']
    
    pes_mate = get_pes_mate(db, info[0],info[1],info[2],info[3], acc_not_included)
    return not pes_mate == None
    
def __check_dpa(info: list, db: Session) -> list:
    if exist_mat_first_group(db, info[3], info[1], info[5], '1'):
        return info
    else:
        mat_oagr = get_mat_first_group(db, info[3], info[1])
        if mat_oagr == None:
            info[8] = 'ERROR'
            return info
        else:
            info[5] = mat_oagr.pfk_dpa
            info[4] = mat_oagr.pk_grupo
            return info
    


def __get_grade(grade) -> tuple:
    qualitative = ''
    quantitative = 0

    if grade == 'nan':
        return None, None
    elif grade in ['AP', 'ap']:
        qualitative = grade
        return qualitative, None
    else:
        qualitative = ('AP' if int(grade) >= 30 else 'NA')
        quantitative = __format_grade(grade)
        return qualitative, str(quantitative)

def __format_grade(grade: int) -> str:
    grade = str(grade)
    if len(grade) == 1:
        grade = f'0.{grade}'
    else:
        grade = f'{grade[0]}.{grade[1]}'
    return grade