import pandas as pd
import panel as pn
from datetime import datetime, date
from database import get_db_connection
from agendamentos.models import STATUS_AGENDAMENTO

con, engine = get_db_connection()

agendamentos_table_pane = pn.Column()


def get_pessoas_abrigadas_para_select():
    """Busca o ID e Nome das pessoas abrigadas para popular um pn.widgets.Select."""
    if engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return [("Selecione a Pessoa", 0)] # Valor padrão
    try:
        df = pd.read_sql_query("SELECT id_pessoa_abrigada, nome FROM pessoas_abrigadas ORDER BY nome ASC;", engine)
        # Retorna uma lista de tuplas (nome, id)
        return [("Selecione a Pessoa", 0)] + list(df[['nome', 'id_pessoa_abrigada']].itertuples(index=False, name=None))
    except Exception as e:
        pn.pane.Alert(f'Erro ao carregar pessoas abrigadas: {str(e)}', alert_type='danger')
        return [("Selecione a Pessoa", 0)]

def get_servicos_para_select():
    """Busca o ID e Nome dos serviços para popular um pn.widgets.Select."""
    if engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return [("Selecione o Serviço", 0)] # Valor padrão
    try:
        df = pd.read_sql_query("SELECT id_servico, nome FROM servicos ORDER BY nome ASC;", engine)
        # Retorna uma lista de tuplas (nome, id)
        return [("Selecione o Serviço", 0)] + list(df[['nome', 'id_servico']].itertuples(index=False, name=None))
    except Exception as e:
        pn.pane.Alert(f'Erro ao carregar serviços: {str(e)}', alert_type='danger')
        return [("Selecione o Serviço", 0)]


# --- Funções CRUD para Agendamentos ---

def get_agendamentos_tabulator(query_str):
    """Executa uma query SQL e retorna um pn.widgets.Tabulator com os resultados."""
    if engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return pn.widgets.Tabulator(pd.DataFrame())
    try:
        # Busca dados e faz join para mostrar nomes ao invés de IDs
        df = pd.read_sql_query(query_str, engine)
        
        
        
        return pn.widgets.Tabulator(df, sizing_mode='stretch_width', pagination='remote', page_size=10, disabled=True) 
    except Exception as e:
        pn.pane.Alert(f'Erro na consulta ao banco de dados: {str(e)}', alert_type='danger')
        print(f"Erro na consulta: {e}") # Para depuração no console
        return pn.widgets.Tabulator(pd.DataFrame())

def update_agendamentos_display():
    """Atualiza o painel da tabela de agendamentos com os dados mais recentes."""
    query = """
    SELECT
        c.id_consulta,
        pa.nome AS nome_pessoa_abrigada,
        s.nome AS nome_servico,
        c.data_agendamento,
        c.horario_agendamento,
        c.profissional,
        c.status_agendamento,
        c.observacoes,
        c.data_criacao
    FROM
        consultas c
    JOIN
        pessoas_abrigadas pa ON c.id_pessoa_abrigada = pa.id_pessoa_abrigada
    JOIN
        servicos s ON c.id_servico = s.id_servico
    ORDER BY
        c.data_agendamento DESC, c.horario_agendamento DESC;
    """
    agendamentos_table_pane.objects = [get_agendamentos_tabulator(query)]


def on_agendar_consulta(id_pessoa_abrigada_widget, id_servico_widget, data_agendamento_widget,
                        horario_agendamento_widget, profissional_widget, observacoes_widget):
    """Função para inserir um novo agendamento de consulta no banco de dados."""
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    # Validação de campos obrigatórios
    if (id_pessoa_abrigada_widget.value == 0 or id_servico_widget.value == 0 or
            not data_agendamento_widget.value or not horario_agendamento_widget.value or
            not profissional_widget.value):
        pn.pane.Alert('Erro: Preencha todos os campos obrigatórios (Pessoa Abrigada, Serviço, Data, Horário, Profissional).', alert_type='warning')
        return

    # Validação de data/hora não retroativa
    agendamento_datetime_str = f"{data_agendamento_widget.value} {horario_agendamento_widget.value}"
    agendamento_datetime = datetime.strptime(agendamento_datetime_str, '%Y-%m-%d %H:%M:%S')

    # Convertendo a data e hora atual para o fuso horário correto (se aplicável) ou comparando como UTC/local se for o caso do DB
    # Para simplicidade, vamos comparar diretamente com o datetime.now() que estará no fuso do servidor
    if agendamento_datetime < datetime.now():
        pn.pane.Alert('Erro: A data e hora do agendamento não podem ser retroativas.', alert_type='warning')
        return

    cursor = None
    try:
        cursor = con.cursor()
        
        # 1. Verificar disponibilidade de horário para o profissional
        check_query = """
        SELECT COUNT(*) FROM consultas
        WHERE profissional = %s AND data_agendamento = %s AND horario_agendamento = %s;
        """
        cursor.execute(check_query, (profissional_widget.value, data_agendamento_widget.value, horario_agendamento_widget.value))
        count = cursor.fetchone()[0]

        if count > 0:
            pn.pane.Alert('Erro: O profissional já possui um agendamento neste horário.', alert_type='warning')
            return

        # 2. Inserir o novo agendamento
        cursor.execute(
            """
            INSERT INTO consultas (id_pessoa_abrigada, id_servico, data_agendamento, horario_agendamento, profissional, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (id_pessoa_abrigada_widget.value, id_servico_widget.value,
             data_agendamento_widget.value, horario_agendamento_widget.value,
             profissional_widget.value, observacoes_widget.value)
        )
        con.commit()
        pn.pane.Alert('Agendamento inserido com sucesso!', alert_type='success')
        
        # Limpar os campos do formulário após o sucesso
        id_pessoa_abrigada_widget.value = 0 # Volta para "Selecione a Pessoa"
        id_servico_widget.value = 0 # Volta para "Selecione o Serviço"
        data_agendamento_widget.value = None
        horario_agendamento_widget.value = None
        profissional_widget.value = ''
        observacoes_widget.value = ''

        # Atualiza a exibição da tabela de agendamentos
        update_agendamentos_display()

    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível agendar a consulta: {str(e)}', alert_type='danger')
        print(f"Erro ao agendar: {e}") # Para depuração
    finally:
        if cursor:
            cursor.close()

def on_consultar_agendamento(id_consulta_widget, filter_pessoa_widget, filter_servico_widget, filter_status_widget, filter_data_inicio_widget, filter_data_fim_widget):
    """Função para consultar agendamentos com filtros."""
    if con is None or engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    consulta_id_val = id_consulta_widget.value
    filter_pessoa_val = filter_pessoa_widget.value
    filter_servico_val = filter_servico_widget.value
    filter_status_val = filter_status_widget.value
    filter_data_inicio_val = filter_data_inicio_widget.value
    filter_data_fim_val = filter_data_fim_widget.value

    # Base da query com JOINs para pegar nomes
    query = """
    SELECT
        c.id_consulta,
        pa.nome AS nome_pessoa_abrigada,
        s.nome AS nome_servico,
        c.data_agendamento,
        c.horario_agendamento,
        c.profissional,
        c.status_agendamento,
        c.observacoes,
        c.data_criacao
    FROM
        consultas c
    JOIN
        pessoas_abrigadas pa ON c.id_pessoa_abrigada = pa.id_pessoa_abrigada
    JOIN
        servicos s ON c.id_servico = s.id_servico
    WHERE 1=1
    """

    params = []

    if consulta_id_val != 0:
        query += f" AND c.id_consulta = %s"
        params.append(consulta_id_val)
    
    if filter_pessoa_val != 0: # 0 é o valor "Selecione a Pessoa"
        query += f" AND c.id_pessoa_abrigada = %s"
        params.append(filter_pessoa_val)

    if filter_servico_val != 0: # 0 é o valor "Selecione o Serviço"
        query += f" AND c.id_servico = %s"
        params.append(filter_servico_val)

    if filter_status_val and filter_status_val != 'Todos':
        query += f" AND c.status_agendamento = %s"
        params.append(filter_status_val)

    if filter_data_inicio_val:
        query += f" AND c.data_agendamento >= %s"
        params.append(filter_data_inicio_val)

    if filter_data_fim_val:
        query += f" AND c.data_agendamento <= %s"
        params.append(filter_data_fim_val)

    query += " ORDER BY c.data_agendamento DESC, c.horario_agendamento DESC;"
    
    # Convertendo os parâmetros para string para a f-string, especialmente datas
    formatted_params = []
    for p in params:
        if isinstance(p, (date, datetime)):
            formatted_params.append(f"'{p.isoformat()}'")
        elif isinstance(p, str):
            formatted_params.append(f"'{p}'")
        else:
            formatted_params.append(str(p))

    final_query = query % tuple(formatted_params) if params else query


    try:
        current_tabulator = get_agendamentos_tabulator(final_query)
        if current_tabulator.value.empty and (consulta_id_val != 0 or filter_pessoa_val != 0 or filter_servico_val != 0 or filter_status_val != 'Todos' or filter_data_inicio_val or filter_data_fim_val):
            pn.pane.Alert(f'Nenhum agendamento encontrado com os critérios de filtro.', alert_type='info')
        agendamentos_table_pane.objects = [current_tabulator]

    except Exception as e:
        pn.pane.Alert(f'Não foi possível consultar agendamentos: {str(e)}', alert_type='danger')
        print(f"Erro ao consultar: {e}") # Para depuração
        update_agendamentos_display() # Volta para a exibição completa se der erro de filtro

def on_atualizar_agendamento(id_consulta_widget, id_pessoa_abrigada_widget, id_servico_widget,
                            data_agendamento_widget, horario_agendamento_widget, profissional_widget,
                            status_agendamento_widget, observacoes_widget):
    """Função para atualizar um agendamento existente."""
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    if id_consulta_widget.value == 0:
        pn.pane.Alert('Erro: Informe o ID do Agendamento para atualizar.', alert_type='warning')
        return
    
    # Validação de campos obrigatórios
    if (id_pessoa_abrigada_widget.value == 0 or id_servico_widget.value == 0 or
            not data_agendamento_widget.value or not horario_agendamento_widget.value or
            not profissional_widget.value or not status_agendamento_widget.value):
        pn.pane.Alert('Erro: Preencha todos os campos obrigatórios para atualização.', alert_type='warning')
        return

    # Validação de data/hora não retroativa para atualização
    agendamento_datetime_str = f"{data_agendamento_widget.value} {horario_agendamento_widget.value}"
    agendamento_datetime = datetime.strptime(agendamento_datetime_str, '%Y-%m-%d %H:%M:%S')

    if agendamento_datetime < datetime.now() and status_agendamento_widget.value == 'Agendado':
        # Permite atualizar status para "Realizado" ou "Cancelado" em datas passadas, mas não "Agendado"
        if agendamento_datetime.date() < date.today() and status_agendamento_widget.value not in ['Realizado', 'Cancelado', 'Não Compareceu']:
            pn.pane.Alert('Erro: Não é possível agendar para uma data passada ou manter status "Agendado" em data retroativa.', alert_type='warning')
            return
        elif agendamento_datetime.date() >= date.today() and agendamento_datetime < datetime.now():
             pn.pane.Alert('Erro: Não é possível agendar para um horário passado na data atual.', alert_type='warning')
             return
    
    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute(
            """
            UPDATE consultas
            SET
                id_pessoa_abrigada = %s,
                id_servico = %s,
                data_agendamento = %s,
                horario_agendamento = %s,
                profissional = %s,
                status_agendamento = %s,
                observacoes = %s
            WHERE id_consulta = %s;
            """,
            (id_pessoa_abrigada_widget.value, id_servico_widget.value,
             data_agendamento_widget.value, horario_agendamento_widget.value,
             profissional_widget.value, status_agendamento_widget.value,
             observacoes_widget.value, id_consulta_widget.value)
        )
        if cursor.rowcount == 0:
            pn.pane.Alert(f'Nenhum agendamento encontrado com o ID: {id_consulta_widget.value} para atualizar.', alert_type='info')
        else:
            con.commit()
            pn.pane.Alert('Agendamento atualizado com sucesso!', alert_type='success')
        
        # Limpar ID após atualização para evitar nova operação acidental
        id_consulta_widget.value = 0
        update_agendamentos_display()

    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível atualizar o agendamento: {str(e)}', alert_type='danger')
        print(f"Erro ao atualizar: {e}") # Para depuração
    finally:
        if cursor:
            cursor.close()

def on_excluir_agendamento(id_consulta_widget):
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    if id_consulta_widget.value == 0:
        pn.pane.Alert('Erro: Informe o ID do Agendamento para excluir.', alert_type='warning')
        return

    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute(
            "DELETE FROM consultas WHERE id_consulta = %s;",
            (id_consulta_widget.value,)
        )
        if cursor.rowcount == 0:
            pn.pane.Alert(f'Nenhum agendamento encontrado com o ID: {id_consulta_widget.value} para excluir.', alert_type='info')
        else:
            con.commit()
            pn.pane.Alert('Agendamento excluído com sucesso!', alert_type='success')
            id_consulta_widget.value = 0 # Limpa o ID após a exclusão
        update_agendamentos_display()

    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível excluir o agendamento: {str(e)}', alert_type='danger')
        print(f"Erro ao excluir: {e}") 
    finally:
        if cursor:
            cursor.close()