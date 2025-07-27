import panel as pn
import pandas as pd
from datetime import datetime
from database import SessionLocal
from crud import create_abrigado, read_abrigados, delete_abrigado, update_abrigado, filter_abrigados

pn.extension()

db = SessionLocal()

# Widgets de busca
busca_nome = pn.widgets.TextInput(name="Buscar por nome")
busca_status = pn.widgets.Select(name="Status", options=["", "abrigado", "encaminhado", "saiu"])
busca_genero = pn.widgets.Select(name="Gênero", options=["", "Masculino", "Feminino", "Outro"])
botao_buscar = pn.widgets.Button(name="Buscar", button_type="primary")

# Formulário de cadastro/edição
form_nome = pn.widgets.TextInput(name="Nome")
form_genero = pn.widgets.Select(name="Gênero", options=["Masculino", "Feminino", "Outro"])
form_nascimento = pn.widgets.DatePicker(name="Data de nascimento")
form_documento = pn.widgets.TextInput(name="Documento")
form_status = pn.widgets.Select(name="Status", options=["abrigado", "encaminhado", "saiu"])
form_condicoes = pn.widgets.TextAreaInput(name="Condições de saúde")

botao_salvar = pn.widgets.Button(name="Salvar novo", button_type="success")
botao_atualizar = pn.widgets.Button(name="Atualizar", button_type="primary", visible=False)

# Área de resultado
tabela = pn.pane.DataFrame(pd.DataFrame(), sizing_mode="stretch_width", height=300)
mensagem = pn.pane.Markdown("")

# ID do registro que está sendo editado
abrigado_editando_id = [None]

# Funções
def carregar_tabela(event=None):
    abrigados = filter_abrigados(
        db,
        nome=busca_nome.value,
        status=busca_status.value if busca_status.value else None,
        genero=busca_genero.value if busca_genero.value else None
    )
    df = pd.DataFrame([{
        "ID": a.id,
        "Nome": a.nome,
        "Gênero": a.genero,
        "Nascimento": a.data_nascimento,
        "Documento": a.documento,
        "Status": a.status,
        "Saúde": a.condicoes_saude
    } for a in abrigados])
    tabela.object = df

def salvar_novo(event):
    try:
        create_abrigado(
            db,
            nome=form_nome.value,
            genero=form_genero.value,
            data_nascimento=form_nascimento.value,
            documento=form_documento.value,
            status=form_status.value,
            condicoes_saude=form_condicoes.value
        )
        mensagem.object = "✅ Abrigado salvo com sucesso!"
        limpar_form()
        carregar_tabela()
    except Exception as e:
        mensagem.object = f"❌ Erro: {e}"

def limpar_form():
    form_nome.value = ""
    form_genero.value = "Masculino"
    form_nascimento.value = None
    form_documento.value = ""
    form_status.value = "abrigado"
    form_condicoes.value = ""
    abrigado_editando_id[0] = None
    botao_salvar.visible = True
    botao_atualizar.visible = False

def editar_abrigado(event):
    try:
        id = int(event.new)
        dados = [a for a in read_abrigados(db) if a.id == id][0]
        form_nome.value = dados.nome
        form_genero.value = dados.genero
        form_nascimento.value = dados.data_nascimento
        form_documento.value = dados.documento
        form_status.value = dados.status
        form_condicoes.value = dados.condicoes_saude
        abrigado_editando_id[0] = id
        botao_salvar.visible = False
        botao_atualizar.visible = True
    except:
        mensagem.object = "❌ ID inválido para edição."

def atualizar_abrigado_click(event):
    update_abrigado(db, abrigado_editando_id[0], {
        "nome": form_nome.value,
        "genero": form_genero.value,
        "data_nascimento": form_nascimento.value,
        "documento": form_documento.value,
        "status": form_status.value,
        "condicoes_saude": form_condicoes.value
    })
    mensagem.object = "✅ Abrigado atualizado!"
    limpar_form()
    carregar_tabela()

def excluir_abrigado_click(event):
    try:
        id = int(event.new)
        if delete_abrigado(db, id):
            mensagem.object = f"🗑️ Abrigado ID {id} excluído com sucesso."
            carregar_tabela()
        else:
            mensagem.object = "❌ Abrigado não encontrado."
    except:
        mensagem.object = "❌ ID inválido para exclusão."

# Ações
botao_buscar.on_click(carregar_tabela)
botao_salvar.on_click(salvar_novo)
botao_atualizar.on_click(atualizar_abrigado_click)

# Campos para editar ou excluir por ID
campo_id_editar = pn.widgets.TextInput(name="Editar ID")
campo_id_excluir = pn.widgets.TextInput(name="Excluir ID")
campo_id_editar.param.watch(editar_abrigado, 'value')
campo_id_excluir.param.watch(excluir_abrigado_click, 'value')

# Layout
interface = pn.Column(
    "## Busca e Filtragem de Abrigados",
    pn.Row(busca_nome, busca_status, busca_genero, botao_buscar),
    tabela,
    "## Ações",
    pn.Row(campo_id_editar, campo_id_excluir),
    "## Formulário de Cadastro/Edição",
    form_nome, form_genero, form_nascimento, form_documento, form_status, form_condicoes,
    pn.Row(botao_salvar, botao_atualizar),
    mensagem
)

# Inicia a aplicação
interface.servable()
