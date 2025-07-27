import panel as pn
from funcionarios.crud import listar_funcionarios, atualizar_funcionario, deletar_funcionario

def view():
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
