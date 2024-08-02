from pydantic import BaseModel

class TableKey(BaseModel):
    name: str
    value: str