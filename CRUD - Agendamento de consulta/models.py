# Arquivo: CRUD - Agendamento de Consultta/models.py

from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PessoaAbrigada(Base):
    __tablename__ = 'pessoas_abrigadas'
    id_pessoa_abrigada = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    data_nascimento = Column(Date)
    documento = Column(String(50))
    sexo = Column(String(20))
    data_entrada = Column(Date)

    consultas = relationship("Consulta", back_populates="pessoa_abrigada")

    def __repr__(self):
        return f"<PessoaAbrigada(id={self.id_pessoa_abrigada}, nome='{self.nome}')>"

class Servico(Base):
    __tablename__ = 'servicos'
    id_servico = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False, unique=True)
    descricao = Column(Text)
    responsavel = Column(Text)

    consultas = relationship("Consulta", back_populates="servico")

    def __repr__(self):
        return f"<Servico(id={self.id_servico}, nome='{self.nome}')>"

class Consulta(Base):
    __tablename__ = 'consultas'
    id_consulta = Column(Integer, primary_key=True)
    id_pessoa_abrigada = Column(Integer, ForeignKey('pessoas_abrigadas.id_pessoa_abrigada'), nullable=False)
    id_servico = Column(Integer, ForeignKey('servicos.id_servico'), nullable=False)
    data_agendamento = Column(Date, nullable=False)
    horario_agendamento = Column(Time, nullable=False)
    profissional = Column(Text, nullable=False)
    status_agendamento = Column(String(50), nullable=False, default='Agendado')
    observacoes = Column(Text)
    data_criacao = Column(DateTime) # TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    pessoa_abrigada = relationship("PessoaAbrigada", back_populates="consultas")
    servico = relationship("Servico", back_populates="consultas")

    def __repr__(self):
        return f"<Consulta(id={self.id_consulta}, pessoa={self.id_pessoa_abrigada}, servico={self.id_servico})>"