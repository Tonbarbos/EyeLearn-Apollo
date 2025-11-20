-- ============================================================================
-- Banco de Dados: EyeLearnDB
-- Descrição: Schema para aplicação de avaliação neurocognitiva via Eye Tracking
-- SGBD: MySQL 8.0+ (Requerido para colunas VIRTUAL)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS EyeLearnDB;
USE EyeLearnDB;

-- ----------------------------------------------------------------------------
-- Tabela: Diagnosticos
-- Armazena os padrões de classificação pré-definidos pelo sistema.
-- ----------------------------------------------------------------------------
CREATE TABLE Diagnosticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    texto_diagnostico TEXT NOT NULL,
    padrao_visual VARCHAR(255) -- Identificador interno do padrão visual
);

-- Carga inicial de diagnósticos padrão
INSERT INTO Diagnosticos (titulo, texto_diagnostico, padrao_visual) VALUES
('Padrão Típico', 'Rastreamento ocular dentro da normalidade para a faixa etária.', 'foco_distribuido'),
('Atenção Dispersa', 'Dificuldade em manter foco em pontos chave por períodos sustentados.', 'foco_erratico'),
('Possível TDAH', 'Indicadores visuais compatíveis com TDAH. Recomenda-se avaliação clínica.', 'foco_rapido_alternado'),
('Possível Dislexia', 'Fixação prolongada ou regressão frequente durante a leitura.', 'fixacao_irregular');

-- ----------------------------------------------------------------------------
-- Tabela: Alunos
-- Cadastro base dos estudantes. A idade é calculada dinamicamente.
-- ----------------------------------------------------------------------------
CREATE TABLE Alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Dados Pessoais
    nomeCompleto VARCHAR(255) NOT NULL,
    dataNascimento DATE NOT NULL,
    genero ENUM('Masculino', 'Feminino', 'Outro', 'Prefiro não dizer'),

    -- Dados Escolares
    nomeEscola VARCHAR(255),
    serieEscola VARCHAR(50),
    turma VARCHAR(50),

    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Tabela: Sessoes
-- Histórico de avaliações. Permite múltiplos testes para o mesmo aluno.
-- ----------------------------------------------------------------------------
CREATE TABLE Sessoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    diagnostico_id INT,

    -- Resultados
    caminhoMapaCalor VARCHAR(500), -- Caminho relativo para o arquivo
    observacoes TEXT,              -- Notas adicionais

    pontuacao_final INT DEFAULT 0,
    tempo_segundos INT DEFAULT 0,
    erros_count INT DEFAULT 0,

    data_sessao DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    FOREIGN KEY (aluno_id) REFERENCES Alunos(id) ON DELETE CASCADE,
    FOREIGN KEY (diagnostico_id) REFERENCES Diagnosticos(id) ON DELETE SET NULL
);