-- Criação da Tabela 'doacoes_estoque'

CREATE TABLE doacoes_estoque (
    id_item_estoque SERIAL PRIMARY KEY,
    tipo_item VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade_atual INTEGER NOT NULL CHECK (quantidade_atual >= 0),
    unidade_medida VARCHAR(50),
    data_ultima_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de dados na tabela 'doacoes_estoque'
INSERT INTO doacoes_estoque (tipo_item, descricao, quantidade_atual, unidade_medida) VALUES
('Alimento', 'Arroz 5kg', 150, 'kg'),
('Roupa', 'Camisetas masculinas M', 80, 'unidade'),
('Higiene', 'Sabonete líquido 1L', 120, 'litro'),
('Alimento', 'Feijão 1kg', 200, 'kg'),
('Roupa', 'Calças jeans femininas', 60, 'unidade'),
('Higiene', 'Pasta de dente', 300, 'unidade'),
('Alimento', 'Óleo de cozinha', 90, 'litro'),
('Roupa', 'Casacos infantis', 45, 'unidade'),
('Higiene', 'Shampoo 500ml', 75, 'litro'),
('Alimento', 'Leite em pó 400g', 180, 'unidade'),
('Roupa', 'Meias unissex', 250, 'par'),
('Higiene', 'Escovas de dente', 280, 'unidade');