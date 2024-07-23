from fastapi import APIRouter, HTTPException
from ..controller.tutorial_controller import get_table_backup_codes, get_upload_folder_codes
from ..utils.message import print_message

router = APIRouter(
    prefix="/tuto"
)

@router.get("/{name}/backup")
async def read_items(name: str):
    result = get_table_backup_codes(name)
    print_message('COMANDS', "\n".join(result))
    return result

@router.get("/{name}/upload")
async def read_items(name: str):
    result = get_upload_folder_codes(name)
    print_message('COMANDS', "\n".join(result))
    return result
