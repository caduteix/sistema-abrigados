from sqlalchemy import Column, Integer, String, Date
from database import Base

class PessoaAbrigada(Base):
    __tablename__ = "pessoa_abrigada"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    genero = Column(String)
    data_nascimento = Column(Date)
    documento = Column(String)
    status = Column(String)
    condicoes_saude = Column(String)
