from models import PessoaAbrigada, Funcionario
from database import SessionLocal

# Pessoa Abrigada
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

# Funcionario
def criar_funcionario(data):
    session = SessionLocal()
    func = Funcionario(**data)
    session.add(func)
    session.commit()
    session.close()

def listar_funcionarios():
    session = SessionLocal()
    funcionarios = session.query(Funcionario).all()
    session.close()
    return funcionarios

def atualizar_funcionario(id, novos_dados):
    session = SessionLocal()
    func = session.query(Funcionario).get(id)
    for chave, valor in novos_dados.items():
        setattr(func, chave, valor)
    session.commit()
    session.close()

def deletar_funcionario(id):
    session = SessionLocal()
    func = session.query(Funcionario).get(id)
    session.delete(func)
    session.commit()
    session.close()
