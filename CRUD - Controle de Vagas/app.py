import panel as pn
from database import SessionLocal
from crud import get_abrigos, get_abrigo_by_id, atualizar_vagas_ocupadas

pn.extension()

db = SessionLocal()

perfil = pn.widgets.Select(name="Perfil do Usuário", options=["visitante", "gestor"])

abrigos = get_abrigos(db)
abrigo_select = pn.widgets.Select(
    name="Selecionar Abrigo",
    options={a.nome: str(a.id) for a in abrigos},
    value=str(abrigos[0].id) if abrigos else None
)

# Campos de exibição
input_capacidade = pn.widgets.IntInput(name="Capacidade Total", disabled=True)
input_ocupadas = pn.widgets.IntInput(name="Vagas Ocupadas", disabled=True)
input_disponiveis = pn.widgets.IntInput(name="Vagas Disponíveis", disabled=True)

mensagem = pn.pane.Markdown("")

# Botões de ação
botao_ocupar = pn.widgets.Button(name="➕ Ocupar 1 vaga", button_type="success")
botao_desocupar = pn.widgets.Button(name="➖ Desocupar 1 vaga", button_type="warning")
botao_remover = pn.widgets.Button(name="❌ Remover 1 vaga total", button_type="danger")

botoes_gestor = pn.Row(botao_ocupar, botao_desocupar, botao_remover)
botoes_visitante = pn.Row(botao_ocupar)

# Carregar dados do abrigo selecionado
def carregar_dados(event=None):
    try:
        abrigo_id = int(abrigo_select.value)
        abrigo = get_abrigo_by_id(db, abrigo_id)
        if abrigo:
            input_capacidade.value = abrigo.capacidade_total
            input_ocupadas.value = abrigo.vagas_ocupadas or 0
            input_disponiveis.value = abrigo.capacidade_total - (abrigo.vagas_ocupadas or 0)
            atualizar_botoes()
    except Exception as e:
        mensagem.object = f"Erro ao carregar abrigo: {e}"

# Atualiza os botões conforme o perfil
def atualizar_botoes(event=None):
    if perfil.value == "gestor":
        botoes.visible = True
        botoes[:] = botoes_gestor
    else:
        botoes.visible = True
        botoes[:] = botoes_visitante

# Ações dos botões
def ocupar_vaga(event):
    if input_ocupadas.value < input_capacidade.value:
        novo_valor = input_ocupadas.value + 1
        salvar_vagas(novo_valor)
    else:
        mensagem.object = "⚠️ Todas as vagas estão ocupadas."

def desocupar_vaga(event):
    if input_ocupadas.value > 0:
        novo_valor = input_ocupadas.value - 1
        salvar_vagas(novo_valor)
    else:
        mensagem.object = "⚠️ Nenhuma vaga ocupada para desocupar."

def remover_vaga_total(event):
    if input_capacidade.value > 0 and input_ocupadas.value < input_capacidade.value:
        novo_total = input_capacidade.value - 1
        novo_ocupadas = input_ocupadas.value
        sucesso, msg = atualizar_vagas_ocupadas(db, int(abrigo_select.value), novo_ocupadas, novo_total)
        mensagem.object = msg
        if sucesso:
            carregar_dados()
    else:
        mensagem.object = "⚠️ Não é possível remover vaga: abrigo cheio ou capacidade zero."

def salvar_vagas(novas_ocupadas):
    sucesso, msg = atualizar_vagas_ocupadas(db, int(abrigo_select.value), novas_ocupadas)
    mensagem.object = msg
    if sucesso:
        carregar_dados()

# Ligações
abrigo_select.param.watch(carregar_dados, "value")
perfil.param.watch(atualizar_botoes, "value")
botao_ocupar.on_click(ocupar_vaga)
botao_desocupar.on_click(desocupar_vaga)
botao_remover.on_click(remover_vaga_total)

# Contêiner dinâmico para botões
botoes = pn.Row()
carregar_dados()

# Layout final
layout = pn.Column(
    "# 🏠 Controle de Vagas - Abrigos",
    perfil,
    abrigo_select,
    pn.Row(input_capacidade, input_ocupadas, input_disponiveis),
    botoes,
    mensagem
)

layout.servable()
