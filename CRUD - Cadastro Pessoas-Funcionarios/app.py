import panel as pn

# Importando as views
from pessoaAbrigada.cadastrar_pessoa import view as cadastrar_pessoa
from pessoaAbrigada.listar_pessoa import view as listar_pessoa
from funcionarios.cadastrar_funcionarios import view as cadastrar_funcionario
from funcionarios.listar_funcionario import view as listar_funcionario

try:
    with open("styles.css") as f:
        css = f.read()
    pn.extension(raw_css=[css])
except FileNotFoundError:
    pn.extension()

main_area = pn.Column()

# Dicionário com as opções do menu e suas respectivas views
opcoes_menu = {
    "Cadastrar Pessoa Abrigada": cadastrar_pessoa,
    "Listar Pessoas Abrigadas": listar_pessoa,
    "Cadastrar Funcionário": cadastrar_funcionario,
    "Listar Funcionários": listar_funcionario
}

botoes_menu = []
def criar_callback(nome):
    def callback(event):
        main_area[:] = [opcoes_menu[nome]()]
    return callback

for nome in opcoes_menu:
    botao = pn.widgets.Button(
        name=nome,
        button_type="primary",
        css_classes=["sidebar-button"]
    )
    botao.on_click(criar_callback(nome))
    botoes_menu.append(botao)

# Sidebar com os botões
sidebar = pn.Column(
    *botoes_menu,
    sizing_mode="stretch_width",
    margin=(10, 10),
    css_classes=["sidebar"]
)

# Template principal
app = pn.template.FastListTemplate(
    title="Sistema Abrigo",
    sidebar=sidebar,
    main=[main_area]
)

# Tela inicial padrão
main_area[:] = [cadastrar_pessoa()]
app.servable()
