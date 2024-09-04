from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..controller.report_controller import report

from ..model.insert_conf import InsertConf

router = APIRouter(
    prefix="/report"
)

@router.post("/{name}")
async def gen_report(name: str, insert: InsertConf, db: Session = Depends(get_db)):

    return report(name, insert, db)