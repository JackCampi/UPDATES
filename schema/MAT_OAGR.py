from ..database import Base
from sqlalchemy import Column, String, Integer

class MAT_OAGR(Base):
    __tablename__ = "MAT_OAGR"

    pfk_mat = Column(Integer, primary_key=True)
    pfk_dpa = Column(Integer, primary_key=True)
    pfk_pac = Column(Integer, primary_key=True)
    pk_grupo = Column(String, primary_key=True)
    cupo = Column(Integer)
    inscritos = Column(Integer)