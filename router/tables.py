from fastapi import APIRouter, HTTPException
from ..controller.tables_controller import get_all, insert_table, table_exists
from ..model.table import Table

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