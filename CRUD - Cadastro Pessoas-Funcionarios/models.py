from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PessoaAbrigada(Base):
    __tablename__ = 'pessoa_abrigada'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nascimento = Column(Date)
    documento = Column(String, nullable=True)
    sexo = Column(String)
    condicoes_saude = Column(String)

class Funcionario(Base):
    __tablename__ = 'funcionario'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cargo = Column(String)
    contato = Column(String)

from database import engine
Base.metadata.create_all(bind=engine)