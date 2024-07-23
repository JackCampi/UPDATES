from ..database import Base
from sqlalchemy import Column, String

class PER(Base):
    __tablename__ = "PER"
    pk_pid = Column(String, primary_key=True)
    pid_type =  Column(String)
    nombres = Column(String)
    apellidos = Column(String)