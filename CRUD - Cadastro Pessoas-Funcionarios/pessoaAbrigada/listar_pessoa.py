import panel as pn
from pessoaAbrigada.crud import listar_pessoas, atualizar_pessoa, deletar_pessoa

def view():
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
