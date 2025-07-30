from sqlalchemy.orm import Session
from models import Abrigo
from datetime import datetime

def get_abrigos(db: Session):
    return db.query(Abrigo).all()

def get_abrigo_by_id(db: Session, abrigo_id: int):
    return db.query(Abrigo).filter(Abrigo.id == abrigo_id).first()

def atualizar_vagas_ocupadas(db: Session, abrigo_id: int, vagas_ocupadas: int):
    abrigo = get_abrigo_by_id(db, abrigo_id)
    if not abrigo:
        return False, "Abrigo não encontrado."
    if vagas_ocupadas > abrigo.capacidade_total:
        return False, "Vagas ocupadas não podem exceder a capacidade total."
    
    abrigo.vagas_ocupadas = vagas_ocupadas
    abrigo.vagas_disponiveis = abrigo.capacidade_total - vagas_ocupadas
    abrigo.data_atualizacao = datetime.utcnow()
    db.commit()
    return True, "Vagas atualizadas com sucesso."
