-- Cria o banco de dados CRM
CREATE DATABASE crm;

-- Usa o banco de dados CRM
USE crm;

-- Tabela de Usuário
CREATE TABLE usuario (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Tabela de Bate Papo
CREATE TABLE bate_papo (
    bate_papo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensagem TEXT,
    data_hora DATETIME
);

-- Tabela de Setor
CREATE TABLE setor (
    setor_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Tabela de Funcionário
CREATE TABLE funcionario (
    funcionario_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    setor_id INT
);

-- Tabela de Cliente
CREATE TABLE cliente (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Tabela de Motivo
CREATE TABLE motivo (
    motivo_id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL
);

-- Tabela de Chamada
CREATE TABLE chamada (
    chamada_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    funcionario_id INT,
    motivo_id INT,
    data_hora DATETIME
);

-- Tabela de Registro de Email
CREATE TABLE registro_email (
    registro_email_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    data_hora DATETIME,
    assunto VARCHAR(255) NOT NULL,
    corpo TEXT
);
