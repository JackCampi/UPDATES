from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..controller.pro_controller import get_csv_carrers

router = APIRouter(
    prefix="/PRO"
)

@router.post("/get_carrers")
async def run_in_pes(year: str, file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return get_csv_carrers(db, contents, year)
