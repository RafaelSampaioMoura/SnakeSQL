import psycopg2
from psycopg2 import Error

# Mantendo as importações do seu utilitário para o menu do terminal funcionar
try:
    from utils import sql_functions
    query_search = sql_functions.query_search
    selection = sql_functions.selection
    insertion = sql_functions.insertion
    print_table_options = sql_functions.print_table_options
except ImportError:
    print("Aviso: Módulo 'utils.sql_functions' não encontrado. O menu interativo pode falhar, mas o Streamlit funcionará.")

def abrir_conexao():
    """Estabelece e retorna a conexão com o banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        user='postgres',
        password='postgres', 
        host='localhost',
        port='5433',        
        database='northwind' 
    )
    return conn

def inicializar_banco(cursor, conn):
    """Apaga as tabelas antigas, cria a nova estrutura do DER e insere dados iniciais."""
    print("Iniciando a reconstrução do banco de dados...")

    # 1. DROP TABLES (Ordem reversa de dependência)
    drop_tables = '''
        DROP TABLE IF EXISTS experiencia_profissional CASCADE;
        DROP TABLE IF EXISTS formacao CASCADE;
        DROP TABLE IF EXISTS contato CASCADE;
        DROP TABLE IF EXISTS usuario CASCADE;
        DROP TABLE IF EXISTS cargo CASCADE;
        DROP TABLE IF EXISTS empresa CASCADE;
        DROP TABLE IF EXISTS instituicao CASCADE;
        DROP TABLE IF EXISTS endereco CASCADE;
    '''
    cursor.execute(drop_tables)

    # 2. CREATE TABLES
    create_tables = '''
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
    '''
    cursor.execute(create_tables)

    # 3. INSERT DATA
    insert_data = '''
        -- Endereços
        INSERT INTO endereco (rua, bairro, numero, complemento, cep) VALUES 
        ('Avenida Tenente Raimundo Rocha', 'Cidade Universitária', '1639', 'Campus Principal', '63048-080'),
        ('Rua São Pedro', 'Centro', '123', 'Sala 402', '63010-010'),
        ('Rua da Inovação', 'Bairro Tecnológico', '99', 'Galpão B', '60000-000');

        -- Cargos
        INSERT INTO cargo (nome, empresa, salario, descricao) VALUES 
        ('Cientista de Dados Júnior', 'Inova Dados Ltda', 4500.00, 'Análise de dados com Python e SQL. Modelagem estatística e álgebra linear aplicadas.'),
        ('Desenvolvedor Frontend Web', 'Tech Soluções', 3800.00, 'Criação de interfaces responsivas e páginas de login utilizando Next.js e Firebase.'),
        ('Engenheiro de Hardware', 'Mecatrônica Avançada', 7500.00, 'Prototipagem e arquitetura de componentes físicos em baixo nível (C).');

        -- Empresas
        INSERT INTO empresa (cnpj, nome, descricao, endereco) VALUES 
        (12345678000199, 'Inova Dados Ltda', 'Consultoria focada em Data Science.', 3),
        (98765432000188, 'Tech Soluções', 'Sistemas web de alta performance.', 2);

        -- Instituições
        INSERT INTO instituicao (nome, endereco) VALUES 
        ('Universidade Federal do Cariri (UFCA)', 1),
        ('Instituto Federal (IFCE)', 2);

        -- Usuários
        INSERT INTO usuario (primeiro_nome, ultimo_nome, sobre_mim, endereco) VALUES 
        ('Isaac', 'Leite', 'Estudante de Ciência da Computação com interesse em Data Science, Python e arquitetura de hardware.', 1),
        ('Maria', 'Silva', 'Desenvolvedora Fullstack com foco em Next.js e bancos relacionais.', 2);

        -- Contatos
        INSERT INTO contato (id_usuario, tipo, valor) VALUES 
        (1, 'Email', 'isaac.cc@ufca.edu.br'),
        (1, 'GitHub', 'github.com/isaac-leite'),
        (2, 'LinkedIn', 'linkedin.com/in/mariasilva');

        -- Formação
        INSERT INTO formacao (id_usuario, curso, id_instituicao, data_conclusao, descricao) VALUES 
        (1, 'Bacharelado em Ciência da Computação', 1, '2026-12-20', 'Projeto de Iniciação Científica na área de Ciência de Dados e Banco de Dados (DER, 3FN).'),
        (2, 'Tecnólogo em Sistemas de Informação', 2, '2024-06-15', 'TCC com integração de autenticação via Firebase.');

        -- Experiência Profissional
        INSERT INTO experiencia_profissional (id_usuario, id_empresa, id_cargo, data_inicio, data_fim, descricao) VALUES 
        (1, 1, 1, '2025-08-01', '2025-12-20', 'Modelagem de dados relacionais e otimização de consultas.'),
        (2, 2, 2, '2026-02-01', '2026-03-24', 'Implementação de tela de registro/login e dashboard administrativo.');
    '''
    cursor.execute(insert_data)
    
    conn.commit()
    print("Banco de dados reconstruído e populado com sucesso!")


# O bloco abaixo só roda se o arquivo for executado diretamente no terminal
if __name__ == '__main__':
    try:
        conn = abrir_conexao()
        cursor = conn.cursor()

        print("Conectado ao PostgreSQL!\n")

        while True:
            print("\nO que você deseja fazer?")
            options = '''
            1) Resetar Banco (Recriar Tabelas do DER e Inserir Dados Base)
            2) Select (Menu Antigo)
            3) Insert (Menu Antigo)
            4) Update (Menu Antigo)
            5) Sair
            '''
            print(options)
            command = input("Escolha uma opção: ")

            if command == '1':
                inicializar_banco(cursor, conn)
            elif command == '2':
                print('Qual tabela você deseja consultar?')
                print_table_options()
                cmd_table = input()
                selection(cmd_table, cursor)
            elif command == '3':
                print("Qual tabela você deseja inserir um novo item?")
                print_table_options()
                cmd_table = input()
                insertion(cmd_table, cursor)
            elif command == '4':
                print("Qual tabela você deseja atualizar?")
                print_table_options()
                cmd_table = input()
                # Aqui iria a lógica antiga de update
            elif command == '5':
                break
            else:
                print("Opção inválida.")

    except (Exception, Error) as error:
        print("Deu cauê, irmão: ", error)
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("Conexão terminada.")