import panel as pn
from crud import *
from datetime import date

with open("styles.css") as f:
    css = f.read()

pn.extension(raw_css=[css], template='fast')
pn.config.template.title = "Sistema Abrigo"

# --- Cadastrar Pessoa Abrigada ---
def cadastrar_pessoa_view():
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

# --- Listar Pessoas Abrigadas ---
def listar_pessoas_table():
    container = pn.Column()
    titulo = pn.pane.Markdown("## Lista de Pessoas Abrigadas", css_classes=["titulo-principal"])

    def atualizar():
        pessoas = listar_pessoas()
        if not pessoas:
            return pn.pane.Markdown("**Nenhuma pessoa cadastrada ainda.**", width=700, css_classes=["empty-msg"])

        linhas = []
        for pessoa in pessoas:
            nome = pn.widgets.TextInput(value=pessoa.nome, width=180)
            data_nasc = pn.widgets.DatePicker(value=pessoa.data_nascimento, width=140)
            documento = pn.widgets.Select(value=pessoa.documento, options=["RG", "CPF", "CNH", "Outro"], width=120)
            sexo = pn.widgets.Select(value=pessoa.sexo, options=["Masculino", "Feminino", "Outro"], width=120)
            data_entrada = pn.widgets.DatePicker(value=pessoa.data_entrada, width=140)
            cond = pn.widgets.TextAreaInput(value=pessoa.condicoes_saude, width=200, height=50)

            def make_callbacks(pid):
                def salvar(event):
                    atualizar_pessoa(pid, {
                        "nome": nome.value,
                        "data_nascimento": data_nasc.value,
                        "documento": documento.value,
                        "sexo": sexo.value,
                        "data_entrada": data_entrada.value,
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

            linha = pn.Row(
                nome, data_nasc, documento, sexo, data_entrada, cond,
                pn.widgets.Button(name="Salvar", button_type="primary", width=80, on_click=salvar_cb),
                pn.widgets.Button(name="Deletar", button_type="danger", width=80, on_click=deletar_cb),
                css_classes=["table-row"]
            )
            linhas.append(linha)

        cabecalho = pn.Row(
            pn.pane.Markdown("**Nome**", width=180),
            pn.pane.Markdown("**Nascimento**", width=140),
            pn.pane.Markdown("**Documento**", width=120),
            pn.pane.Markdown("**Sexo**", width=120),
            pn.pane.Markdown("**Entrada**", width=140),
            pn.pane.Markdown("**Condições**", width=200),
            pn.pane.Markdown("**Salvar**", width=80),
            pn.pane.Markdown("**Excluir**", width=80),
            css_classes=["table-header"]
        )

        return pn.Column(cabecalho, *linhas)

    def atualizar_lista():
        container[:] = [titulo, atualizar()]

    btn_atualizar = pn.widgets.Button(name="Atualizar Lista", button_type="success", width=200)
    btn_atualizar.on_click(lambda e: atualizar_lista())

    atualizar_lista()
    return pn.Column(btn_atualizar, container)

# --- Cadastrar Funcionário ---
def cadastrar_funcionario_view():
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

# --- Listar Funcionários ---
def listar_funcionarios_table():
    container = pn.Column()
    titulo = pn.pane.Markdown("## Lista de Funcionários", css_classes=["titulo-principal"])

    def atualizar():
        funcionarios = listar_funcionarios()
        if not funcionarios:
            return pn.pane.Markdown("**Nenhum funcionário cadastrado ainda.**", width=700, css_classes=["empty-msg"])

        linhas = []
        for func in funcionarios:
            nome = pn.widgets.TextInput(value=func.nome, width=180)
            cargo = pn.widgets.Select(value=func.cargo, options=["Admin", "Cuidador", "Recepcionista", "Voluntário"], width=160)
            contato = pn.widgets.TextInput(value=func.contato, width=140)
            data_admissao = pn.widgets.DatePicker(value=func.data_admissao, width=140)

            def make_callbacks(fid):
                def salvar(event):
                    atualizar_funcionario(fid, {
                        "nome": nome.value,
                        "cargo": cargo.value,
                        "contato": contato.value,
                        "data_admissao": data_admissao.value
                    })
                    pn.state.notifications.success("Funcionário atualizado.")
                    atualizar_lista()

                def deletar(event):
                    deletar_funcionario(fid)
                    pn.state.notifications.success("Funcionário deletado.")
                    atualizar_lista()

                return salvar, deletar

            salvar_cb, deletar_cb = make_callbacks(func.id)

            linha = pn.Row(
                nome, cargo, contato, data_admissao,
                pn.widgets.Button(name="Salvar", button_type="primary", width=80, on_click=salvar_cb),
                pn.widgets.Button(name="Deletar", button_type="danger", width=80, on_click=deletar_cb),
                css_classes=["table-row"]
            )
            linhas.append(linha)

        cabecalho = pn.Row(
            pn.pane.Markdown("**Nome**", width=180),
            pn.pane.Markdown("**Cargo**", width=160),
            pn.pane.Markdown("**Contato**", width=140),
            pn.pane.Markdown("**Admissão**", width=140),
            pn.pane.Markdown("**Salvar**", width=80),
            pn.pane.Markdown("**Excluir**", width=80),
            css_classes=["table-header"]
        )

        return pn.Column(cabecalho, *linhas)

    def atualizar_lista():
        container[:] = [titulo, atualizar()]

    btn_atualizar = pn.widgets.Button(name="Atualizar Lista", button_type="success", width=200)
    btn_atualizar.on_click(lambda e: atualizar_lista())

    atualizar_lista()
    return pn.Column(btn_atualizar, container)

# --- Navegação com Sidebar ---
conteudo = pn.Column(sizing_mode="stretch_both", css_classes=["conteudo"])

def mostrar_view(view_func):
    conteudo.clear()
    conteudo.append(view_func())
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
