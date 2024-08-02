from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..controller.pro_controller import get_csv_carrers, fix_pro_column

router = APIRouter(
    prefix="/PRO"
)

@router.post("/get_carrers")
async def run_in_pes(year: str, file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return get_csv_carrers(db, contents, year)

@router.post("/fix_pro")
async def run_in_pes(file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return fix_pro_column(db, contents)
