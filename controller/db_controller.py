from sqlalchemy.orm import Session
from sqlalchemy import text
from ..schema.PER import PER
from ..schema.PES import PES
from ..schema.PDC import PDC
from ..schema.QPR import QPR

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

def run_script(db: Session, path: str):
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
                except:
                    print('Ops')
                    print(sql_command)

                # Finally, clear command string
                finally:
                    sql_command = ''
    sql_file.close()
    

def exists_in_pdc(db: Session, per: str) -> bool:
    return not(db.query(PDC).filter(PDC.pfk_per == per).first() == None)

def exists_in_qpr(db: Session, qpr: int) -> bool:
    return not(db.query(QPR).filter(QPR.pk_id == qpr).first() == None)