# Dicionário com todas as tabelas presentes no banco de dados
this_tables = {
    "1":"categories",
    "2":"customers",
    "3":"employees",
    "4":"orders",
    "5":"products"
}

def query_search(table_name, cursor):
    query_string = ""
    # String para pegar o nome das colunas da tabela
    query_collumns = f'''
        SELECT 
            table_name, 
            column_name, 
            data_type 
        FROM 
            information_schema.columns
        WHERE 
            table_name = '{this_tables[table_name]}';
    '''
    
    cursor.execute(query_collumns)
    collumns = cursor.fetchall()
    length = len(collumns)

    print("What collumn would you like to query?")
    for x in range(length):
        print(f"{x + 1}) {collumns[x][1]}")
    print(f"{length + 1}) All")
    input_collumn = int(input())

    print("What is your condition?")
    condition = input()

    query_string = f"SELECT {collumns[input_collumn - 1][1]} FROM {this_tables[table_name]} WHERE {condition};"

    cursor.execute(query_string)
    result = cursor.fetchall()
    for item in result:
        print(item)

def insertion_string(table_name, table_collumns):
    # Inicia a string de inserção com o nome da tabela pego dos argumentos da função
    # Ex.: INSERT INTO products 
    insert_str = f"INSERT INTO {table_name} "
    length = len(table_collumns)

    # Continua a construção a construção da string adicionando as colunas
    # Ex.: INSERT INTO products (product_id, product_name, product_price)
    insert_str = insert_str + "("
    for x in range(length - 1):
        insert_str = insert_str + f"{table_collumns[x]}, "
    
    # Adiciona à string os literais %s que irão ser substituídos pelos valores colocados pelo
    # usuário
    # Ex.: INSERT INTO products (product_id, product_name, product_price) VALUES (%s, %s, %s);
    insert_str = insert_str + f"{table_collumns[length-1]}) VALUES ("
    for x in range(length - 1):
        insert_str = insert_str + "%s, "
    insert_str = insert_str + "%s);"

    # Retorna a string de inserção finalizada para query
    return insert_str

# função que cuida da busca de informações das tabelas
def selection(table_name, cursor):
    query_string = ""
    # String para pegar o nome das colunas da tabela
    query_collumns = f'''
        SELECT 
            table_name, 
            column_name, 
            data_type 
        FROM 
            information_schema.columns
        WHERE 
            table_name = '{this_tables[table_name]}';
    '''
    
    cursor.execute(query_collumns)
    collumns = cursor.fetchall()
    length = len(collumns)

    print("What collumn would you like to query?")
    for x in range(length):
        print(f"{x + 1}) {collumns[x][1]}")
    print(f"{length + 1}) All")

    input_collumn = int(input())

    if (input_collumn != (length + 1)):
        query_string = f"SELECT {collumns[input_collumn - 1][1]} FROM {this_tables[table_name]};"
    else:
        query_string = f"SELECT * FROM {this_tables[table_name]};"
    cursor.execute(query_string)
    record = cursor.fetchall()
    for item in record:
        print(item)

# função que cuida da inserção de novos items nas tabelas
def insertion(table_name, cursor):
    # Query enviada para o banco de dados para pegar o nome e o tipo de dado das colunas
    query_collumns = f'''
        SELECT 
            table_name, 
            column_name, 
            data_type 
        FROM 
            information_schema.columns
        WHERE 
            table_name = '{this_tables[table_name]}';
    '''
    
    # Exibe o nome e os tipos de dados das colunas para que o burro do usuário não coloque nada errado
    print("You'll have to obey the following schema:\nCOLLUMN_NAME ==+== TYPE:")
    cursor.execute(query_collumns)
    record = cursor.fetchall()
    table_collumns = []
    for item in record:
        print(f"{item[1]} ==+== {item[2]}")
        # Aproveita a deixa e pega o nome das colunas para a string de inserção
        table_collumns.append(item[1])
    
    table_tuple = tuple(table_collumns)
    insert_str = insertion_string(this_tables[table_name], table_tuple)
    #print(insert_str)
    
    # Pede para o usuário colocar, em ordem, as informações de cada coluna do novo item da tabela
    size = len(record)
    for_insertion = []
    for x in range(size):
        print(f"Insert {record[x][1]} with type of {record[x][2]}")
        user_input = input()
        for_insertion.append(user_input)
    cursor.execute(insert_str, for_insertion)
    record = cursor.fetchone
    print(record)

def update(table_name, cursor):
    return

# imprime ao usuário quais as tabelas ele tem como selecionar
def print_table_options():
    option_tables = '''
    1) Categories
    2) Custumers
    3) Employees
    4) Orders
    5) Products
    '''
    print(option_tables)
