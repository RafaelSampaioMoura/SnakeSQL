--
-- PostgreSQL database dump - Sistema de Gestão de Vagas
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';
SET default_with_oids = false;

---
--- 1. Apagando as tabelas antigas (ordem reversa para evitar erro de chave estrangeira)
---
DROP TABLE IF EXISTS experiencia_profissional CASCADE;
DROP TABLE IF EXISTS formacao CASCADE;
DROP TABLE IF EXISTS contato CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS cargo CASCADE;
DROP TABLE IF EXISTS empresa CASCADE;
DROP TABLE IF EXISTS instituicao CASCADE;
DROP TABLE IF EXISTS endereco CASCADE;

---
--- 2. Criação das Tabelas (DDL)
---

CREATE TABLE endereco (
    id BIGSERIAL PRIMARY KEY,
    rua VARCHAR(255),
    bairro VARCHAR(100),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    cep VARCHAR(20)
);

CREATE TABLE cargo (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    empresa VARCHAR(100),
    salario FLOAT,
    descricao TEXT
);

CREATE TABLE empresa (
    id_empresa BIGSERIAL PRIMARY KEY,
    cnpj BIGINT UNIQUE NOT NULL,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    endereco BIGINT REFERENCES endereco(id)
);

CREATE TABLE instituicao (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    endereco BIGINT REFERENCES endereco(id)
);

CREATE TABLE usuario (
    id BIGSERIAL PRIMARY KEY,
    primeiro_nome VARCHAR(50) NOT NULL,
    ultimo_nome VARCHAR(50) NOT NULL,
    sobre_mim TEXT,
    contato BIGINT,
    endereco BIGINT REFERENCES endereco(id),
    formacao BIGINT
);

CREATE TABLE contato (
    id BIGSERIAL PRIMARY KEY,
    id_usuario BIGINT REFERENCES usuario(id),
    tipo VARCHAR(50),
    valor VARCHAR(150)
);

CREATE TABLE formacao (
    id BIGSERIAL PRIMARY KEY,
    id_usuario BIGINT REFERENCES usuario(id),
    curso VARCHAR(150),
    id_instituicao BIGINT REFERENCES instituicao(id),
    data_conclusao DATE,
    descricao TEXT
);

CREATE TABLE experiencia_profissional (
    id_experiencia BIGSERIAL PRIMARY KEY,
    id_usuario BIGINT REFERENCES usuario(id),
    id_empresa BIGINT REFERENCES empresa(id_empresa),
    id_cargo BIGINT REFERENCES cargo(id),
    data_inicio DATE,
    data_fim DATE,
    descricao TEXT
);

---
--- 3. Inserção de Dados (DML)
---

-- Endereços Base (Polos tecnológicos e universitários)
INSERT INTO endereco (id, rua, bairro, numero, complemento, cep) VALUES 
(1, 'Avenida Tenente Raimundo Rocha', 'Cidade Universitária', '1639', 'Campus Principal', '63048-080'),
(2, 'Rua São Pedro', 'Centro', '123', 'Sala 402', '63010-010'),
(3, 'Avenida Padre Cícero', 'Triângulo', '4040', 'Shopping Empresarial', '63041-140'),
(4, 'Rua da Inovação', 'Bairro Tecnológico', '99', 'Galpão B', '60000-000'),
(5, 'Rua dos Estudantes', 'Universitário', '55', 'Apto 101', '63050-222');

-- Cargos Disponíveis
INSERT INTO cargo (id, nome, empresa, salario, descricao) VALUES 
(1, 'Cientista de Dados Júnior', 'Inova Dados Ltda', 4500.00, 'Análise de dados com Python, Pandas e SQL. Criação de modelos preditivos.'),
(2, 'Desenvolvedor Backend (Python/Java)', 'Tech Soluções', 5200.00, 'Desenvolvimento de APIs RESTful, gerenciamento de banco de dados PostgreSQL.'),
(3, 'Estagiário em Banco de Dados', 'SoftSertão', 1200.00, 'Auxílio na modelagem de DER, normalização e queries SQL complexas.'),
(4, 'Engenheiro de Hardware', 'Mecatrônica Avançada', 7500.00, 'Manutenção e projeto de arquitetura de componentes de hardware corporativo.');

-- Empresas Contratantes
INSERT INTO empresa (id_empresa, cnpj, nome, descricao, endereco) VALUES 
(1, 12345678000199, 'Inova Dados Ltda', 'Consultoria focada em Big Data e Inteligência Artificial.', 3),
(2, 98765432000188, 'SoftSertão', 'Fábrica de software especializada em sistemas web e mobile.', 2),
(3, 45612378000177, 'Mecatrônica Avançada', 'Desenvolvimento de hardware e IoT industrial.', 4);

-- Instituições de Ensino
INSERT INTO instituicao (id, nome, endereco) VALUES 
(1, 'Universidade Federal do Cariri (UFCA)', 1),
(2, 'Instituto Federal (IFCE)', 2),
(3, 'Senai', 3);

-- Usuários (Candidatos)
INSERT INTO usuario (id, primeiro_nome, ultimo_nome, sobre_mim, contato, endereco, formacao) VALUES 
(1, 'Carlos', 'Eduardo', 'Estudante de Ciência da Computação apaixonado por estatística, álgebra linear e hardware.', NULL, 5, NULL),
(2, 'Ana', 'Bia', 'Desenvolvedora com experiência em C, Prolog e bases relacionais.', NULL, 2, NULL),
(3, 'Lucas', 'Mendes', 'Focado em front-end com Next.js, mas buscando migrar para Data Science.', NULL, 3, NULL);

-- Contatos dos Usuários
INSERT INTO contato (id, id_usuario, tipo, valor) VALUES 
(1, 1, 'Email', 'carlos.edu@email.com'),
(2, 1, 'LinkedIn', 'linkedin.com/in/carlosedu'),
(3, 2, 'Email', 'ana.bia.dev@email.com'),
(4, 3, 'Telefone', '(88) 99999-0000');

-- Formação Acadêmica
INSERT INTO formacao (id, id_usuario, curso, id_instituicao, data_conclusao, descricao) VALUES 
(1, 1, 'Bacharelado em Ciência da Computação', 1, '2026-12-20', 'Projeto de pesquisa focado em Ciência de Dados e Banco de Dados (3FN).'),
(2, 2, 'Tecnólogo em Redes de Computadores', 2, '2024-06-15', 'TCC sobre infraestrutura e segurança de hardware.'),
(3, 3, 'Sistemas de Informação', 1, '2025-12-10', 'Projeto integrador usando Firebase e Next.js.');

-- Experiência Profissional Anteriores
INSERT INTO experiencia_profissional (id_experiencia, id_usuario, id_empresa, id_cargo, data_inicio, data_fim, descricao) VALUES 
(1, 1, 2, 3, '2025-01-10', '2025-12-05', 'Estágio modelando bancos de dados relacionais e otimizando consultas SQL.'),
(2, 2, 1, 2, '2024-07-01', '2026-01-30', 'Desenvolvedora backend lidando com alta volumetria de dados e integrações.'),
(3, 3, 2, 2, '2026-02-01', '2026-03-20', 'Criação de páginas de registro e login com Next.js e Firebase.');

---
--- Fim do Dump
---