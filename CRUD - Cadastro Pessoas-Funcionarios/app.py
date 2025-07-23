import panel as pn
from crud import *
from datetime import date

with open("styles.css") as f:
    css = f.read()

pn.extension(raw_css=[css], template='fast')
pn.config.template.title = "Sistema Abrigo"

def cadastrar_pessoa_view():
    nome = pn.widgets.TextInput(name="Nome")
    data_nascimento = pn.widgets.DatePicker(name="Data de Nascimento")
    documento = pn.widgets.Select(name="Documento", options=["RG", "CPF", "CNH", "Outro"])
    sexo = pn.widgets.Select(name="Sexo", options=["Masculino", "Feminino", "Outro"])
    condicoes_saude = pn.widgets.TextAreaInput(name="Condições de Saúde", height=100)

    botao = pn.widgets.Button(name="Cadastrar", button_type="primary")
    msg = pn.pane.Markdown("", width=700)

    titulo = pn.pane.Markdown("## Cadastro de Pessoa Abrigada", css_classes=["titulo-principal"])

    def cadastrar(event):
        if not nome.value or not data_nascimento.value:
            msg.object = "<div class='msg-erro'>Preencha os campos obrigatórios.</div>"
            return

        criar_pessoa({
            "nome": nome.value,
            "data_nascimento": data_nascimento.value,
            "documento": documento.value,
            "sexo": sexo.value,
            "condicoes_saude": condicoes_saude.value
        })
        msg.object = "<div class='msg-sucesso'>Pessoa cadastrada com sucesso!</div>"
        nome.value = ""
        data_nascimento.value = None
        documento.value = ""
        sexo.value = "Masculino"
        condicoes_saude.value = ""

    botao.on_click(cadastrar)

    return pn.Column(titulo, nome, data_nascimento, documento, sexo, condicoes_saude, botao, msg, css_classes=["form-panel"])


def listar_pessoas_table():
    container = pn.Column()
    titulo = pn.pane.Markdown("## Lista de Pessoas Abrigadas", css_classes=["titulo-principal"])

    def atualizar():
        pessoas = listar_pessoas()
        if not pessoas:
            return pn.pane.Markdown("**Nenhuma pessoa cadastrada ainda.**", width=700, css_classes=["empty-msg"])

        linhas = []
        for pessoa in pessoas:
            nome = pn.widgets.TextInput(value=pessoa.nome, width=200)
            data_nasc = pn.widgets.DatePicker(value=pessoa.data_nascimento, width=180)
            documento = pn.widgets.Select(value=pessoa.documento, options=["RG", "CPF", "CNH", "Outro"], width=150)
            sexo = pn.widgets.Select(value=pessoa.sexo, options=["Masculino", "Feminino", "Outro"], width=150)
            cond = pn.widgets.TextAreaInput(value=pessoa.condicoes_saude, width=200, height=50)

            def make_callbacks(pid):
                def salvar(event):
                    atualizar_pessoa(pid, {
                        "nome": nome.value,
                        "data_nascimento": data_nasc.value,
                        "documento": documento.value,
                        "sexo": sexo.value,
                        "condicoes_saude": cond.value
                    })
                    pn.state.notifications.success("Pessoa atualizada.")
                    atualizar_lista()

                def deletar(event):
                    deletar_pessoa(pid)
                    pn.state.notifications.success("Pessoa deletada.")
                    atualizar_lista()

                return salvar, deletar

            salvar_cb, deletar_cb = make_callbacks(pessoa.id)

            btn_salvar = pn.widgets.Button(name="Salvar", button_type="primary", width=100)
            btn_salvar.on_click(salvar_cb)

            btn_deletar = pn.widgets.Button(name="Deletar", button_type="danger", width=100)
            btn_deletar.on_click(deletar_cb)

            linha = pn.Row(nome, data_nasc, documento, sexo, cond, btn_salvar, btn_deletar)
            linhas.append(linha)

        return pn.Column(*linhas)

    def atualizar_lista():
        container[:] = [titulo, atualizar()]

    btn_atualizar = pn.widgets.Button(name="Atualizar Lista", button_type="success", width=200)
    btn_atualizar.on_click(lambda e: atualizar_lista())

    atualizar_lista()
    return pn.Column(btn_atualizar, container)

def cadastrar_funcionario_view():
    nome = pn.widgets.TextInput(name="Nome")
    cargo = pn.widgets.Select(name="Cargo", options=["Admin", "Cuidador", "Recepcionista", "Voluntário"])
    contato = pn.widgets.TextInput(name="Telefone", placeholder="(88) 8888-8888")

    botao = pn.widgets.Button(name="Cadastrar", button_type="primary")
    msg = pn.pane.Markdown("", width=700)

    titulo = pn.pane.Markdown("## Cadastro de Funcionário", css_classes=["titulo-principal"])

    def cadastrar(event):
        if not nome.value or not cargo.value:
            msg.object = "<div class='msg-erro'>Preencha os campos obrigatórios.</div>"
            return

        criar_funcionario({
            "nome": nome.value,
            "cargo": cargo.value,
            "contato": contato.value
        })
        msg.object = "<div class='msg-sucesso'>Funcionário cadastrado com sucesso!</div>"
        nome.value = ""
        cargo.value = ""
        contato.value = ""

    botao.on_click(cadastrar)

    return pn.Column(titulo, nome, cargo, contato, botao, msg, css_classes=["form-panel"])


def listar_funcionarios_table():
    container = pn.Column()
    titulo = pn.pane.Markdown("## Lista de Funcionários", css_classes=["titulo-principal"])

    def atualizar():
        funcionarios = listar_funcionarios()
        if not funcionarios:
            return pn.pane.Markdown("**Nenhum funcionário cadastrado ainda.**", width=700, css_classes=["empty-msg"])

        linhas = []
        for func in funcionarios:
            nome = pn.widgets.TextInput(value=func.nome, width=200)
            cargo = pn.widgets.Select(value=func.cargo, options=["Admin", "Cuidador", "Recepcionista", "Voluntário"], width=200)
            contato = pn.widgets.TextInput(value=func.contato, width=180)

            def make_callbacks(fid):
                def salvar(event):
                    atualizar_funcionario(fid, {
                        "nome": nome.value,
                        "cargo": cargo.value,
                        "contato": contato.value
                    })
                    pn.state.notifications.success("Funcionário atualizado.")
                    container[:] = [titulo, atualizar()]

                def deletar(event):
                    deletar_funcionario(fid)
                    pn.state.notifications.success("Funcionário deletado.")
                    container[:] = [titulo, atualizar()]

                return salvar, deletar

            salvar_cb, deletar_cb = make_callbacks(func.id)

            btn_salvar = pn.widgets.Button(name="Salvar", button_type="primary", width=100)
            btn_salvar.on_click(salvar_cb)

            btn_deletar = pn.widgets.Button(name="Deletar", button_type="danger", width=100)
            btn_deletar.on_click(deletar_cb)

            linha = pn.Row(nome, cargo, contato, btn_salvar, btn_deletar)
            linhas.append(linha)

        return pn.Column(*linhas)

    def atualizar_lista():
        container[:] = [titulo, atualizar()]

    btn_atualizar = pn.widgets.Button(name="Atualizar Lista", button_type="success", width=200)
    btn_atualizar.on_click(lambda e: atualizar_lista())

    container[:] = [titulo, atualizar()]
    return pn.Column(btn_atualizar, container)


# Layout com sidebar e controle do botão ativo via button_type
conteudo = pn.Column(sizing_mode="stretch_both", css_classes=["conteudo"])


def mostrar_view(view_func):
    conteudo.clear()
    conteudo.append(view_func())
    # Ajusta o button_type para simular botão ativo
    for btn in [btn_cad_pessoa, btn_list_pessoa, btn_cad_func, btn_list_func]:
        btn.button_type = "default"
    if view_func == cadastrar_pessoa_view:
        btn_cad_pessoa.button_type = "primary"
    elif view_func == listar_pessoas_table:
        btn_list_pessoa.button_type = "primary"
    elif view_func == cadastrar_funcionario_view:
        btn_cad_func.button_type = "primary"
    elif view_func == listar_funcionarios_table:
        btn_list_func.button_type = "primary"


btn_cad_pessoa = pn.widgets.Button(name="Cadastrar Pessoa Abrigada", button_type="primary", css_classes=["sidebar-button"])
btn_list_pessoa = pn.widgets.Button(name="Listar Pessoas Abrigadas", button_type="default", css_classes=["sidebar-button"])
btn_cad_func = pn.widgets.Button(name="Cadastrar Funcionário", button_type="default", css_classes=["sidebar-button"])
btn_list_func = pn.widgets.Button(name="Listar Funcionários", button_type="default", css_classes=["sidebar-button"])

btn_cad_pessoa.on_click(lambda e: mostrar_view(cadastrar_pessoa_view))
btn_list_pessoa.on_click(lambda e: mostrar_view(listar_pessoas_table))
btn_cad_func.on_click(lambda e: mostrar_view(cadastrar_funcionario_view))
btn_list_func.on_click(lambda e: mostrar_view(listar_funcionarios_table))

mostrar_view(cadastrar_pessoa_view)

sidebar = pn.Column(
    btn_cad_pessoa,
    btn_list_pessoa,
    btn_cad_func,
    btn_list_func,
    css_classes=["sidebar"],
)

app = pn.Row(
    sidebar,
    conteudo,
    sizing_mode="stretch_width",
    margin=20
)

app.servable()
