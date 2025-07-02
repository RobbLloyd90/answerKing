import os
import json
import psycopg2
from psycopg2 import Error
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# SAMPLE DATA

json_data = [
  {
    "name": "Filter Coffee",
    "price": 2.95,
    "description": "Single origin arabica beans from kenya and roasted by London's own Square Mile Coffee.",
    "category": "Drink",
    "dietary requirement": "Vegan",
    "kcals": 1,
    "fat": 0,
    "carbs": 0,
    "sugar": 0,
    "fiber": 0,
    "salt": 0,
    "isActive": True
  },
  {
    "name": "Fresh Orange Juice",
    "price": 3.50,
    "description": "Freshly squeezed British oranges for a tangy, refreshing drink.",
    "category": "Drink",
    "dietary requirement": "Vegan",
    "kcals": 45,
    "fat": 0,
    "carbs": 11,
    "sugar": 9,
    "fiber": 2,
    "salt": 0,
    "isActive": True
  },
  {
    "name": "Apple Juice",
    "price": 3.50,
    "description": "Pressed from juicy British apples, naturally sweet and crisp.",
    "category": "Drink",
    "dietary requirement": "Vegan",
    "kcals": 40,
    "fat": 0,
    "carbs": 10,
    "sugar": 8,
    "fiber": 1,
    "salt": 0,
    "isActive": True
  },
  {
    "name": "Bottled Water",
    "price": 1.50,
    "description": "Bottled water sourced from the lakes of the Lake District.",
    "category": "Drink",
    "dietary requirement": "Vegan",
    "kcals": 0,
    "fat": 0,
    "carbs": 0,
    "sugar": 0,
    "fiber": 0,
    "salt": 0,
    "isActive": True
  },
  {
    "name": "British Lamb Hotpot",
    "price": 14.99,
    "description": "Slow-cooked British lamb with root vegetables, topped with buttery mash.",
    "category": "Main",
    "dietary requirement": "Nut-free",
    "kcals": 650,
    "fat": 30,
    "carbs": 70,
    "sugar": 10,
    "fiber": 8,
    "salt": 1.8,
    "isActive": True
  },
  {
    "name": "Vegetarian Lentil Shepherd's Pie",
    "price": 12.50,
    "description": "Hearty vegan lentil and vegetable pie topped with creamy mashed potatoes.",
    "category": "Main",
    "dietary requirement": "Vegan",
    "kcals": 550,
    "fat": 12,
    "carbs": 92,
    "sugar": 8,
    "fiber": 20,
    "salt": 1.5,
    "isActive": True
  },
  {
    "name": "British Roast Chicken",
    "price": 15.50,
    "description": "Roasted British free-range chicken served with seasonal vegetables.",
    "category": "Main",
    "dietary requirement": "Nut-free",
    "kcals": 700,
    "fat": 25,
    "carbs": 50,
    "sugar": 5,
    "fiber": 7,
    "salt": 2.0,
    "isActive": False
  },
  {
    "name": "Vegan Mushroom Risotto",
    "price": 13.00,
    "description": "Creamy risotto with local British mushrooms and herbs.",
    "category": "Main",
    "dietary requirement": "Vegan",
    "kcals": 480,
    "fat": 8,
    "carbs": 70,
    "sugar": 3,
    "fiber": 5,
    "salt": 1.2,
    "isActive": True
  },
  {
    "name": "Seafood Pie",
    "price": 16.00,
    "description": "British caught fish and shellfish in a creamy sauce topped with pastry.",
    "category": "Main",
    "dietary requirement": "Nut-free",
    "kcals": 730,
    "fat": 40,
    "carbs": 60,
    "sugar": 4,
    "fiber": 5,
    "salt": 2.3,
    "isActive": True
  },
  {
    "name": "Steak and Chips",
    "price": 18.50,
    "description": "Prime British beef steak served with crispy chips and béarnaise sauce.",
    "category": "Main",
    "dietary requirement": "Nut-free",
    "kcals": 900,
    "fat": 50,
    "carbs": 70,
    "sugar": 4,
    "fiber": 4,
    "salt": 2.5,
    "isActive": True
  }]

#Setting spl protected variables
dropItemsTableQuery = "DROP TABLE IF EXISTS items_table;"
dropStaffTableQuery = "DROP TABLE IF EXISTS staff_table;"
dropOrderTableQuery = "DROP TABLE IF EXISTS order_table;"
dropCustomerTableQuery = "DROP TABLE IF EXISTS customer_table;"
dropCategoryTableQuery = "DROP TABLE IF EXISTS category_table"
    
createCustomerTableQuery = "CREATE TABLE customer_table(customer_id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, surname_name VARCHAR(200), location VARCHAR(500) NOT NULL, email_address VARCHAR(500) NOT NULL, wallet DOUBLE PRECISION NOT NULL)"
createOrderTableQuery = "CREATE TABLE order_table(order_id SERIAL PRIMARY KEY, customer_id INT NOT NULL, item_id INT, date TIMESTAMP, paid_status BOOL NOT NULL, fulfilled_status BOOL NOT NULL, staff_id INT NOT NULL)"
createStaffTableQuery = "CREATE TABLE staff_table(staff_id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, surname_name VARCHAR(200) NOT NULL, staff_number INT NOT NULL UNIQUE, store_location VARCHAR(200), email_address VARCHAR(500))"
createItemTableQuery = "CREATE TABLE items_table(item_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, price DOUBLE PRECISION NOT NULL, description TEXT, kcals DOUBLE PRECISION, fat DOUBLE PRECISION, carbs DOUBLE PRECISION, sugar DOUBLE PRECISION, fiber DOUBLE PRECISION, salt DOUBLE PRECISION, isActive BOOL)"
createCategoryTableQuery = "CREATE TABLE category_table(category_id SERIAL PRIMARY KEY, name VARCHAR(100))"

# Make db connection
def handle_dbInit():
    connection = None
    cursor = None
    try:
        logger.info("Connecting to the database")
        connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"))
        
    #Cursor helps to perform database operations
        logger.info("Connection established")
        cursor = connection.cursor()

    #DROP EXISTING TABLES IF THEY EXISTS

        logger.info("Dropping existing tables if they exist")
        cursor.execute(dropOrderTableQuery)
        cursor.execute(dropStaffTableQuery)
        cursor.execute(dropCustomerTableQuery)
        cursor.execute(dropItemsTableQuery)
        cursor.execute(dropCategoryTableQuery)
        logger.info("Existing Tables dropped")

    # CREATE INITIAL TABLES
        logger.info("Creating tables")
        cursor.execute(createOrderTableQuery)
        cursor.execute(createStaffTableQuery)
        cursor.execute(createCustomerTableQuery)
        cursor.execute(createItemTableQuery)
        cursor.execute(createCategoryTableQuery)
        logger.info("Tables created")

    #INSERT TABLE DATA
        logger.info("Inserting data into items_tables")
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
        logger.info("Data insertion complete.")
        return {
            'statusCode': 200,
            'body': json.dumps('Database initialized successfully')
        }

    except (Exception) as error:
        logger.info("Data insertion complete")
        return {
            'statusCode': 500,
            'body': json.dumps(str(error))
            }
    finally:
        if cursor:
            cursor.close()
            logger.info("Cursor Closed")
        if connection:
            connection.close()
            logger.info("Connection close")

def lambda_handler(event, context):
    return handle_dbInit()

        
