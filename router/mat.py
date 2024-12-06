from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..model.insert_conf import InsertConf, decode_InsertConf
from ..database import get_db
from ..controller.mat_controller import process_pes_mate_homogate

router = APIRouter(
    prefix="/MAT"
)

@router.post("/homo/{inserturl}")
async def run_in_pes(inserturl: str, file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return process_pes_mate_homogate(db, contents, decode_InsertConf(inserturl))
