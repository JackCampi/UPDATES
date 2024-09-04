from datetime import date
from .db_controller import run_script
import os
from sqlalchemy.orm import Session
from ..utils.message import print_message

def __get_last_backup(name: str) -> str:
    path = ""
    last_date = ""

    files = os.listdir('./data/backups')
    for file in files:
        if name in file and len(file) <= len(name) + 22:
            parts = file.split("_")
            selected_date = f'{parts[-3]}_{parts[-2]}_{parts[-1]}'
            if selected_date > last_date:
                last_date = selected_date
                path = file
                
    
    return path

def restore_table(db: Session, name: str):
    path = __get_last_backup(name)
    complete_path = f'./data/backups/{path}'
    print_message(f"RESTORING: {path}")
    run_script(db, complete_path)
    return{
        "FINITI" : True
    }

def restore_database(db: Session):
    path = __get_last_backup('mainDB')
    complete_path = f'./data/backups/{path}'
    print_message(f" RESTORING: {path} ")
    run_script(db, complete_path)
    return{
        "FINITI" : True
    }

