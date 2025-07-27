-- Script SQL Completo para o Sistema de Gestão de Abrigo de Pessoas de Rua

-- Criação das Tabelas

-- Tabela Abrigo
CREATE TABLE IF NOT EXISTS Abrigo (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco TEXT,
    capacidade_total INTEGER NOT NULL,
    telefone VARCHAR(50),
    vagas_disponiveis INTEGER NOT NULL DEFAULT 0 CHECK (vagas_disponiveis >= 0)
);

-- Tabela Funcionario
CREATE TABLE IF NOT EXISTS Funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    contato VARCHAR(100),
    data_admissao DATE
);

-- Tabela Pessoa_Abrigada (para Cadastro e Filtragem de Abrigados)
CREATE TABLE IF NOT EXISTS pessoa_abrigada (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    genero TEXT,
    data_nascimento DATE,
    documento TEXT,
    status TEXT,
    condicoes_saude TEXT,
    data_entrada DATE
);

-- Tabela Servico
CREATE TABLE IF NOT EXISTS Servico (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- Tabela doacoes_estoque
CREATE TABLE IF NOT EXISTS doacoes_estoque (
    id_item_estoque SERIAL PRIMARY KEY,
    tipo_item VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade_atual INTEGER NOT NULL CHECK (quantidade_atual >= 0),
    unidade_medida VARCHAR(50),
    data_ultima_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nome_doador VARCHAR(255)
);

-- Tabela Historico
CREATE TABLE IF NOT EXISTS Historico (
    id SERIAL PRIMARY KEY,
    data_entrada DATE NOT NULL,
    data_saida DATE,
    motivo_saida TEXT,
    destino_pos_abrigo TEXT,
    observacoes TEXT,
    id_abrigado INTEGER NOT NULL,
    CONSTRAINT fk_historico_abrigado FOREIGN KEY (id_abrigado) REFERENCES pessoa_abrigada(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Agendamento (para Agendamento de Consulta)
CREATE TABLE IF NOT EXISTS Agendamento (
    id SERIAL PRIMARY KEY,
    data_agendamento DATE NOT NULL,
    hora_agendamento TIME NOT NULL,
    tipo_agendamento VARCHAR(100),
    profissional_instituicao VARCHAR(255),
    status_agendamento VARCHAR(50),
    observacoes TEXT,
    id_abrigado INTEGER NOT NULL,
    CONSTRAINT fk_agendamento_abrigado FOREIGN KEY (id_abrigado) REFERENCES pessoa_abrigada(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Instituicao_Destino
CREATE TABLE IF NOT EXISTS Instituicao_Destino (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    descricao TEXT
);

-- Tabela Encaminhamento
CREATE TABLE IF NOT EXISTS Encaminhamento (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100),
    data_encaminhamento DATE NOT NULL,
    status VARCHAR(50),
    id_instituicao_destino INTEGER NOT NULL,
    id_abrigado INTEGER NOT NULL,
    responsavel_encaminhamento INTEGER,
    CONSTRAINT fk_encaminhamento_instituicao FOREIGN KEY (id_instituicao_destino) REFERENCES Instituicao_Destino(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_encaminhamento_abrigado FOREIGN KEY (id_abrigado) REFERENCES pessoa_abrigada(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_encaminhamento_responsavel FOREIGN KEY (responsavel_encaminhamento) REFERENCES Funcionario(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Criação das Tabelas Associativas 

-- Tabela Trabalha_Para (Funcionário em Abrigo)
CREATE TABLE IF NOT EXISTS Trabalha_Para (
    id_abrigo INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    PRIMARY KEY (id_abrigo, id_funcionario),
    CONSTRAINT fk_trabalha_abrigo FOREIGN KEY (id_abrigo) REFERENCES Abrigo(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_trabalha_funcionario FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Oferece_Um (Abrigo oferece Serviço)
CREATE TABLE IF NOT EXISTS Oferece_Um (
    id_abrigo INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    PRIMARY KEY (id_abrigo, id_servico),
    CONSTRAINT fk_oferece_abrigo FOREIGN KEY (id_abrigo) REFERENCES Abrigo(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_oferece_servico FOREIGN KEY (id_servico) REFERENCES Servico(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Recebe_Doacao (Pessoa Abrigada recebe item do Estoque de Doações)
CREATE TABLE IF NOT EXISTS Recebe_Doacao (
    id_item_estoque INTEGER NOT NULL,
    id_pessoa_abrigada INTEGER NOT NULL,
    PRIMARY KEY (id_item_estoque, id_pessoa_abrigada),
    CONSTRAINT fk_recebe_doacao_estoque FOREIGN KEY (id_item_estoque) REFERENCES doacoes_estoque(id_item_estoque) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_recebe_pessoa FOREIGN KEY (id_pessoa_abrigada) REFERENCES pessoa_abrigada(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Usa_O (Pessoa Abrigada usa Serviço)
CREATE TABLE IF NOT EXISTS Usa_O (
    id_servico INTEGER NOT NULL,
    id_pessoa_abrigada INTEGER NOT NULL,
    data_uso DATE NOT NULL,
    resultado TEXT,
    frequencia TEXT,
    PRIMARY KEY (id_servico, id_pessoa_abrigada, data_uso),
    CONSTRAINT fk_usa_servico FOREIGN KEY (id_servico) REFERENCES Servico(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_usa_pessoa FOREIGN KEY (id_pessoa_abrigada) REFERENCES pessoa_abrigada(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabela Consulta (ligação Agendamento e Serviço)
CREATE TABLE IF NOT EXISTS Consulta (
    id_agendamento INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    profissional VARCHAR(255),
    PRIMARY KEY (id_agendamento, id_servico),
    CONSTRAINT fk_consulta_agendamento FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_servico FOREIGN KEY (id_servico) REFERENCES Servico(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Ajustes e Adição de FKs

-- Adicionar FK Responsável em Serviço
ALTER TABLE Servico
ADD COLUMN id_funcionario_responsavel INTEGER,
ADD CONSTRAINT fk_servico_funcionario FOREIGN KEY (id_funcionario_responsavel) REFERENCES Funcionario(id) ON DELETE SET NULL ON UPDATE CASCADE;

-- Inserção de Dados de Exemplo

-- doacoes_estoque (com o campo nome_doador da antiga tabela Doacoes)
INSERT INTO doacoes_estoque (tipo_item, descricao, quantidade_atual, unidade_medida, nome_doador) VALUES
('Alimento', 'Arroz 5kg', 150, 'kg', 'Empresa Solidária'),
('Roupa', 'Camisetas masculinas M', 80, 'unidade', 'Maria do Carmo'),
('Higiene', 'Sabonete líquido 1L', 120, 'litro', 'João Ninguém'),
('Dinheiro', 'Doação em dinheiro', 500, 'unidade', 'Anônimo'),
('Alimento', 'Feijão 1kg', 200, 'kg', 'Feira Livre do Bairro'),
('Roupa', 'Calças jeans femininas', 60, 'unidade', 'Família Silva'),
('Higiene', 'Pasta de dente', 300, 'unidade', 'Lar dos Idosos'),
('Alimento', 'Óleo de cozinha', 90, 'litro', 'Padaria Central'),
('Roupa', 'Casacos infantis', 45, 'unidade', 'Igreja da Comunidade'),
('Higiene', 'Shampoo 500ml', 75, 'litro', 'ONG Criança Feliz'),
('Alimento', 'Leite em pó 400g', 180, 'unidade', 'Doador Teste 1'),
('Roupa', 'Meias unissex', 250, 'par', 'Doador Teste 2'),
('Higiene', 'Escovas de dente', 280, 'unidade', 'Doador Teste 3');

-- pessoa_abrigada
INSERT INTO pessoa_abrigada (nome, genero, data_nascimento, documento, status, condicoes_saude, data_entrada) VALUES
('João Silva', 'Masculino', '1980-03-12', '12345678900', 'abrigado', 'diabetes', '2024-01-15'),
('Maria Oliveira', 'Feminino', '1975-05-10', '98765432100', 'abrigado', 'hipertensão', '2024-02-20'),
('Carlos Pereira', 'Masculino', '1968-07-21', '11122233344', 'encaminhado', 'nenhuma', '2024-03-01'),
('Ana Lima', 'Feminino', '1985-01-22', '22233344455', 'abrigado', 'deficiência visual', '2024-04-10'),
('Pedro Souza', 'Masculino', '1990-12-01', '33344455566', 'saiu', 'epilepsia', '2024-05-05'),
('Juliana Rocha', 'Feminino', '2000-08-30', '44455566677', 'abrigado', 'diabetes', '2024-06-01'),
('Rafael Duarte', 'Masculino', '1982-04-17', '55566677788', 'abrigado', 'nenhuma', '2024-07-10'),
('Luciana Costa', 'Feminino', '1979-06-05', '66677788899', 'encaminhado', 'hipertensão', '2024-08-12'),
('Bruno Marques', 'Masculino', '1995-11-09', '77788899900', 'saiu', 'deficiência auditiva', '2024-09-01'),
('Camila Nunes', 'Feminino', '1988-02-28', '88899900011', 'abrigado', 'diabetes', '2024-10-25');

-- Abrigo
INSERT INTO Abrigo (nome, endereco, capacidade_total, telefone, vagas_disponiveis) VALUES
('Abrigo Esperança', 'Rua da Paz, 123', 50, '21987654321', 40),
('Casa Acolhedora', 'Av. Central, 456', 30, '1134567890', 25),
('Recanto Seguro', 'Travessa da Felicidade, 78', 60, '31998765432', 50),
('Novo Lar', 'Rua dos Sonhos, 90', 40, '4133221100', 35),
('Porto da Solidariedade', 'Alameda das Rosas, 10', 20, '51987612345', 18),
('Estrela Guia', 'Praça do Sol, 5', 25, '6130009988', 20),
('Caminho da Luz', 'Rua da Espera, 200', 35, '7190901010', 30),
('Vila Feliz', 'Estrada Velha, 300', 45, '8132109876', 40),
('Aconchego Urbano', 'Viela Estreita, 1', 15, '9198765432', 10),
('Paz e Harmonia', 'Largo da União, 7', 55, '2133445566', 50);

-- Funcionario
INSERT INTO Funcionario (nome, cargo, contato, data_admissao) VALUES
('Ana Paula', 'Gestora', 'ana.paula@abrigo.com', '2020-01-10'),
('Bruno Fernandes', 'Assistente Social', 'bruno.f@abrigo.com', '2021-03-01'),
('Carla Dias', 'Voluntária', 'carla.d@voluntaria.org', '2022-05-15'),
('Daniel Costa', 'Cozinheiro', 'daniel.c@abrigo.com', '2019-11-20'),
('Eliana Santos', 'Enfermeira', 'eliana.s@abrigo.com', '2023-01-25'),
('Fábio Lima', 'Auxiliar de Limpeza', 'fabio.l@abrigo.com', '2022-08-01'),
('Gabriela Rocha', 'Psicóloga', 'gabriela.r@abrigo.com', '2021-09-10'),
('Heloísa Mello', 'Recepcionista', 'heloisa.m@abrigo.com', '2023-03-15'),
('Igor Pereira', 'Segurança', 'igor.p@abrigo.com', '2020-06-01'),
('Julia Almeida', 'Nutricionista', 'julia.a@abrigo.com', '2022-02-05');

-- Servico
INSERT INTO Servico (nome, descricao) VALUES
('Alimentação Diária', 'Serviço de refeições completas (café, almoço, janta)'),
('Apoio Psicológico', 'Sessões individuais e em grupo de apoio psicológico'),
('Orientação Jurídica', 'Atendimento para questões legais e documentação'),
('Apoio Médico', 'Consultas e acompanhamento de saúde básica'),
('Oficina de Artesanato', 'Atividades de criação com diversos materiais'),
('Banho e Higiene', 'Disponibilização de estrutura para banho e itens de higiene'),
('Corte de Cabelo', 'Serviço de corte de cabelo voluntário'),
('Lavanderia', 'Serviço de lavagem e secagem de roupas'),
('Treinamento Profissional', 'Cursos e capacitações para reinserção no mercado de trabalho'),
('Acompanhamento Nutricional', 'Orientações e planos alimentares personalizados');

-- Historico
INSERT INTO Historico (id_abrigado, data_entrada, data_saida, motivo_saida, destino_pos_abrigo) VALUES
(1, '2024-01-15', '2024-03-01', 'Reencontro familiar', 'Casa da Família'),
(2, '2024-02-20', NULL, NULL, NULL),
(3, '2024-03-01', '2024-03-15', 'Encaminhado para reabilitação', 'Clínica de Reabilitação Alpha'),
(4, '2024-04-10', NULL, NULL, NULL),
(5, '2024-05-05', '2024-05-20', 'Saída voluntária', 'Endereço desconhecido'),
(6, '2024-06-01', NULL, NULL, NULL),
(7, '2024-07-10', NULL, NULL, NULL),
(8, '2024-08-12', '2024-08-25', 'Encaminhado para moradia', 'Apartamento Alugado'),
(9, '2024-09-01', '2024-09-10', 'Saída voluntária', 'Endereço desconhecido'),
(10, '2024-10-25', NULL, NULL, NULL);

-- Agendamento
INSERT INTO Agendamento (id_abrigado, data_agendamento, hora_agendamento, tipo_agendamento, profissional_instituicao, status_agendamento) VALUES
(1, '2025-08-01', '10:00:00', 'Consulta Médica', 'Dr. Silva', 'Agendado'),
(2, '2025-08-01', '14:00:00', 'Atendimento Psicológico', 'Dra. Ana', 'Agendado'),
(3, '2025-08-02', '09:30:00', 'Orientação Jurídica', 'Dr. Souza', 'Agendado'),
(4, '2025-08-03', '11:00:00', 'Consulta Odontológica', 'Dr. Santos', 'Agendado'),
(5, '2025-08-04', '15:00:00', 'Sessão de Terapia Ocupacional', 'Terapeuta Paula', 'Agendado'),
(1, '2025-07-20', '09:00:00', 'Consulta Médica', 'Dr. Silva', 'Realizado'),
(2, '2025-07-21', '13:00:00', 'Atendimento Psicológico', 'Dra. Ana', 'Realizado'),
(6, '2025-08-05', '10:30:00', 'Consulta com Nutricionista', 'Nutri. Fernanda', 'Agendado'),
(7, '2025-08-06', '14:30:00', 'Atendimento Social', 'Assistente Carlos', 'Agendado'),
(8, '2025-08-07', '09:00:00', 'Exame de Rotina', 'Clínica Vida', 'Agendado'),
(9, '2025-08-08', '11:00:00', 'Sessão de Fisioterapia', 'Fisio. Roberto', 'Agendado'),
(10, '2025-08-09', '10:00:00', 'Acompanhamento Farmacêutico', 'Farm. Clara', 'Agendado');


-- Instituicao_Destino
INSERT INTO Instituicao_Destino (nome, tipo, descricao) VALUES
('Hospital Municipal', 'Hospital', 'Hospital público geral.'),
('Clínica de Reabilitação Alpha', 'Clínica de Reabilitação', 'Especializada em recuperação de dependentes químicos.'),
('Centro de Apoio Psicossocial (CAPS)', 'Saúde Mental', 'Oferece atendimento psicossocial.'),
('Escola de Qualificação Profissional', 'Educação/Profissional', 'Cursos profissionalizantes.'),
('Associação Amigos do Bem', 'ONG', 'Suporte a pessoas em vulnerabilidade.'),
('Lar dos Idosos Feliz', 'Abrigo para Idosos', 'Acolhimento de idosos sem moradia.'),
('Maternidade da Cidade', 'Maternidade', 'Atendimento a gestantes em situação de rua.'),
('Abrigo Feminino Maria', 'Abrigo Feminino', 'Abrigo exclusivo para mulheres.'),
('Comunidade Terapêutica Luz', 'Comunidade Terapêutica', 'Tratamento para transtornos mentais e dependência.'),
('Casa de Passagem Boa Esperança', 'Casa de Passagem', 'Acolhimento temporário.');

-- Encaminhamento
INSERT INTO Encaminhamento (id_abrigado, id_instituicao_destino, tipo, data_encaminhamento, status, responsavel_encaminhamento) VALUES
(3, 2, 'Reabilitação', '2024-03-10', 'Concluído', 2),
(8, 5, 'Moradia', '2024-08-20', 'Concluído', 2),
(1, 1, 'Saúde', '2025-07-20', 'Pendente', 5),
(4, 3, 'Psicossocial', '2025-07-25', 'Agendado', 7),
(6, 4, 'Profissional', '2025-08-01', 'Agendado', 1),
(10, 1, 'Saúde', '2025-08-05', 'Pendente', 5),
(2, 3, 'Psicossocial', '2025-08-10', 'Agendado', 7),
(7, 4, 'Profissional', '2025-08-15', 'Agendado', 1),
(9, 2, 'Reabilitação', '2024-09-05', 'Concluído', 2),
(5, 5, 'Moradia', '2024-05-10', 'Cancelado', 2);

-- Trabalha_Para
INSERT INTO Trabalha_Para (id_abrigo, id_funcionario) VALUES
(1, 1), (1, 2), (1, 4), (1, 5), (1, 7),
(2, 1), (2, 3), (2, 6), (2, 8),
(3, 2), (3, 9), (3, 10),
(4, 1), (4, 4),
(5, 2);

-- Oferece_Um
INSERT INTO Oferece_Um (id_abrigo, id_servico) VALUES
(1, 1), (1, 2), (1, 4), (1, 6),
(2, 1), (2, 5), (2, 7),
(3, 1), (3, 3), (3, 8),
(4, 1), (4, 9),
(5, 1), (5, 10);

-- Recebe_Doacao
INSERT INTO Recebe_Doacao (id_item_estoque, id_pessoa_abrigada) VALUES
(1, 1), (2, 2), (3, 4), (4, 6),
(5, 1), (6, 4),
(7, 1), (8, 2), (9, 4), (10, 6), (11, 7), (12, 10);

-- Usa_O
INSERT INTO Usa_O (id_servico, id_pessoa_abrigada, data_uso, resultado, frequencia) VALUES
(1, 1, '2025-07-27', 'Completo', 'Diário'),
(1, 2, '2025-07-27', 'Completo', 'Diário'),
(2, 1, '2025-07-26', 'Completo', 'Semanal'),
(4, 2, '2025-07-25', 'Completo', 'Mensal'),
(6, 4, '2025-07-27', 'Completo', 'Diário'),
(1, 6, '2025-07-27', 'Completo', 'Diário'),
(2, 7, '2025-07-24', 'Parcial', 'Semanal'),
(4, 8, '2025-07-23', 'Completo', 'Mensal'),
(1, 9, '2024-09-05', 'Completo', 'Diário'),
(1, 10, '2025-07-27', 'Completo', 'Diário');

-- Consulta
INSERT INTO Consulta (id_agendamento, id_servico, profissional) VALUES
(1, 4, 'Dr. Silva'), 
(2, 2, 'Dra. Ana'), 
(3, 3, 'Dr. Souza'),
(4, 4, 'Dr. Santos'),  
(5, 5, 'Terapeuta Paula'),
(6, 4, 'Dr. Silva'),  
(7, 2, 'Dra. Ana'),    
(8, 10, 'Nutri. Fernanda'), 
(9, 3, 'Assistente Carlos'), 
(10, 4, 'Clínica Vida'); 
