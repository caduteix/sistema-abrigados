# Arquivo: CRUD - Agendamento de Consultta/test_connection.py

from database import get_db_connection
import pandas as pd

print("Iniciando teste de conexão...")
con, engine = get_db_connection()

if con and engine:
    print("Conexão bem-sucedida com o banco de dados!")
    print(f"Host: {engine.url.host}, Database: {engine.url.database}, User: {engine.url.username}")

    try:
        # Testando se as tabelas existem e têm dados
        df_pessoas = pd.read_sql_query("SELECT COUNT(*) FROM pessoas_abrigadas;", engine)
        print(f"Tabela 'pessoas_abrigadas' tem {df_pessoas.iloc[0,0]} registros.")

        df_servicos = pd.read_sql_query("SELECT COUNT(*) FROM servicos;", engine)
        print(f"Tabela 'servicos' tem {df_servicos.iloc[0,0]} registros.")

        df_consultas = pd.read_sql_query("SELECT COUNT(*) FROM consultas;", engine)
        print(f"Tabela 'consultas' tem {df_consultas.iloc[0,0]} registros.")

    except Exception as e:
        print(f"Erro ao verificar tabelas: {e}")
        print("Certifique-se de que o script SQL foi executado corretamente no banco de dados 'agendamentos_db'.")
    finally:
        # Feche a conexão temporária se precisar (mas o get_db_connection gerencia a global)
        pass

else:
    print("Falha na conexão com o banco de dados.")
    print("Verifique:")
    print("1. Se o PostgreSQL está rodando.")
    print("2. As informações de DB_HOST, DB_NAME, DB_USER, DB_PASS no seu arquivo .env.")
    print("3. Se o arquivo .env está na mesma pasta que database.py e test_connection.py.")

print("Teste de conexão concluído.")