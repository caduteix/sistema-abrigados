# Arquivo: CRUD - Agendamento de Consultta/views.py (CORRIGIDO PARA EXECUÇÃO PELO PANEL SERVE)

import panel as pn
import param
from datetime import datetime, date, time
from crud_operations import (
    get_all_pessoas_abrigadas,
    get_all_servicos,
    get_all_consultas,
    add_consulta,
    update_consulta,
    delete_consulta
)


# Configurações globais do Panel (essenciais para que o app funcione corretamente)
pn.extension('tabulator', notifications=True) # Habilita a extensão Tabulator e notificações
pn.extension(sizing_mode="stretch_width")    # Define o modo de dimensionamento para preencher a largura

# Painel global para a tabela de agendamentos, para que possa ser atualizado por callbacks
agendamentos_table_pane = pn.Column(sizing_mode="stretch_width")

# --- Constantes ---
STATUS_AGENDAMENTO = ["Agendado", "Realizado", "Cancelado", "Remarcado", "Não Compareceu", "Pendente"]
STATUS_AGENDAMENTO_FILTRO = ["Todos"] + STATUS_AGENDAMENTO

# --- Funções Auxiliares para Carregar Opções de Select ---
def get_pessoas_abrigadas_for_select():
    df = get_all_pessoas_abrigadas()
    if not df.empty:
        return [("Selecione a Pessoa", 0)] + list(df[['nome', 'id_pessoa_abrigada']].itertuples(index=False, name=None))
    return [("Selecione a Pessoa", 0)]

def get_servicos_for_select():
    df = get_all_servicos()
    if not df.empty:
        return [("Selecione o Serviço", 0)] + list(df[['nome', 'id_servico']].itertuples(index=False, name=None))
    return [("Selecione o Serviço", 0)]

# --- Classe Principal para Gerenciar Widgets e Lógica ---
class AgendamentoWidgets(param.Parameterized):
    id_consulta_input = pn.widgets.IntInput(name='ID Agendamento (para Atualizar/Excluir)', value=0, width=200)
    pessoa_abrigada_select = pn.widgets.Select(name='Pessoa Abrigada', options=get_pessoas_abrigadas_for_select(), value=0, width=300)
    servico_select = pn.widgets.Select(name='Serviço', options=get_servicos_for_select(), value=0, width=300)
    data_agendamento_picker = pn.widgets.DatePicker(name='Data Agendamento', value=date.today(), width=200)
    horario_agendamento_picker = pn.widgets.TextInput(name='Horário (HH:MM)', placeholder='Ex: 14:30', value='09:00', width=150)
    profissional_input = pn.widgets.TextInput(name='Profissional', placeholder='Nome do profissional', width=300)
    status_agendamento_select = pn.widgets.Select(name='Status', options=STATUS_AGENDAMENTO, value='Agendado', width=200)
    observacoes_text = pn.widgets.TextAreaInput(name='Observações', placeholder='Detalhes adicionais', height=100, width=400)

    agendar_button = pn.widgets.Button(name='Agendar Consulta', button_type='primary', width=200)
    atualizar_button = pn.widgets.Button(name='Atualizar Agendamento', button_type='warning', width=200)
    excluir_button = pn.widgets.Button(name='Excluir Agendamento', button_type='danger', width=200)
    limpar_campos_button = pn.widgets.Button(name='Limpar Campos', button_type='default', width=200)

    filter_id_consulta_input = pn.widgets.IntInput(name='Filtrar por ID', value=0, width=150)
    filter_pessoa_select = pn.widgets.Select(name='Filtrar por Pessoa', options=get_pessoas_abrigadas_for_select(), value=0, width=250)
    filter_servico_select = pn.widgets.Select(name='Filtrar por Serviço', options=get_servicos_for_select(), value=0, width=250)
    filter_status_select = pn.widgets.Select(name='Filtrar por Status', options=STATUS_AGENDAMENTO_FILTRO, value='Todos', width=200)
    filter_data_inicio_picker = pn.widgets.DatePicker(name='Data Início', width=180)
    filter_data_fim_picker = pn.widgets.DatePicker(name='Data Fim', width=180)
    consultar_button = pn.widgets.Button(name='Consultar Agendamentos', button_type='success', width=200)
    reset_filters_button = pn.widgets.Button(name='Resetar Filtros', button_type='default', width=200)

    def __init__(self, **params):
        super().__init__(**params)
        self._connect_callbacks()
        self.update_agendamentos_display()

    def _connect_callbacks(self):
        self.agendar_button.on_click(self._on_agendar_consulta)
        self.atualizar_button.on_click(self._on_atualizar_agendamento)
        self.excluir_button.on_click(self._on_excluir_agendamento)
        self.limpar_campos_button.on_click(self._on_limpar_campos)
        self.consultar_button.on_click(self._on_consultar_agendamento)
        self.reset_filters_button.on_click(self._on_reset_filters)
        agendamentos_table_pane.param.watch(self._on_table_selection_change, 'objects')

    def _on_agendar_consulta(self, event):
        try:
            if (self.pessoa_abrigada_select.value == 0 or self.servico_select.value == 0 or
                    not self.data_agendamento_picker.value or not self.horario_agendamento_picker.value or
                    not self.profissional_input.value):
                pn.pane.Alert('Erro: Preencha todos os campos obrigatórios.', alert_type='warning').show()
                return
            try:
                datetime.strptime(self.horario_agendamento_picker.value, '%H:%M').time()
            except ValueError:
                pn.pane.Alert('Erro: Formato de horário inválido. Use HH:MM (ex: 14:30).', alert_type='warning').show()
                return
            agendamento_datetime_str = f"{self.data_agendamento_picker.value} {self.horario_agendamento_picker.value}:00"
            agendamento_datetime = datetime.strptime(agendamento_datetime_str, '%Y-%m-%d %H:%M:%S')
            if agendamento_datetime < datetime.now():
                pn.pane.Alert('Erro: A data e hora do agendamento não podem ser retroativas.', alert_type='warning').show()
                return
            success = add_consulta(
                id_pessoa_abrigada=self.pessoa_abrigada_select.value,
                id_servico=self.servico_select.value,
                data_agendamento=str(self.data_agendamento_picker.value),
                horario_agendamento=self.horario_agendamento_picker.value,
                profissional=self.profissional_input.value,
                observacoes=self.observacoes_text.value
            )
            if success:
                pn.pane.Alert('Agendamento inserido com sucesso!', alert_type='success').show()
                self._on_limpar_campos(None)
                self.update_agendamentos_display()
            else:
                pn.pane.Alert('Não foi possível agendar a consulta. Verifique o console.', alert_type='danger').show()
        except Exception as e:
            pn.pane.Alert(f'Erro inesperado ao agendar: {str(e)}', alert_type='danger').show()
            print(f"Erro inesperado ao agendar: {e}")

    def _on_atualizar_agendamento(self, event):
        try:
            if self.id_consulta_input.value == 0:
                pn.pane.Alert('Erro: Informe o ID do Agendamento para atualizar.', alert_type='warning').show()
                return
            if (self.pessoa_abrigada_select.value == 0 or self.servico_select.value == 0 or
                    not self.data_agendamento_picker.value or not self.horario_agendamento_picker.value or
                    not self.profissional_input.value or not self.status_agendamento_select.value):
                pn.pane.Alert('Erro: Preencha todos os campos obrigatórios para atualização.', alert_type='warning').show()
                return
            try:
                datetime.strptime(self.horario_agendamento_picker.value, '%H:%M').time()
            except ValueError:
                pn.pane.Alert('Erro: Formato de horário inválido. Use HH:MM (ex: 14:30).', alert_type='warning').show()
                return
            agendamento_datetime_str = f"{self.data_agendamento_picker.value} {self.horario_agendamento_picker.value}:00"
            agendamento_datetime = datetime.strptime(agendamento_datetime_str, '%Y-%m-%d %H:%M:%S')
            if agendamento_datetime < datetime.now() and self.status_agendamento_select.value == 'Agendado':
                if agendamento_datetime.date() < date.today() and self.status_agendamento_select.value not in ['Realizado', 'Cancelado', 'Não Compareceu']:
                    pn.pane.Alert('Erro: Não é possível agendar para uma data passada ou manter status "Agendado" em data retroativa.', alert_type='warning').show()
                    return
                elif agendamento_datetime.date() >= date.today() and agendamento_datetime < datetime.now():
                    pn.pane.Alert('Erro: Não é possível agendar para um horário passado na data atual.', alert_type='warning').show()
                    return
            success = update_consulta(
                id_consulta=self.id_consulta_input.value,
                id_pessoa_abrigada=self.pessoa_abrigada_select.value,
                id_servico=self.servico_select.value,
                data_agendamento=str(self.data_agendamento_picker.value),
                horario_agendamento=self.horario_agendamento_picker.value,
                profissional=self.profissional_input.value,
                status_agendamento=self.status_agendamento_select.value,
                observacoes=self.observacoes_text.value
            )
            if success:
                pn.pane.Alert('Agendamento atualizado com sucesso!', alert_type='success').show()
                self._on_limpar_campos(None)
                self.update_agendamentos_display()
            else:
                pn.pane.Alert('Não foi possível atualizar o agendamento. Verifique o console.', alert_type='danger').show()
        except Exception as e:
            pn.pane.Alert(f'Erro inesperado ao atualizar: {str(e)}', alert_type='danger').show()
            print(f"Erro inesperado ao atualizar: {e}")

    def _on_excluir_agendamento(self, event):
        try:
            if self.id_consulta_input.value == 0:
                pn.pane.Alert('Erro: Informe o ID do Agendamento para excluir.', alert_type='warning').show()
                return
            success = delete_consulta(self.id_consulta_input.value)
            if success:
                pn.pane.Alert('Agendamento excluído com sucesso!', alert_type='success').show()
                self._on_limpar_campos(None)
                self.update_agendamentos_display()
            else:
                pn.pane.Alert('Não foi possível excluir o agendamento. Verifique o console.', alert_type='danger').show()
        except Exception as e:
            pn.pane.Alert(f'Erro inesperado ao excluir: {str(e)}', alert_type='danger').show()
            print(f"Erro inesperado ao excluir: {e}")

    def _on_limpar_campos(self, event):
        self.id_consulta_input.value = 0
        self.pessoa_abrigada_select.value = 0
        self.servico_select.value = 0
        self.data_agendamento_picker.value = date.today()
        self.horario_agendamento_picker.value = '09:00'
        self.profissional_input.value = ''
        self.status_agendamento_select.value = 'Agendado'
        self.observacoes_text.value = ''

    def update_agendamentos_display(self, query_str=None):
        if query_str is None:
            df_agendamentos = get_all_consultas()
        else:
            df_agendamentos = get_all_consultas()
            pn.pane.Alert('Funcionalidade de filtro avançado será implementada em breve!', alert_type='info').show() # Mover este alert para o _on_consultar_agendamento

        if df_agendamentos.empty:
            agendamentos_table_pane.objects = [pn.pane.Markdown("### Nenhum agendamento encontrado.")]
        else:
            if 'Data Agendamento' in df_agendamentos.columns:
                df_agendamentos['Data Agendamento'] = df_agendamentos['Data Agendamento'].dt.strftime('%Y-%m-%d')
            if 'Horário Agendamento' in df_agendamentos.columns:
                df_agendamentos['Horário Agendamento'] = df_agendamentos['Horário Agendamento'].apply(lambda x: x.strftime('%H:%M') if x else '')
            if 'Data Criação' in df_agendamentos.columns:
                df_agendamentos['Data Criação'] = df_agendamentos['Data Criação'].dt.strftime('%Y-%m-%d %H:%M:%S')

            tabulator = pn.widgets.Tabulator(
                df_agendamentos,
                sizing_mode='stretch_width',
                pagination='remote',
                page_size=10,
                disabled=True,
                selectable='checkbox'
            )
            agendamentos_table_pane.objects = [tabulator]
            tabulator.param.watch(self._on_tabulator_row_selected, 'selection')

    def _on_consultar_agendamento(self, event):
        filters = {}
        if self.filter_id_consulta_input.value != 0:
            filters['id_consulta'] = self.filter_id_consulta_input.value
        if self.filter_pessoa_select.value != 0:
            filters['id_pessoa_abrigada'] = self.filter_pessoa_select.value
        if self.filter_servico_select.value != 0:
            filters['id_servico'] = self.filter_servico_select.value
        if self.filter_status_select.value != 'Todos':
            filters['status_agendamento'] = self.filter_status_select.value
        if self.filter_data_inicio_picker.value:
            filters['data_inicio'] = str(self.filter_data_inicio_picker.value)
        if self.filter_data_fim_picker.value:
            filters['data_fim'] = str(self.filter_data_fim_picker.value)

        self.update_agendamentos_display()
        pn.pane.Alert('Funcionalidade de filtro avançado será implementada em breve!', alert_type='info').show()

    def _on_reset_filters(self, event):
        self.filter_id_consulta_input.value = 0
        self.filter_pessoa_select.value = 0
        self.filter_servico_select.value = 0
        self.filter_status_select.value = 'Todos'
        self.filter_data_inicio_picker.value = None
        self.filter_data_fim_picker.value = None
        self.update_agendamentos_display()

    def _on_tabulator_row_selected(self, event):
        if agendamentos_table_pane.objects and isinstance(agendamentos_table_pane.objects[0], pn.widgets.Tabulator):
            tabulator = agendamentos_table_pane.objects[0]
            if tabulator.selection:
                selected_indices = tabulator.selection
                selected_row_data = tabulator.value.iloc[selected_indices[0]]

                self.id_consulta_input.value = selected_row_data['ID Consulta']
                
                pessoas_df = get_all_pessoas_abrigadas()
                servicos_df = get_all_servicos()

                pessoa_id = pessoas_df[pessoas_df['nome'] == selected_row_data['Pessoa Abrigada']]['id_pessoa_abrigada'].iloc[0] if not pessoas_df.empty else 0
                servico_id = servicos_df[servicos_df['nome'] == selected_row_data['Serviço']]['id_servico'].iloc[0] if not servicos_df.empty else 0
                
                self.pessoa_abrigada_select.value = pessoa_id
                self.servico_select.value = servico_id
                
                self.data_agendamento_picker.value = datetime.strptime(selected_row_data['Data Agendamento'], '%Y-%m-%d').date()
                self.horario_agendamento_picker.value = selected_row_data['Horário Agendamento']
                self.profissional_input.value = selected_row_data['Profissional']
                self.status_agendamento_select.value = selected_row_data['Status']
                self.observacoes_text.value = selected_row_data['Observações'] if pd.notna(selected_row_data['Observações']) else ''

# --- Função Principal que Retorna o Layout do Aplicativo ---
def agendamento_app():
    widgets = AgendamentoWidgets()

    cadastro_agendamento_pane = pn.Card(
        pn.Column(
            pn.Row(widgets.id_consulta_input),
            pn.Row(widgets.pessoa_abrigada_select, widgets.servico_select),
            pn.Row(widgets.data_agendamento_picker, widgets.horario_agendamento_picker),
            pn.Row(widgets.profissional_input, widgets.status_agendamento_select),
            pn.Row(widgets.observacoes_text),
            pn.Row(widgets.agendar_button, widgets.atualizar_button, widgets.excluir_button, widgets.limpar_campos_button)
        ),
        title="Agendar / Atualizar / Excluir Consulta",
        collapsible=True,
        width=800,
        sizing_mode="stretch_width"
    )

    filtros_consulta_pane = pn.Card(
        pn.Column(
            pn.Row(widgets.filter_id_consulta_input, widgets.filter_pessoa_select, widgets.filter_servico_select),
            pn.Row(widgets.filter_status_select, widgets.filter_data_inicio_picker, widgets.filter_data_fim_picker),
            pn.Row(widgets.consultar_button, widgets.reset_filters_button)
        ),
        title="Consultar Agendamentos",
        collapsible=True,
        collapsed=True,
        width=800,
        sizing_mode="stretch_width"
    )

    main_agendamento_column = pn.Column(
        pn.pane.Markdown("# Gerenciamento de Agendamentos de Consultas/Atendimentos"),
        cadastro_agendamento_pane,
        filtros_consulta_pane,
        pn.pane.Markdown("## Agendamentos Existentes"),
        agendamentos_table_pane,
        sizing_mode="stretch_width"
    )

    return main_agendamento_column

# --- Bloco de Execução Principal do Panel ---
agendamento_app().servable()