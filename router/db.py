from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controller.db_controller import get_PER, exists_in_pes, get_carrer_in_pes, insert_per, run_script
from ..database import get_db
from ..schema.PER import PER
from ..model.insert_conf import InsertConf
from ..data_management.data_connector import build_try_sql_path

router = APIRouter(
    prefix="/db"
)

@router.get("/PER")
async def read_items(db: Session = Depends(get_db)):
    return get_PER(db)

@router.get("/PES")
async def read_pes(per: str, pro: str, db: Session = Depends(get_db)):
    return exists_in_pes(db, per, pro)

@router.get("/PES/carrer")
async def read_pes(per: str, db: Session = Depends(get_db)):
    return get_carrer_in_pes(db, per)

@router.post("/PER")
def insert_in_per(per: str, name: str, db: Session = Depends(get_db)):
    return insert_per(db, PER(
        pk_pid = per,
        pid_type = "CC",
        nombres = name,
        apellidos = "test"
    ))

@router.post("/test/{name}")
def test_script(name: str, insert: InsertConf, db: Session = Depends(get_db)):
    path = build_try_sql_path(insert, name)
    return run_script(db, path)