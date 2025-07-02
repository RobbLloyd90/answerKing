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

def handle_removeItems():
    conn = connect()
    table_name_insert = 'items_table'
    set_column_insert = "isactive"
    where_column_insert = "item_id"
    newSet_value = "false"
    where_value = 2

    queryStr = sql.SQL("UPDATE {table_name} SET {set_column} = %s WHERE {where_column} = %s RETURNING item_id, name, isactive").format(table_name=sql.Identifier(table_name_insert), set_column=sql.Identifier(set_column_insert), where_column=sql.Identifier(where_column_insert))
    testQ = (newSet_value, where_value)

    try:
        cursor = conn.cursor()
        cursor.execute(queryStr, testQ)
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
        return handle_removeItems()    

