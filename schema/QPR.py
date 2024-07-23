from ..database import Base
from sqlalchemy import Column, String, Integer

class QPR(Base):
    __tablename__ = "QPR"
    
    pk_id = Column(Integer, primary_key=True)
    desc = Column(String)