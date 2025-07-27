import pandas as pd
import panel as pn
from database import get_db_connection
from models import TIPOS_DE_ITEM, UNIDADES_DE_MEDIDA

con, engine = get_db_connection()

estoque_table_pane = pn.Column()

def get_estoque_tabulator(query_str):
    if engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return pn.widgets.Tabulator(pd.DataFrame())
    try:
        df = pd.read_sql_query(query_str, engine)
        return pn.widgets.Tabulator(df, sizing_mode='stretch_width', pagination='remote', page_size=10)
    except Exception as e:
        pn.pane.Alert(f'Erro na consulta ao banco de dados: {str(e)}', alert_type='danger')
        return pn.widgets.Tabulator(pd.DataFrame())

def update_estoque_display():
    query = "SELECT id_item_estoque, tipo_item, descricao, quantidade_atual, unidade_medida, data_ultima_movimentacao, nome_doador FROM doacoes_estoque ORDER BY id_item_estoque ASC;"
    estoque_table_pane.objects = [get_estoque_tabulator(query)]

def on_consultar_estoque(id_item_widget, filter_tipo_widget, filter_unidade_widget, filter_descricao_text_widget):
    if con is None or engine is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    item_id_val = id_item_widget.value
    filter_tipo_val = filter_tipo_widget.value
    filter_unidade_val = filter_unidade_widget.value
    filter_descricao_text_val = filter_descricao_text_widget.value.strip()

    query = "SELECT id_item_estoque, tipo_item, descricao, quantidade_atual, unidade_medida, data_ultima_movimentacao, nome_doador FROM doacoes_estoque WHERE 1=1"

    if item_id_val != 0:
        query += f" AND id_item_estoque = {item_id_val}"
    
    if filter_tipo_val and filter_tipo_val != 'Todos':
        query += f" AND tipo_item = '{filter_tipo_val}'"

    if filter_unidade_val and filter_unidade_val != 'Todas':
        query += f" AND unidade_medida = '{filter_unidade_val}'"

    if filter_descricao_text_val:
        query += f" AND descricao ILIKE '%{filter_descricao_text_val}%'"

    query += " ORDER BY id_item_estoque ASC;"

    try:
        current_tabulator = get_estoque_tabulator(query)
        if current_tabulator.value.empty and (item_id_val != 0 or filter_tipo_val != 'Todos' or filter_unidade_val != 'Todas' or filter_descricao_text_val):
            pn.pane.Alert(f'Nenhum item encontrado com os critérios de filtro.', alert_type='info')
        estoque_table_pane.objects = [current_tabulator]

    except Exception as e:
        pn.pane.Alert(f'Não foi possível consultar: {str(e)}', alert_type='danger')
        update_estoque_display()

def on_inserir_item(tipo_item_widget, descricao_widget, quantidade_atual_widget, unidade_medida_widget, nome_doador_widget):
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    if not tipo_item_widget.value or quantidade_atual_widget.value < 0 or not unidade_medida_widget.value:
        pn.pane.Alert('Erro: Campos "Tipo de Item", "Quantidade Atual" e "Unidade de Medida" são obrigatórios e a quantidade não pode ser negativa.', alert_type='warning')
        return

    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO doacoes_estoque (tipo_item, descricao, quantidade_atual, unidade_medida, nome_doador) VALUES (%s, %s, %s, %s, %s);",
            (tipo_item_widget.value, descricao_widget.value, quantidade_atual_widget.value, unidade_medida_widget.value, nome_doador_widget.value)
        )
        con.commit()
        pn.pane.Alert('Item inserido com sucesso! ID gerado automaticamente pelo banco.', alert_type='success')
        descricao_widget.value = ''
        quantidade_atual_widget.value = 0
        tipo_item_widget.value = TIPOS_DE_ITEM[1]
        unidade_medida_widget.value = UNIDADES_DE_MEDIDA[1]
        nome_doador_widget.value = ''
        update_estoque_display()
    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível inserir o item: {str(e)}', alert_type='danger')
    finally:
        if cursor:
            cursor.close()

def on_atualizar_item(id_item_widget, tipo_item_widget, descricao_widget, quantidade_atual_widget, unidade_medida_widget, nome_doador_widget):
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    if id_item_widget.value == 0:
        pn.pane.Alert('Erro: Informe o ID do Item para atualizar.', alert_type='warning')
        return
    
    if quantidade_atual_widget.value < 0:
        pn.pane.Alert('Erro: A quantidade atual não pode ser negativa.', alert_type='warning')
        return

    if not tipo_item_widget.value or not unidade_medida_widget.value:
        pn.pane.Alert('Erro: Campos "Tipo de Item" e "Unidade de Medida" são obrigatórios para atualização.', alert_type='warning')
        return

    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute(
            """
            UPDATE doacoes_estoque
            SET tipo_item = %s, descricao = %s, quantidade_atual = %s, unidade_medida = %s, data_ultima_movimentacao = CURRENT_TIMESTAMP, nome_doador = %s
            WHERE id_item_estoque = %s;
            """,
            (tipo_item_widget.value, descricao_widget.value, quantidade_atual_widget.value, unidade_medida_widget.value, nome_doador_widget.value, id_item_widget.value)
        )
        if cursor.rowcount == 0:
            pn.pane.Alert(f'Nenhum item encontrado com o ID: {id_item_widget.value} para atualizar.', alert_type='info')
        else:
            con.commit()
            pn.pane.Alert('Item atualizado com sucesso!', alert_type='success')
        update_estoque_display()
    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível atualizar o item: {str(e)}', alert_type='danger')
    finally:
        if cursor:
            cursor.close()

def on_excluir_item(id_item_widget):
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    if id_item_widget.value == 0:
        pn.pane.Alert('Erro: Informe o ID do Item para excluir.', alert_type='warning')
        return

    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute(
            "DELETE FROM doacoes_estoque WHERE id_item_estoque = %s;",
            (id_item_widget.value,)
        )
        if cursor.rowcount == 0:
            pn.pane.Alert(f'Nenhum item encontrado com o ID: {id_item_widget.value} para excluir.', alert_type='info')
        else:
            con.commit()
            pn.pane.Alert('Item excluído com sucesso!', alert_type='success')
            id_item_widget.value = 0
        update_estoque_display()
    except Exception as e:
        if con:
            con.rollback()
        pn.pane.Alert(f'Não foi possível excluir o item: {str(e)}', alert_type='danger')
    finally:
        if cursor:
            cursor.close()

def on_resetar_estoque():
    if con is None:
        pn.pane.Alert('Erro: Conexão com o banco de dados não estabelecida.', alert_type='danger')
        return

    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute("TRUNCATE TABLE doacoes_estoque RESTART IDENTITY CASCADE;")
        con.commit()
        pn.pane.Alert('Estoque resetado com sucesso! Todos os dados foram apagados e IDs reiniciados.', alert_type='success')
        update_estoque_display()
    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao resetar estoque: {e}")
        pn.pane.Alert(f'Não foi possível resetar o estoque: {str(e)}', alert_type='danger')
    finally:
        if cursor:
            cursor.close()