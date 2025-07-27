from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "seu_usuario"
PASSWORD = "jjdavi2005"
DB_NAME = "abrigo"
HOST = "localhost"

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
