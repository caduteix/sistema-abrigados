from sqlalchemy.orm import Session
from models import PessoaAbrigada
from datetime import date

# CREATE
def create_abrigado(db: Session, nome, genero, data_nascimento, documento, status, condicoes_saude):
    novo = PessoaAbrigada(
        nome=nome,
        genero=genero,
        data_nascimento=data_nascimento,
        documento=documento,
        status=status,
        condicoes_saude=condicoes_saude
    )
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise e

# READ
def read_abrigados(db: Session):
    return db.query(PessoaAbrigada).all()

# FILTER
def filter_abrigados(db: Session, nome=None, status=None, genero=None):
    query = db.query(PessoaAbrigada)
    if nome:
        query = query.filter(PessoaAbrigada.nome.ilike(f"%{nome}%"))
    if status:
        query = query.filter(PessoaAbrigada.status == status)
    if genero:
        query = query.filter(PessoaAbrigada.genero == genero)
    return query.all()

# UPDATE
ddef update_abrigado(db: Session, id: int, novos_dados: dict):
    abrigado = db.query(PessoaAbrigada).filter(PessoaAbrigada.id == id).first()
    if not abrigado:
        return None
    for campo, valor in novos_dados.items():
        setattr(abrigado, campo, valor)
    try:
        db.commit()
        db.refresh(abrigado)
        return abrigado
    except Exception as e:
        db.rollback()
        raise e

# DELETE
def delete_abrigado(db: Session, id: int):
    abrigado = db.query(PessoaAbrigada).filter(PessoaAbrigada.id == id).first()
    if not abrigado:
        return False
    db.delete(abrigado)
    db.commit()
    return True
