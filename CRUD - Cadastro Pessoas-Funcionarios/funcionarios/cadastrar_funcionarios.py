import panel as pn
from funcionarios.crud import criar_funcionario

def view():
    nome = pn.widgets.TextInput(name="Nome", placeholder="Nome completo")
    cargo = pn.widgets.Select(name="Cargo", options=["Admin", "Cuidador", "Recepcionista", "Voluntário"])
    contato = pn.widgets.TextInput(name="Telefone", placeholder="(88) 8888-8888")
    data_admissao = pn.widgets.DatePicker(name="Data de Admissão")

    botao = pn.widgets.Button(name="Cadastrar", button_type="primary")
    msg = pn.pane.Markdown("", width=700)
    titulo = pn.pane.Markdown("## Cadastro de Funcionário", css_classes=["titulo-principal"])

    def cadastrar(event):
        if not nome.value or not cargo.value or not data_admissao.value:
            msg.object = "<div class='msg-erro'>Preencha os campos obrigatórios.</div>"
            return

        criar_funcionario({
            "nome": nome.value,
            "cargo": cargo.value,
            "contato": contato.value,
            "data_admissao": data_admissao.value
        })
        msg.object = "<div class='msg-sucesso'>Funcionário cadastrado com sucesso!</div>"
        nome.value = ""
        cargo.value = ""
        contato.value = ""
        data_admissao.value = None

    botao.on_click(cadastrar)

    return pn.Column(titulo, nome, cargo, contato, data_admissao, botao, msg, css_classes=["form-panel"])
