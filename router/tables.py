from fastapi import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session

from ..exception.equiv_error import EquivalenceError

from ..database import get_db
from ..controller.tables_controller import get_all, insert_table, table_exists, fix_column_with_equivalences, fix_table_with_equivalences, check_table_keys
from ..model.table import Table
from ..model.tables_key_list import TableKeyList

router = APIRouter(
    prefix="/tables"
)

@router.get("/")
async def read_items():
    return get_all()

@router.post("/")
async def add_table(new_table: Table):
    insert_table(new_table)
    if len(new_table.column_names) == len(new_table.column_types):
        return new_table
    else:
        return HTTPException(400, "names and types are not same lenght")
    
@router.get("/{name}")
async def check(name: str):
    table = table_exists(name)
    if table != None:
        return table
    else:
        return HTTPException(400, 'No, it does not exist')

@router.post("/equiv/{name}")
async def equiv(name: str, file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    return fix_column_with_equivalences(db, contents, name)

@router.post("/equivtable/{name}")
async def equivtables(name: str, col_name: str, file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    #TODO: remove
    """ try:
        return fix_table_with_equivalences(db, contents, name, col_name)
    except EquivalenceError as e:
        raise e """
    return fix_table_with_equivalences(db, contents, name, col_name)

@router.post("/keys/{name}")
async def equivtables(name: str, file: UploadFile, db: Session = Depends(get_db)):
    #return keys
    contents = await file.read()
    return check_table_keys(db, contents, name)