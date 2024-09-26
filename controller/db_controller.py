from sqlalchemy.orm import Session
from sqlalchemy import text
from ..schema.PER import PER
from ..schema.PES import PES
from ..schema.PDC import PDC
from ..schema.QPR import QPR
from ..schema.PRO import PRO
from ..utils.message import print_message

from ..model.table_key import TableKey

def get_PER(db: Session):
    return db.query(PER).all()

def exists_in_pes(db: Session, per: str, pro: str):
    return not(db.query(PES).filter(PES.pfk_per == per, PES.pfk_pro == pro).first() == None)

def get_carrer_in_pes(db: Session, per: str) -> int:
    result = db.query(PES).filter(PES.pfk_per == per).first()
    if result == None:
        return -1
    else:
        return result.pfk_pro
    
def insert_per(db: Session, per: PER):
    
    check = db.query(PER).filter(PER.pk_pid == per.pk_pid).first()
    if check:
        return -1
    
    db.add(per)
    db.commit()
    db.refresh(per)
    return per

def insert_pes(db: Session, pes: PES):
    
    check = db.query(PES).filter(PES.pfk_per == pes.pfk_per, PES.pfk_pro == pes.pfk_pro).first()
    if check:
        return -1
    
    db.add(pes)
    db.commit()
    db.refresh(pes)
    return pes

def run_command(db: Session, line: str):
    result = db.execute(text(line))
    return str(result.first())

def run_script(db: Session, path: str):
    #error log
    err = []

    # Open the .sql file
    sql_file = open(path,'r', encoding="utf-8")

    # Create an empty command string
    sql_command = ''

    # Iterate over all lines in the sql file
    for line in sql_file:
        # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):
            # Append line to the command string
            sql_command += line.strip('\n')

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statement and commit it
                try:
                    db.execute(text(sql_command))
                    db.commit()

                # Assert in case of error
                except Exception as e:
                    msg = f'comand: {sql_command} \n err: {e}'
                    print_message("OPS" , msg)
                    err.append(sql_command)

                # Finally, clear command string
                finally:
                    sql_command = ''
    sql_file.close()
    return {
        "FINITI": True,
        "ERR" : len(err),
        "LOG": err
    }
    

def exists_in_pdc(db: Session, per: str) -> bool:
    return not(db.query(PDC).filter(PDC.pfk_per == per).first() == None)

def exists_in_qpr(db: Session, qpr: int) -> bool:
    return not(db.query(QPR).filter(QPR.pk_id == qpr).first() == None)

def exists_key_in_table(db: Session, keys : list[TableKey], name: str) -> bool :
    conditions = [f'{x.name} = "{x.value}"' for x in keys]
    query = f'select * from {name} where {" and ".join(conditions)}'
    result = db.execute(text(query))
    return not(result.first() == None)

def get_changable_keys_in_table(db: Session, keys : list[TableKey], name: str):
    conditions = [f'{x.name} = "{x.value}"' for x in keys]
    query = f'select * from {name} where {" and ".join(conditions)}'
    result = db.execute(text(query))
    return str(result.first())

def get_pro_name(db: Session, pro: str) -> str:
    return db.query(PRO).filter(PRO.pk_id == pro).first().nom