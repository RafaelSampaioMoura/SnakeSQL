import psycopg2
from psycopg2 import Error, connect
from utils import sql_functions

query_search = sql_functions.query_search
insertion_string = sql_functions.insertion_string
selection = sql_functions.selection
insertion = sql_functions.insertion
print_table_options = sql_functions.print_table_options
update = sql_functions.update

try:
    # Configuração da conexão com o banco de dados
    conn = connect(
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
        database='northwind'
    )

    # Cria um cursor para realizar as operações
    cursor = conn.cursor()

    # Imprime as informações do servidor
    print('Informações do servidor:\n')
    print(conn.get_dsn_parameters(), "\n")

    set_statements = '''
            SET statement_timeout = 0;
            SET lock_timeout = 0;
            SET client_encoding = 'UTF8';
            SET standard_conforming_strings = on;
            SET check_function_bodies = false;
            SET client_min_messages = warning;
            SET default_tablespace = '';
            SET default_with_oids = false;
        '''

    drop_tables = '''
        DROP TABLE IF EXISTS customer_customer_demo;
        DROP TABLE IF EXISTS customer_demographics;
        DROP TABLE IF EXISTS employee_territories;
        DROP TABLE IF EXISTS order_details;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS shippers;
        DROP TABLE IF EXISTS suppliers;
        DROP TABLE IF EXISTS territories;
        DROP TABLE IF EXISTS us_states;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS region;
        DROP TABLE IF EXISTS employees;
    '''

    create_table_usuario = '''
            CREATE TABLE usuario (
                id_usuario INT PRIMARY KEY,
                primeiro_nome VARCHAR(255) NOT NULL,
                ultimo_nome VARCHAR(255) NOT NULL,
                sobre_mim TEXT
             );
        '''
    
    create_table_contato = '''
            CREATE TABLE contato (
            id_contato INT PRIMARY KEY,
            id_usuario INT REFERENCES usuario (id_usuario),
            tipo VARCHAR(255) NOT NULL,
            valor VARCHAR(255) NOT NULL);
        '''
    
    create_table_formacao = '''
        CREATE TABLE formacao (
            id_formacao INT PRIMARY KEY,
            id_usuario INT REFERENCES usuario (id_usuario),
            curso VARCHAR(255),
            id_instituicao INT REFERENCES instituicao (id_instituicao),
            data_conclusao DATE,
            descricao TEXT
        );
    '''

    create_table_instituicao = '''
        CREATE TABLE instituicao (
            id_instituicao INT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            endereco INT REFERENCES endereco (id)
        );
    '''

    create_table_empresa = '''
        CREATE TABLE empresa (
            cnpj VARCHAR(255) PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            descricao TEXT NOT NULL,
            endereco INT REFERENCES endereco (id)
        );
    '''

    create_table_endereco = '''
        CREATE TABLE endereco (
            id INT PRIMARY KEY,
            rua VARCHAR(255) NOT NULL,
            bairro VARCHAR(255) NOT NULL,
            numero VARCHAR(255) NOT NULL,
            cidade VARCHAR(255) NOT NULL,
            estado VARCHAR(255) NOT NULL
        );
    '''

    create_table_cargo = '''
        CREATE TABLE cargo (
            id_cargo INT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cnpj VARCHAR(255) REFERENCES empresa (cnpj),
            salario FLOAT NOT NULL,
            descricao TEXT NOT NULL
        );
    '''

    create_table_experiencia = '''
        CREATE TABLE experiencia (
            id_experiencia INT PRIMARY KEY,
            id_usuario INT REFERENCES usuario (id_usuario),
            cnpj VARCHAR(255) REFERENCES empresa (cnpj),
            id_cargo INT REFERENCES cargo (id_cargo),
            descricao TEXT NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE
        );
    '''
    '''
    cursor.execute("SELECT version();")
    cursor.execute(set_statements)
    cursor.execute(drop_tables)
    cursor.execute(create_table_endereco)
    cursor.execute(create_table_usuario)
    cursor.execute(create_table_empresa)
    cursor.execute(create_table_contato)
    cursor.execute(create_table_cargo)
    cursor.execute(create_table_experiencia)
    cursor.execute(create_table_instituicao)
    cursor.execute(create_table_formacao)
    conn.commit()
    '''
    
    
    
    while 1:
        print("What would you like do to? (Input anything else to close)")
        options = '''
        1) Select
        2) Insert
        3) Update
        4) Query
        '''
        print(options)
        command = input()
        if command == '1':
            print('Which table would you like to query?')
            print_table_options()
            command = input()
            selection(command, cursor)
        elif command == '2':
            print("Which table would you like to insert a new item?")
            print_table_options()
            command = input()
            insertion(command, cursor)
        elif command == '3':
            print("Which table would you like to update?")
            print_table_options()
            command = input()
            update(command, cursor)
        elif command == '4':
            print('Which table would you like to query?')
            print_table_options()
            command = input()
            query_search(command, cursor)
        else:
            break


except (Exception, Error) as error:
    print("Deu cauê, irmão: ", error)
finally:
    if (conn):
        conn.commit()
        cursor.close()
        conn.close()
        print("Conexão terminada.")
