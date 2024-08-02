from pydantic import BaseModel
from typing import List

class TableKeyList(BaseModel):
    keys: List[str]