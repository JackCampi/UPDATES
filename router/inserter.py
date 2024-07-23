from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controller.enrolled_controller import run_enrolled_checker
from ..model.insert_conf import InsertConf
from ..controller.inserter_controller import run_inserter
from ..controller.pes_inserter_controller import run_pes_inserter, run_complete_pes_inserter
from ..controller.pdc_inserter_controller import run_pdc_inserter
from ..database import get_db

router = APIRouter(
    prefix="/inserter"
)

@router.post("/{name}")
async def run_insert(name: str, insert: InsertConf):
    path = run_inserter(name, insert)
    return{
        "FINITI" : True,
        "TABLE" : name,
        "PATH" : path
    }

@router.post("/pes_check/{name}")
async def run_in_pes(name: str, check_pro: bool, insert: InsertConf, db: Session = Depends(get_db)):
    path = run_pes_inserter(name, insert, db, check_pro)
    return{
        "FINITI" : True,
        "TABLE" : name,
        "PATH" : path
    }

@router.post("/enrolled/{name}")
async def run_in_enrolled(name: str, insert: InsertConf, db: Session = Depends(get_db)):
    path = run_enrolled_checker(name, insert, db)
    return{
        "FINITI" : True,
        "TABLE" : name,
        "PATH" : path
    }

@router.post("/PES/{name}")
async def run_pes_insert(name: str, check_carrer: bool, insert: InsertConf, db: Session = Depends(get_db)):
    path = run_complete_pes_inserter(name, insert, check_carrer, db)
    return{
        "FINITI" : True,
        "TABLE" : name,
        "PATH" : path
    }

@router.post("/pdc_check/{name}")
async def run_in_pdc(name: str, insert: InsertConf, db: Session = Depends(get_db)):
    path = run_pdc_inserter(name, insert, db)
    return{
        "FINITI" : True,
        "TABLE" : name,
        "PATH" : path
    }