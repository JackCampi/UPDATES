from fastapi import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..controller.enrolled_controller import search_pbm

router = APIRouter(
    prefix="/enrolled"
)


@router.post("/PBM/{year}")
async def search_for_pbm(file: UploadFile, year: int, db: Session = Depends(get_db)):
    contents = await file.read()
    return search_pbm(contents, year)