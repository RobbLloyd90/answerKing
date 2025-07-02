import os
import json
import psycopg2
from psycopg2 import Error, sql
from dotenv import load_dotenv

load_dotenv()


def connect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))
    
    return connection

def handle_setNewItem(data):
    #split url path into an object/list
    newItemData = []
    return newItemData

def handle_createItem():
    conn = connect()

    itemData = handle_setNewItem()

    try:
        cursor = conn.cursor()
        
        for item in itemData:
                name = item['name']
                price = item['price']
                description =item['description']
                kcals = item['kcals']
                carbs = item['carbs']
                sugar = item['sugar']
                fiber = item['fiber']
                salt =item['salt']
                isActive = item['isActive']


                queryStr = """INSERT INTO items_table(name, price, description, kcals, carbs, sugar, fiber, salt, isActive) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING;"""
                queryData = (name, price, description, kcals, carbs, sugar, fiber, salt, isActive)

                cursor.execute(queryStr, queryData)
                conn.commit()
                cursor.close()



        cursor.execute("SELECT item_id, name, isactive FROM items_table" )
        results = cursor.fetchall()
        print(results)

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    
    finally:
        cursor.close()
        conn.close()
        print("PostgreSQ: connection is closed")
    
def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']
    
    if method == 'DELETE' and path == '/items/remove:6':
#Get uri path details
        return handle_createItem()    

