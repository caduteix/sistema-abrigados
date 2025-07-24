-- 1. Tabela 'pessoas_abrigadas' (Simplificada para a FK)
CREATE TABLE IF NOT EXISTS pessoas_abrigadas (
    id_pessoa_abrigada SERIAL PRIMARY KEY, -- Corresponde a "ID pessoa abrigada"
    nome TEXT NOT NULL,
    data_nascimento DATE,
    documento VARCHAR(50),
    sexo VARCHAR(20),
    data_entrada DATE
);


-- 2. Tabela 'servicos'
CREATE TABLE IF NOT EXISTS servicos (
    id_servico SERIAL PRIMARY KEY, -- Corresponde a "ID servico"
    nome TEXT NOT NULL UNIQUE, -- Nome do serviço (ex: Consulta Médica, Atendimento Psicológico)
    descricao TEXT,
    responsavel TEXT -- Pode ser o profissional ou a área responsável
);

-- 2. Tabela 'consultas'
CREATE TABLE IF NOT EXISTS consultas (
    id_consulta SERIAL PRIMARY KEY, -- ID do Agendamento
    id_pessoa_abrigada INTEGER NOT NULL, -- ID do Abrigado (FK para pessoas_abrigadas)
    id_servico INTEGER NOT NULL, -- FK para a tabela de servicos (para o "Tipo de agendamento")
    data_agendamento DATE NOT NULL,
    horario_agendamento TIME NOT NULL,
    profissional TEXT NOT NULL, -- Profissional/Instituição responsável
    status_agendamento VARCHAR(50) NOT NULL DEFAULT 'Agendado', -- Status do agendamento
    observacoes TEXT, -- Observações
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Para rastrear quando o agendamento foi feito

    -- Chaves Estrangeiras
    FOREIGN KEY (id_pessoa_abrigada) REFERENCES pessoas_abrigadas(id_pessoa_abrigada),
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico)
);

-- Dados de Exemplo para 'servicos' (Total de 10 registros)
INSERT INTO servicos (nome, descricao, responsavel) VALUES
('Consulta Médica', 'Atendimento com clínico geral', 'Dr. Carlos'),
('Atendimento Psicológico', 'Sessões de terapia', 'Dra. Ana'),
('Atendimento Jurídico', 'Orientação legal', 'Dr. Fernando'),
('Atendimento Social', 'Assistência social', 'Equipe Social'),
('Odontologia', 'Tratamento e prevenção dental', 'Dra. Paula'),
('Fisioterapia', 'Sessões de reabilitação', 'Dr. Roberto'),
('Nutrição', 'Orientação alimentar', 'Nutricionista Clara'),
('Corte de Cabelo', 'Serviço de barbearia/cabeleireiro', 'Salão Comunitário'),
('Apoio Educacional', 'Aulas de reforço e tutoria', 'Voluntários Educação'),
('Oficina de Artesanato', 'Atividades manuais e criativas', 'Monitora Lúcia');

-- Dados de Exemplo para 'pessoas_abrigadas' 
INSERT INTO pessoas_abrigadas (nome, data_nascimento, documento, sexo, data_entrada) VALUES
('João Silva', '1990-05-15', '12345678901', 'Masculino', '2023-01-10'),
('Maria Oliveira', '1985-11-20', '98765432109', 'Feminino', '2023-02-20'),
('Pedro Souza', '2000-03-01', '11223344556', 'Masculino', '2024-06-01'),
('Ana Costa', '1978-07-22', '22334455667', 'Feminino', '2023-03-15'),
('Carlos Pereira', '1995-09-03', '33445566778', 'Masculino', '2024-01-20'),
('Sofia Lima', '1965-01-30', '44556677889', 'Feminino', '2023-04-01'),
('Rafael Santos', '1992-04-12', '55667788990', 'Masculino', '2024-02-18'),
('Beatriz Rocha', '1988-02-28', '66778899001', 'Feminino', '2023-05-05'),
('Gabriel Alves', '2005-10-07', '77889900112', 'Masculino', '2024-03-10'),
('Laura Fernandes', '1970-12-01', '88990011223', 'Feminino', '2023-06-25');


-- Dados de Exemplo para 'consultas'
INSERT INTO consultas (id_pessoa_abrigada, id_servico, data_agendamento, horario_agendamento, profissional, status_agendamento, observacoes) VALUES
(1, 1, '2025-08-01', '10:00:00', 'Dr. Carlos', 'Agendado', 'Retorno para exames'),
(2, 2, '2025-08-02', '14:30:00', 'Dra. Ana', 'Agendado', 'Primeira sessão'),
(1, 3, '2025-08-03', '09:00:00', 'Dr. Fernando', 'Pendente', 'Dúvidas sobre documentação'),
(3, 1, '2025-08-05', '11:00:00', 'Dr. Carlos', 'Agendado', NULL),
(4, 4, '2025-08-06', '10:30:00', 'Equipe Social', 'Agendado', 'Avaliação inicial'),
(5, 5, '2025-08-07', '16:00:00', 'Dra. Paula', 'Agendado', 'Limpeza e avaliação'),
(6, 6, '2025-08-08', '09:30:00', 'Dr. Roberto', 'Remarcado', 'Sessão de fisioterapia'),
(7, 7, '2025-08-09', '13:00:00', 'Nutricionista Clara', 'Agendado', 'Plano alimentar'),
(8, 8, '2025-08-10', '15:00:00', 'Salão Comunitário', 'Agendado', 'Corte de cabelo'),
(9, 9, '2025-08-11', '10:00:00', 'Voluntários Educação', 'Agendado', 'Reforço em matemática');