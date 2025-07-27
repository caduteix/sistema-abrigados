from models import PessoaAbrigada
from database import SessionLocal

def criar_pessoa(data):
    session = SessionLocal()
    pessoa = PessoaAbrigada(**data)
    session.add(pessoa)
    session.commit()
    session.close()

def listar_pessoas():
    session = SessionLocal()
    pessoas = session.query(PessoaAbrigada).all()
    session.close()
    return pessoas

def atualizar_pessoa(id, novos_dados):
    session = SessionLocal()
    pessoa = session.query(PessoaAbrigada).get(id)
    for chave, valor in novos_dados.items():
        setattr(pessoa, chave, valor)
    session.commit()
    session.close()

def deletar_pessoa(id):
    session = SessionLocal()
    pessoa = session.query(PessoaAbrigada).get(id)
    session.delete(pessoa)
    session.commit()
    session.close()
