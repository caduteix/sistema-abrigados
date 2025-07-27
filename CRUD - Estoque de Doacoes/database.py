import os
from dotenv import load_dotenv
import psycopg2 as pg
import sqlalchemy

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

con = None
engine = None

def setup_db_connections():
    global con, engine

    try:
        con = pg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        con.autocommit = False
    except Exception as e:
        con = None

    try:
        cnx = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
        engine = sqlalchemy.create_engine(cnx)
    except Exception as e:
        engine = None

setup_db_connections()

def get_db_connection():
    return con, engine