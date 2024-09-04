from ..database import Base
from sqlalchemy import Column, String, Integer

class PRO(Base):
    __tablename__ = "PRO"
    pk_id = Column(Integer, primary_key=True)
    fk_niv = Column(Integer)
    fk_acr = Column(Integer)
    nom = Column(String)
    tit_pro = Column(String)
    SNIES = Column(Integer)