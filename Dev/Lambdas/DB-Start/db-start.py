import os
import json
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

with open('items.json') as f:
        json_data = json.load(f)

#print(json_data)

#Setting spl protected variables
dropItemsTableQuery = "DROP TABLE IF EXISTS items_table;"
dropStaffTableQuery = "DROP TABLE IF EXISTS staff_table;"
dropOrderTableQuery = "DROP TABLE IF EXISTS order_table;"
dropCustomerTableQuery = "DROP TABLE IF EXISTS customer_table;"
dropCategoryTableQuery = "DROP TABLE IF EXISTS category_table"
dropCatItemMapTableQuery = "DROP TABLE IF EXISTS category_item_map"
    
createCustomerTableQuery = "CREATE TABLE customer_table(customer_id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, surname_name VARCHAR(200), location VARCHAR(500) NOT NULL, email_address VARCHAR(500) NOT NULL, wallet DOUBLE PRECISION NOT NULL)"
createOrderTableQuery = "CREATE TABLE order_table(order_id SERIAL PRIMARY KEY, customer_id INT NOT NULL, item_id INT, date TIMESTAMP, paid_status BOOL NOT NULL, fulfilled_status BOOL NOT NULL, staff_id INT NOT NULL)"
createStaffTableQuery = "CREATE TABLE staff_table(staff_id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, surname_name VARCHAR(200) NOT NULL, staff_number INT NOT NULL UNIQUE, store_location VARCHAR(200), email_address VARCHAR(500))"
createItemTableQuery = "CREATE TABLE items_table(item_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, price DOUBLE PRECISION NOT NULL, description TEXT, kcals DOUBLE PRECISION, fat DOUBLE PRECISION, carbs DOUBLE PRECISION, sugar DOUBLE PRECISION, fiber DOUBLE PRECISION, salt DOUBLE PRECISION, isActive BOOL)"
createCategoryTableQuery = "CREATE TABLE category_table(category_id SERIAL PRIMARY KEY, name VARCHAR(100))"

load_dotenv()

# Make db connection
try:
    connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"))
    
#Cursor helps to perform database operations
    cursor = connection.cursor()

#DROP EXISTING TABLES IF THEY EXISTS

    cursor.execute(dropCatItemMapTableQuery)
    cursor.execute(dropOrderTableQuery)
    cursor.execute(dropStaffTableQuery)
    cursor.execute(dropCustomerTableQuery)
    cursor.execute(dropItemsTableQuery)
    cursor.execute(dropCategoryTableQuery)

#DROP AND CREATE SCHEMA
    cursor.execute("DROP SCHEMA IF EXISTS aks")
    cursor.execute("CREATE SCHEMA aks")

# CREATE INITIAL TABLES
    cursor.execute(createOrderTableQuery)
    cursor.execute(createStaffTableQuery)
    cursor.execute(createCustomerTableQuery)
    cursor.execute(createItemTableQuery)
    cursor.execute(createCategoryTableQuery)

#CREATE MAP TABLES
    #cursor.execute("CREATE TABLE category_item_map(id INT NOT NULL PRIMARY KEY, category_id INT NOT NULL REFERENCES category_table(category_id), item_id INT NOT NULL REFERENCES items_table(item_id))")


#INSERT TABLE DATA
    for item in json_data:
        name = item['name']
        price = item['price']
        description =item['description']
        kcals = item['kcals']
        carbs = item['carbs']
        sugar = item['sugar']
        fiber = item['fiber']
        salt =item['salt']
        isActive = item['isActive']

        cursor.execute("""INSERT INTO items_table(name, price, description, kcals, carbs, sugar, fiber, salt, isActive) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (name, price, description, kcals, carbs, sugar, fiber, salt, isActive))

    connection.commit()
    cursor.close

    print("postgresSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.execute("SELECT * FROM items_table")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        connection.close()
        print("PostgreSQ: connection is closed")
