import panel as pn
import os
from dotenv import load_dotenv

from database import setup_db_connections, get_db_connection
from models import TIPOS_DE_ITEM, UNIDADES_DE_MEDIDA
from crud import (
    estoque_table_pane, update_estoque_display,
    on_consultar_estoque, on_inserir_item, on_atualizar_item,
    on_excluir_item, on_resetar_estoque
)

load_dotenv()

setup_db_connections()

pn.extension('tabulator')
pn.extension(notifications=True)

try:
    with open('styles.css', 'r') as f:
        custom_styles_content = f.read()
    pn.config.raw_css.append(custom_styles_content)
except FileNotFoundError:
    print("Erro: styles.css não encontrado. Certifique-se de que o arquivo está na mesma pasta que app.py.")
except Exception as e:
    print(f"Erro ao carregar styles.css: {e}")


id_item = pn.widgets.IntInput(
    name="ID do Item (Para Consultar, Atualizar, Excluir)",
    value=0,
    step=1,
    start=0,
    disabled=False,
    placeholder='Digite o ID do item existente'
)

tipo_item = pn.widgets.Select(
    name="Tipo de Item",
    options=TIPOS_DE_ITEM[1:],
    value=TIPOS_DE_ITEM[1],
    disabled=False
)

descricao = pn.widgets.TextAreaInput(
    name="Descrição",
    value='',
    placeholder='Detalhes do item doado',
    rows=3,
    disabled=False
)

quantidade_atual = pn.widgets.IntInput(
    name="Quantidade Atual",
    value=0,
    step=1,
    start=0,
    disabled=False
)

unidade_medida = pn.widgets.Select(
    name="Unidade de Medida",
    options=UNIDADES_DE_MEDIDA[1:],
    value=UNIDADES_DE_MEDIDA[1],
    disabled=False
)

filter_tipo_item = pn.widgets.Select(
    name="Filtrar por Tipo",
    options=TIPOS_DE_ITEM,
    value=TIPOS_DE_ITEM[0],
    disabled=False
)

filter_unidade_medida = pn.widgets.Select(
    name="Filtrar por Unidade de Medida",
    options=UNIDADES_DE_MEDIDA,
    value=UNIDADES_DE_MEDIDA[0],
    disabled=False
)

filter_descricao_text = pn.widgets.TextInput(
    name="Filtrar por Descrição (Texto Livre)",
    value='',
    placeholder='Ex: Arroz',
    disabled=False
)

buttonConsultar = pn.widgets.Button(name='Consultar Estoque', button_type='default')
buttonInserir = pn.widgets.Button(name='Inserir Item', button_type='primary')
buttonAtualizar = pn.widgets.Button(name='Atualizar Item', button_type='warning')
buttonExcluir = pn.widgets.Button(name='Excluir Item', button_type='danger')
buttonResetarEstoque = pn.widgets.Button(name='RESETAR ESTOQUE (ATENÇÃO!)', button_type='danger', button_style='outline')


buttonConsultar.on_click(lambda event: on_consultar_estoque(id_item, filter_tipo_item, filter_unidade_medida, filter_descricao_text))
buttonInserir.on_click(lambda event: on_inserir_item(tipo_item, descricao, quantidade_atual, unidade_medida))
buttonAtualizar.on_click(lambda event: on_atualizar_item(id_item, tipo_item, descricao, quantidade_atual, unidade_medida))
buttonExcluir.on_click(lambda event: on_excluir_item(id_item))
buttonResetarEstoque.on_click(lambda event: on_resetar_estoque())

insert_controls = pn.Column(
    pn.pane.Markdown("## **Informações do Item (Para Inserção):**"),
    tipo_item,
    descricao,
    quantidade_atual,
    unidade_medida,
    pn.Row(buttonInserir, sizing_mode='stretch_width', align='center'),
    css_classes=['control-panel-section']
)

query_filter_controls = pn.Column(
    pn.pane.Markdown("## **Operações por ID e Filtros:**"),
    id_item,
    pn.Row(
        filter_tipo_item,
        filter_unidade_medida,
        filter_descricao_text,
        sizing_mode='stretch_width',
        align='center'
    ),
    pn.Row(buttonConsultar, buttonAtualizar, buttonExcluir, sizing_mode='stretch_width', align='center'),
    pn.pane.Markdown("---"),
    pn.Row(buttonResetarEstoque, sizing_mode='stretch_width', align='center'),
    css_classes=['control-panel-section']
)

table_display = pn.Column(
    pn.pane.Markdown("## **Estoque Atual:**"),
    estoque_table_pane,
    sizing_mode='stretch_width',
    css_classes=['table-view-section']
)

main_layout = pn.Column(
    pn.Row(pn.pane.Markdown("# 📦 Gestão de Estoque de Doações", width=500), sizing_mode='stretch_width', align='center'),
    pn.Row(
        insert_controls,
        pn.Column(
            query_filter_controls,
            table_display,
            sizing_mode='stretch_width',
            css_classes=['table-and-query-column']
        ),
        sizing_mode='stretch_width',
        align='start',
        css_classes=['main-layout-container']
    )
)

pn.Column(main_layout, sizing_mode='stretch_width', align='center').servable()