from pydantic import BaseModel
from ..utils.message import print_debug

class InsertConf(BaseModel):
    folder: str = ""
    year: str
    semester: str = ""
    write_columns : bool = False
    seq: str



def decode_InsertConf(coded: str) -> InsertConf:
    '''
    PES_MATE$21$1$0$0

    '''
    
    parts = coded.split('$')
    print_debug(parts[3])
    print_debug(bool(parts[3]))
    return InsertConf(
        folder=parts[0],
        year=parts[1],
        semester=parts[2],
        write_columns= bool(parts[3]),
        seq=parts[4]
        )
