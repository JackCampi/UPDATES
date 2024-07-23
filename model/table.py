from pydantic import BaseModel
from typing import List

class Table(BaseModel):
    name: str
    column_names: List[str]
    column_types: List[str] 