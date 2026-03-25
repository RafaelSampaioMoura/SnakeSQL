import psycopg2
from psycopg2 import Error, connect
from utils import sql_functions

query_search = sql_functions.query_search
insertion_string = sql_functions.insertion_string
selection = sql_functions.selection
insertion = sql_functions.insertion
print_table_options = sql_functions.print_table_options

try:
    # Configuração da conexão com o banco de dados
    conn = connect(
        user='postgres',
        password='postgres',
        host='localhost',
        port='5433',
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

    create_table_categories = '''
            CREATE TABLE categories (
            category_id smallint NOT NULL,
            category_name character varying(15) NOT NULL,
            description text,
            picture bytea );
        '''
    
    create_table_customer_customer_demo = '''
            CREATE TABLE customer_customer_demo (
            customer_id character varying(5) NOT NULL,
            customer_type_id character varying(5) NOT NULL );
        '''
    
    create_table_customers = '''
        CREATE TABLE customers (
            customer_id character varying(5) NOT NULL,
            company_name character varying(40) NOT NULL,
            contact_name character varying(30),
            contact_title character varying(30),
            address character varying(60),
            city character varying(15),
            region character varying(15),
            postal_code character varying(10),
            country character varying(15),
            phone character varying(24),
            fax character varying(24)
        );
    '''

    create_table_employees = '''
            CREATE TABLE employees (
            employee_id smallint NOT NULL,
            last_name character varying(20) NOT NULL,
            first_name character varying(10) NOT NULL,
            title character varying(30),
            title_of_courtesy character varying(25),
            birth_date date,
            hire_date date,
            address character varying(60),
            city character varying(15),
            region character varying(15),
            postal_code character varying(10),
            country character varying(15),
            home_phone character varying(24),
            extension character varying(4),
            photo bytea,
            notes text,
            reports_to smallint,
            photo_path character varying(255)
        );
    '''

    create_table_employee_territories = '''
        CREATE TABLE employee_territories (
        employee_id smallint NOT NULL,
        territory_id character varying(20) NOT NULL );
    '''

    create_table_order_details = '''
        CREATE TABLE order_details (
            order_id smallint NOT NULL,
            product_id smallint NOT NULL,
            unit_price real NOT NULL,
            quantity smallint NOT NULL,
            discount real NOT NULL );
    '''

    create_table_orders = '''
        CREATE TABLE orders (
            order_id smallint NOT NULL,
            customer_id character varying(5),
            employee_id smallint,
            order_date date,
            required_date date,
            shipped_date date,
            ship_via smallint,
            freight real,
            ship_name character varying(40),
            ship_address character varying(60),
            ship_city character varying(15),
            ship_region character varying(15),
            ship_postal_code character varying(10),
            ship_country character varying(15) );
    '''

    create_table_products = '''
        CREATE TABLE products (
            product_id smallint NOT NULL,
            product_name character varying(40) NOT NULL,
            supplier_id smallint,
            category_id smallint,
            quantity_per_unit character varying(20),
            unit_price real,
            units_in_stock smallint,
            units_on_order smallint,
            reorder_level smallint,
            discontinued integer NOT NULL );
    '''

    cursor.execute("SELECT version();")
    cursor.execute(set_statements)
    cursor.execute(drop_tables)
    cursor.execute(create_table_categories)
    cursor.execute(create_table_customer_customer_demo)
    cursor.execute(create_table_customers)
    cursor.execute(create_table_employees)
    cursor.execute(create_table_employee_territories)
    cursor.execute(create_table_order_details)
    cursor.execute(create_table_orders)
    cursor.execute(create_table_products)
    conn.commit()

    insert_categories = '''
        INSERT INTO categories VALUES (1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales', 'x');
        INSERT INTO categories VALUES (2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings', 'x');
        INSERT INTO categories VALUES (3, 'Confections', 'Desserts, candies, and sweet breads', 'x');
        INSERT INTO categories VALUES (4, 'Dairy Products', 'Cheeses', 'x');
        INSERT INTO categories VALUES (5, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal', 'x');
        INSERT INTO categories VALUES (6, 'Meat/Poultry', 'Prepared meats', 'x');
        INSERT INTO categories VALUES (7, 'Produce', 'Dried fruit and bean curd', 'x');
        INSERT INTO categories VALUES (8, 'Seafood', 'Seaweed and fish', 'x');
    '''

    insert_costumers = '''
        INSERT INTO customers VALUES ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany', '030-0074321', '030-0076545');
        INSERT INTO customers VALUES ('ANATR', 'Ana Trujillo Emparedados y helados', 'Ana Trujillo', 'Owner', 'Avda. de la Constitución 2222', 'México D.F.', NULL, '05021', 'Mexico', '(5) 555-4729', '(5) 555-3745');
        INSERT INTO customers VALUES ('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Owner', 'Mataderos  2312', 'México D.F.', NULL, '05023', 'Mexico', '(5) 555-3932', NULL);
        INSERT INTO customers VALUES ('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', NULL, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750');
        INSERT INTO customers VALUES ('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Berguvsvägen  8', 'Luleå', NULL, 'S-958 22', 'Sweden', '0921-12 34 65', '0921-12 34 67');
        INSERT INTO customers VALUES ('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Sales Representative', 'Forsterstr. 57', 'Mannheim', NULL, '68306', 'Germany', '0621-08460', '0621-08924');
        INSERT INTO customers VALUES ('BLONP', 'Blondesddsl père et fils', 'Frédérique Citeaux', 'Marketing Manager', '24, place Kléber', 'Strasbourg', NULL, '67000', 'France', '88.60.15.31', '88.60.15.32');
        INSERT INTO customers VALUES ('BOLID', 'Bólido Comidas preparadas', 'Martín Sommer', 'Owner', 'C/ Araquil, 67', 'Madrid', NULL, '28023', 'Spain', '(91) 555 22 82', '(91) 555 91 99');
        INSERT INTO customers VALUES ('BONAP', 'Bon app', 'Laurence Lebihan', 'Owner', '12, rue des Bouchers', 'Marseille', NULL, '13008', 'France', '91.24.45.40', '91.24.45.41');
        INSERT INTO customers VALUES ('BOTTM', 'Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Accounting Manager', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada', '(604) 555-4729', '(604) 555-3745');
        INSERT INTO customers VALUES ('BSBEV', 'B''s Beverages', 'Victoria Ashworth', 'Sales Representative', 'Fauntleroy Circus', 'London', NULL, 'EC2 5NT', 'UK', '(171) 555-1212', NULL);
    '''

    insert_employees = '''
        INSERT INTO employees VALUES (1, 'Davolio', 'Nancy', 'Sales Representative', 'Ms.', '1948-12-08', '1992-05-01', '507 - 20th Ave. E.\nApt. 2A', 'Seattle', 'WA', '98122', 'USA', '(206) 555-9857', '5467', 'x', 'Education includes a BA in psychology from Colorado State University in 1970.  She also completed The Art of the Cold Call.  Nancy is a member of Toastmasters International.', 2, 'http://accweb/emmployees/davolio.bmp');
        INSERT INTO employees VALUES (2, 'Fuller', 'Andrew', 'Vice President, Sales', 'Dr.', '1952-02-19', '1992-08-14', '908 W. Capital Way', 'Tacoma', 'WA', '98401', 'USA', '(206) 555-9482', '3457', 'x', 'Andrew received his BTS commercial in 1974 and a Ph.D. in international marketing from the University of Dallas in 1981.  He is fluent in French and Italian and reads German.  He joined the company as a sales representative, was promoted to sales manager in January 1992 and to vice president of sales in March 1993.  Andrew is a member of the Sales Management Roundtable, the Seattle Chamber of Commerce, and the Pacific Rim Importers Association.', NULL, 'http://accweb/emmployees/fuller.bmp');
        INSERT INTO employees VALUES (3, 'Leverling', 'Janet', 'Sales Representative', 'Ms.', '1963-08-30', '1992-04-01', '722 Moss Bay Blvd.', 'Kirkland', 'WA', '98033', 'USA', '(206) 555-3412', '3355', 'x', 'Janet has a BS degree in chemistry from Boston College (1984).  She has also completed a certificate program in food retailing management.  Janet was hired as a sales associate in 1991 and promoted to sales representative in February 1992.', 2, 'http://accweb/emmployees/leverling.bmp');
        INSERT INTO employees VALUES (4, 'Peacock', 'Margaret', 'Sales Representative', 'Mrs.', '1937-09-19', '1993-05-03', '4110 Old Redmond Rd.', 'Redmond', 'WA', '98052', 'USA', '(206) 555-8122', '5176', 'x', 'Margaret holds a BA in English literature from Concordia College (1958) and an MA from the American Institute of Culinary Arts (1966).  She was assigned to the London office temporarily from July through November 1992.', 2, 'http://accweb/emmployees/peacock.bmp');
        INSERT INTO employees VALUES (5, 'Buchanan', 'Steven', 'Sales Manager', 'Mr.', '1955-03-04', '1993-10-17', '14 Garrett Hill', 'London', NULL, 'SW1 8JR', 'UK', '(71) 555-4848', '3453', 'x', 'Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses Successful Telemarketing and International Sales Management.  He is fluent in French.', 2, 'http://accweb/emmployees/buchanan.bmp');
        INSERT INTO employees VALUES (6, 'Suyama', 'Michael', 'Sales Representative', 'Mr.', '1963-07-02', '1993-10-17', 'Coventry House\nMiner Rd.', 'London', NULL, 'EC2 7JR', 'UK', '(71) 555-7773', '428', 'x', 'Michael is a graduate of Sussex University (MA, economics, 1983) and the University of California at Los Angeles (MBA, marketing, 1986).  He has also taken the courses Multi-Cultural Selling and Time Management for the Sales Professional.  He is fluent in Japanese and can read and write French, Portuguese, and Spanish.', 5, 'http://accweb/emmployees/davolio.bmp');
        INSERT INTO employees VALUES (7, 'King', 'Robert', 'Sales Representative', 'Mr.', '1960-05-29', '1994-01-02', 'Edgeham Hollow\nWinchester Way', 'London', NULL, 'RG1 9SP', 'UK', '(71) 555-5598', '465', 'x', 'Robert King served in the Peace Corps and traveled extensively before completing his degree in English at the University of Michigan in 1992, the year he joined the company.  After completing a course entitled Selling in Europe, he was transferred to the London office in March 1993.', 5, 'http://accweb/emmployees/davolio.bmp');
        INSERT INTO employees VALUES (8, 'Callahan', 'Laura', 'Inside Sales Coordinator', 'Ms.', '1958-01-09', '1994-03-05', '4726 - 11th Ave. N.E.', 'Seattle', 'WA', '98105', 'USA', '(206) 555-1189', '2344', 'x', 'Laura received a BA in psychology from the University of Washington.  She has also completed a course in business French.  She reads and writes French.', 2, 'http://accweb/emmployees/davolio.bmp');
        INSERT INTO employees VALUES (9, 'Dodsworth', 'Anne', 'Sales Representative', 'Ms.', '1966-01-27', '1994-11-15', '7 Houndstooth Rd.', 'London', NULL, 'WG2 7LT', 'UK', '(71) 555-4444', '452', 'x', 'Anne has a BA degree in English from St. Lawrence College.  She is fluent in French and German.', 5, 'http://accweb/emmployees/davolio.bmp');
    '''

    insert_orders = '''
        INSERT INTO orders VALUES (10248, 'VINET', 5, '1996-07-04', '1996-08-01', '1996-07-16', 3, 32.3800011, 'Vins et alcools Chevalier', '59 rue de l''Abbaye', 'Reims', NULL, '51100', 'France');
        INSERT INTO orders VALUES (10249, 'TOMSP', 6, '1996-07-05', '1996-08-16', '1996-07-10', 1, 11.6099997, 'Toms Spezialitäten', 'Luisenstr. 48', 'Münster', NULL, '44087', 'Germany');
        INSERT INTO orders VALUES (10250, 'HANAR', 4, '1996-07-08', '1996-08-05', '1996-07-12', 2, 65.8300018, 'Hanari Carnes', 'Rua do Paço, 67', 'Rio de Janeiro', 'RJ', '05454-876', 'Brazil');
        INSERT INTO orders VALUES (10251, 'VICTE', 3, '1996-07-08', '1996-08-05', '1996-07-15', 1, 41.3400002, 'Victuailles en stock', '2, rue du Commerce', 'Lyon', NULL, '69004', 'France');
        INSERT INTO orders VALUES (10252, 'SUPRD', 4, '1996-07-09', '1996-08-06', '1996-07-11', 2, 51.2999992, 'Suprêmes délices', 'Boulevard Tirou, 255', 'Charleroi', NULL, 'B-6000', 'Belgium');
        INSERT INTO orders VALUES (10253, 'HANAR', 3, '1996-07-10', '1996-07-24', '1996-07-16', 2, 58.1699982, 'Hanari Carnes', 'Rua do Paço, 67', 'Rio de Janeiro', 'RJ', '05454-876', 'Brazil');
        INSERT INTO orders VALUES (10254, 'CHOPS', 5, '1996-07-11', '1996-08-08', '1996-07-23', 2, 22.9799995, 'Chop-suey Chinese', 'Hauptstr. 31', 'Bern', NULL, '3012', 'Switzerland');
        INSERT INTO orders VALUES (10255, 'RICSU', 9, '1996-07-12', '1996-08-09', '1996-07-15', 3, 148.330002, 'Richter Supermarkt', 'Starenweg 5', 'Genève', NULL, '1204', 'Switzerland');
        INSERT INTO orders VALUES (10256, 'WELLI', 3, '1996-07-15', '1996-08-12', '1996-07-17', 2, 13.9700003, 'Wellington Importadora', 'Rua do Mercado, 12', 'Resende', 'SP', '08737-363', 'Brazil');
        INSERT INTO orders VALUES (10257, 'HILAA', 4, '1996-07-16', '1996-08-13', '1996-07-22', 3, 81.9100037, 'HILARION-Abastos', 'Carrera 22 con Ave. Carlos Soublette #8-35', 'San Cristóbal', 'Táchira', '5022', 'Venezuela');
    '''
    
    insert_products = '''
        INSERT INTO products VALUES (1, 'Chai', 8, 1, '10 boxes x 30 bags', 18, 39, 0, 10, 1);
        INSERT INTO products VALUES (2, 'Chang', 1, 1, '24 - 12 oz bottles', 19, 17, 40, 25, 1);
        INSERT INTO products VALUES (3, 'Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10, 13, 70, 25, 0);
        INSERT INTO products VALUES (4, 'Chef Anton''s Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22, 53, 0, 0, 0);
        INSERT INTO products VALUES (5, 'Chef Anton''s Gumbo Mix', 2, 2, '36 boxes', 21.3500004, 0, 0, 0, 1);
        INSERT INTO products VALUES (6, 'Grandma''s Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25, 120, 0, 25, 0);
        INSERT INTO products VALUES (7, 'Uncle Bob''s Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30, 15, 0, 10, 0);
        INSERT INTO products VALUES (8, 'Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40, 6, 0, 0, 0);
        INSERT INTO products VALUES (9, 'Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97, 29, 0, 0, 1);
        INSERT INTO products VALUES (10, 'Ikura', 4, 8, '12 - 200 ml jars', 31, 31, 0, 0, 0);
    '''
    
    cursor.execute(insert_categories)
    cursor.execute(insert_costumers)
    cursor.execute(insert_employees)
    cursor.execute(insert_orders)
    cursor.execute(insert_products)
    conn.commit()

    
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
        cursor.close()
        conn.close()
        print("Conexão terminada.")
