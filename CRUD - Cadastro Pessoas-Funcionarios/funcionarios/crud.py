from models import Funcionario
from database import SessionLocal

def criar_funcionario(data):
    session = SessionLocal()
    funcionario = Funcionario(**data)
    session.add(funcionario)
    session.commit()
    session.close()

def listar_funcionarios():
    session = SessionLocal()
    funcionarios = session.query(Funcionario).all()
    session.close()
    return funcionarios

def atualizar_funcionario(id, novos_dados):
    session = SessionLocal()
    funcionario = session.query(Funcionario).get(id)
    for chave, valor in novos_dados.items():
        setattr(funcionario, chave, valor)
    session.commit()
    session.close()

def deletar_funcionario(id):
    session = SessionLocal()
    funcionario = session.query(Funcionario).get(id)
    session.delete(funcionario)
    session.commit()
    session.close()
