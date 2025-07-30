from sqlalchemy import Column, Integer, String
from database import Base

from sqlalchemy import Column, Integer, String, DateTime

class Abrigo(Base):
    __tablename__ = "abrigo"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    endereco = Column(String)
    capacidade_total = Column(Integer)
    vagas_ocupadas = Column(Integer)
    vagas_disponiveis = Column(Integer)
    telefone = Column(String)
    data_atualizacao = Column(DateTime)
