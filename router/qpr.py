from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..controller.qpr_controller import check_csv_in_qpr

router = APIRouter(
    prefix="/QPR"
)

@router.post("/check")
async def run_in_pes(file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return check_csv_in_qpr(db, contents)