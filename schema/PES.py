from ..database import Base
from sqlalchemy import Column, String, Integer

class PES(Base):
    __tablename__ = "PES"
    
    pfk_per = Column(String, primary_key=True)
    pfk_pro = Column(Integer, primary_key=True)
    fk_pac = Column(Integer)
    fk_ins = Column(Integer)
    fk_noi = Column(Integer)
    fk_ace = Column(Integer)
    fk_sac = Column(Integer)
    edad = Column(Integer)
    correo = Column(String)