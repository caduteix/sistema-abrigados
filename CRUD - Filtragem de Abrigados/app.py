import panel as pn
import datetime
from crud import (
    create_abrigado, read_abrigados, delete_abrigado,
    update_abrigado, filter_abrigados
)
from database import SessionLocal

pn.extension()

db = SessionLocal()

form_nome = pn.widgets.TextInput(name="Nome")
form_genero = pn.widgets.Select(name="Genero", options=["Masculino", "Feminino", "Outro"])
form_data_nascimento = pn.widgets.DatePicker(name="Data de Nascimento", value=datetime.date.today())
form_documento = pn.widgets.TextInput(name="Documento")
form_status = pn.widgets.Select(name="Status", options=["abrigado", "saiu", "encaminhado"])
form_condicoes = pn.widgets.TextAreaInput(name="Condicoes de saude")

form_id = pn.widgets.IntInput(name="ID do abrigado (para editar/excluir)")

# Tabela
tabela = pn.pane.DataFrame(read_abrigados(db), width=900, height=300)

def cadastrar(event):
    create_abrigado(
        db,
        form_nome.value,
        form_genero.value,
        form_data_nascimento.value,
        form_documento.value,
        form_status.value,
        form_condicoes.value
    )
    tabela.object = read_abrigados(db)

def atualizar(event):
    novos_dados = {
        "nome": form_nome.value,
        "genero": form_genero.value,
        "data_nascimento": form_data_nascimento.value,
        "documento": form_documento.value,
        "status": form_status.value,
        "condicoes_saude": form_condicoes.value
    }
    update_abrigado(db, form_id.value, novos_dados)
    tabela.object = read_abrigados(db)

def excluir(event):
    delete_abrigado(db, form_id.value)
    tabela.object = read_abrigados(db)

def filtrar(event):
    resultado = filter_abrigados(
        db,
        nome=form_nome.value,
        status=form_status.value,
        genero=form_genero.value
    )
    tabela.object = resultado

botao_cadastrar = pn.widgets.Button(name="Cadastrar", button_type="primary")
botao_cadastrar.on_click(cadastrar)

botao_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
botao_atualizar.on_click(atualizar)

botao_excluir = pn.widgets.Button(name="Excluir", button_type="danger")
botao_excluir.on_click(excluir)

botao_filtrar = pn.widgets.Button(name="Filtrar", button_type="success")
botao_filtrar.on_click(filtrar)

layout = pn.Column(
    "## CRUD de Pessoas Abrigadas",
    form_id,
    form_nome,
    form_genero,
    form_data_nascimento,
    form_documento,
    form_status,
    form_condicoes,
    pn.Row(botao_cadastrar, botao_atualizar, botao_excluir, botao_filtrar),
    tabela
)

layout.servable()
