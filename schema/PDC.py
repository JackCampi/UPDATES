from ..database import Base
from sqlalchemy import Column, String, Integer

class PDC(Base):
    __tablename__ = "PDC"
    pfk_per = Column(String, primary_key=True)
    fk_dpa =  Column(Integer)
    fk_ins = Column(Integer)
    cor_un = Column(String)
    
    