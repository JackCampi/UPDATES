from pydantic import BaseModel

class InsertConf(BaseModel):
    folder: str = ""
    year: str
    semester: str = ""
    write_columns : bool = False
    seq: str
