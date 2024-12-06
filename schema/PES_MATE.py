from ..database import Base
from sqlalchemy import Column, String, Integer

class PES_MATE(Base):
    __tablename__ = "PES_MATE"
    
    pfk_per = Column(String, primary_key=True)
    pfk_pac = Column(Integer, primary_key=True)
    pfk_pro = Column(Integer, primary_key=True)
    pfk_mat = Column(Integer, primary_key=True)
    fk_grupo = Column(String)
    fk_dpa = Column(Integer)
    fk_ins = Column(Integer)
    tipologia = Column(String)
    tipo_asignatura = Column(String)
    calificacion_cuantitativa = Column(Integer)
    calificacion_cualitativa = Column(String)
    observaciones = Column(String)