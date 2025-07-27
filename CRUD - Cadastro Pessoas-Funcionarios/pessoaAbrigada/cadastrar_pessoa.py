import panel as pn
from pessoaAbrigada.crud import criar_pessoa

def view():
    nome = pn.widgets.TextInput(name="Nome", placeholder="Nome completo")
    data_nascimento = pn.widgets.DatePicker(name="Data de Nascimento")
    documento = pn.widgets.Select(name="Documento", options=["RG", "CPF", "CNH", "Outro"])
    sexo = pn.widgets.Select(name="Sexo", options=["Masculino", "Feminino", "Outro"])
    data_entrada = pn.widgets.DatePicker(name="Data de Entrada")
    condicoes_saude = pn.widgets.TextAreaInput(name="Condições de Saúde", height=100)

    botao = pn.widgets.Button(name="Cadastrar", button_type="primary")
    msg = pn.pane.Markdown("", width=700)
    titulo = pn.pane.Markdown("## Cadastro de Pessoa Abrigada", css_classes=["titulo-principal"])

    def cadastrar(event):
        if not nome.value or not data_nascimento.value or not data_entrada.value:
            msg.object = "<div class='msg-erro'>Preencha os campos obrigatórios.</div>"
            return

        criar_pessoa({
            "nome": nome.value,
            "data_nascimento": data_nascimento.value,
            "documento": documento.value,
            "sexo": sexo.value,
            "data_entrada": data_entrada.value,
            "condicoes_saude": condicoes_saude.value
        })
        msg.object = "<div class='msg-sucesso'>Pessoa cadastrada com sucesso!</div>"
        nome.value = ""
        data_nascimento.value = None
        documento.value = ""
        sexo.value = "Masculino"
        data_entrada.value = None
        condicoes_saude.value = ""

    botao.on_click(cadastrar)

    return pn.Column(titulo, nome, data_nascimento, documento, sexo, data_entrada, condicoes_saude, botao, msg, css_classes=["form-panel"])
