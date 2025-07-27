-- Criação da tabela
CREATE TABLE IF NOT EXISTS pessoa_abrigada (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    genero TEXT,
    data_nascimento DATE,
    documento TEXT,
    status TEXT,
    condicoes_saude TEXT
);

-- Inserção de 10 abrigados
INSERT INTO pessoa_abrigada (nome, genero, data_nascimento, documento, status, condicoes_saude) VALUES
('João Silva', 'Masculino', '1980-03-12', '12345678900', 'abrigado', 'diabetes'),
('Maria Oliveira', 'Feminino', '1975-05-10', '98765432100', 'abrigado', 'hipertensão'),
('Carlos Pereira', 'Masculino', '1968-07-21', '11122233344', 'encaminhado', 'nenhuma'),
('Ana Lima', 'Feminino', '1985-01-22', '22233344455', 'abrigado', 'deficiência visual'),
('Pedro Souza', 'Masculino', '1990-12-01', '33344455566', 'saiu', 'epilepsia'),
('Juliana Rocha', 'Feminino', '2000-08-30', '44455566677', 'abrigado', 'diabetes'),
('Rafael Duarte', 'Masculino', '1982-04-17', '55566677788', 'abrigado', 'nenhuma'),
('Luciana Costa', 'Feminino', '1979-06-05', '66677788899', 'encaminhado', 'hipertensão'),
('Bruno Marques', 'Masculino', '1995-11-09', '77788899900', 'saiu', 'deficiência auditiva'),
('Camila Nunes', 'Feminino', '1988-02-28', '88899900011', 'abrigado', 'diabetes');