# Arquivo: CRUD - Agendamento de Consultta/crud_operations.py

import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import get_db_connection, engine
from models import Base, PessoaAbrigada, Servico, Consulta
import datetime

# Garante que as tabelas sejam criadas (se não existirem)
# Isso é útil para quando você roda o script pela primeira vez
# ou em um banco de dados vazio. Já fizemos manualmente, mas é bom ter.
if engine:
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
else:
    print("Engine do SQLAlchemy não está disponível. Conexão com o banco falhou.")
    Session = None

def get_all_pessoas_abrigadas():
    if Session:
        session = Session()
        try:
            pessoas = session.query(PessoaAbrigada).all()
            return pd.DataFrame([p.__dict__ for p in pessoas]).drop(columns=['_sa_instance_state'], errors='ignore')
        except Exception as e:
            print(f"Erro ao buscar pessoas abrigadas: {e}")
            return pd.DataFrame()
        finally:
            session.close()
    return pd.DataFrame()

def get_all_servicos():
    if Session:
        session = Session()
        try:
            servicos = session.query(Servico).all()
            return pd.DataFrame([s.__dict__ for s in servicos]).drop(columns=['_sa_instance_state'], errors='ignore')
        except Exception as e:
            print(f"Erro ao buscar serviços: {e}")
            return pd.DataFrame()
        finally:
            session.close()
    return pd.DataFrame()

def get_all_consultas():
    if Session:
        session = Session()
        try:
            # Carrega todas as consultas e faz o join com as tabelas relacionadas
            consultas_data = session.query(
                Consulta.id_consulta,
                PessoaAbrigada.nome.label('nome_pessoa_abrigada'),
                Servico.nome.label('nome_servico'),
                Consulta.data_agendamento,
                Consulta.horario_agendamento,
                Consulta.profissional,
                Consulta.status_agendamento,
                Consulta.observacoes,
                Consulta.data_criacao
            ).join(PessoaAbrigada).join(Servico).all()

            df = pd.DataFrame(consultas_data, columns=[
                'ID Consulta', 'Pessoa Abrigada', 'Serviço', 'Data Agendamento',
                'Horário Agendamento', 'Profissional', 'Status', 'Observações', 'Data Criação'
            ])
            return df
        except Exception as e:
            print(f"Erro ao buscar consultas: {e}")
            return pd.DataFrame()
        finally:
            session.close()
    return pd.DataFrame()

def add_consulta(id_pessoa_abrigada, id_servico, data_agendamento, horario_agendamento, profissional, observacoes=None):
    if Session:
        session = Session()
        try:
            # Converte data e hora para os tipos corretos
            data_agendamento_dt = datetime.datetime.strptime(data_agendamento, '%Y-%m-%d').date()
            horario_agendamento_time = datetime.datetime.strptime(horario_agendamento, '%H:%M').time()

            nova_consulta = Consulta(
                id_pessoa_abrigada=id_pessoa_abrigada,
                id_servico=id_servico,
                data_agendamento=data_agendamento_dt,
                horario_agendamento=horario_agendamento_time,
                profissional=profissional,
                observacoes=observacoes,
                data_criacao=datetime.datetime.now()
            )
            session.add(nova_consulta)
            session.commit()
            print(f"Consulta adicionada com sucesso! ID: {nova_consulta.id_consulta}")
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao adicionar consulta: {e}")
            return False
        finally:
            session.close()
    return False

def update_consulta(id_consulta, **kwargs):
    if Session:
        session = Session()
        try:
            consulta = session.query(Consulta).filter_by(id_consulta=id_consulta).first()
            if not consulta:
                print(f"Consulta com ID {id_consulta} não encontrada.")
                return False

            for key, value in kwargs.items():
                if key == 'data_agendamento' and value:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                elif key == 'horario_agendamento' and value:
                    value = datetime.datetime.strptime(value, '%H:%M').time()
                setattr(consulta, key, value)

            session.commit()
            print(f"Consulta com ID {id_consulta} atualizada com sucesso!")
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar consulta: {e}")
            return False
        finally:
            session.close()
    return False

def delete_consulta(id_consulta):
    if Session:
        session = Session()
        try:
            consulta = session.query(Consulta).filter_by(id_consulta=id_consulta).first()
            if not consulta:
                print(f"Consulta com ID {id_consulta} não encontrada.")
                return False
            session.delete(consulta)
            session.commit()
            print(f"Consulta com ID {id_consulta} deletada com sucesso!")
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar consulta: {e}")
            return False
        finally:
            session.close()
    return False

# Função para testar a conexão e a recuperação de dados
def test_db_connection_and_data():
    con, engine = get_db_connection()
    if con and engine:
        print("\nTeste de Conexão e Dados:")
        print("Conexão com banco de dados bem-sucedida.")

        print("\nPessoas Abrigadas:")
        df_pessoas = get_all_pessoas_abrigadas()
        print(df_pessoas.head())

        print("\nServiços:")
        df_servicos = get_all_servicos()
        print(df_servicos.head())

        print("\nConsultas:")
        df_consultas = get_all_consultas()
        print(df_consultas.head())

        con.close()
    else:
        print("Falha na conexão com o banco de dados. Verifique suas credenciais no .env e se o PostgreSQL está rodando.")

if __name__ == '__main__':
    test_db_connection_and_data()