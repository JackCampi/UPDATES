from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..controller.restore_controller import restore_table, restore_database
from ..database import get_db

router = APIRouter(
    prefix="/restore"
)

@router.get("/DB")
async def read_items(db: Session = Depends(get_db)):
    restore_database(db)

@router.get("/{name}")
async def read_items(name: str, db: Session = Depends(get_db)):
    restore_table(db, name)



