import os
import json
import psycopg2
from psycopg2 import Error, sql
import logging
import copy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))
    
    return connection

def handle_modifyItem(item_id, body):
    logger.info("Connecting to the database")
    conn = connect()
    logger.info("Connection Established")

    table_name_insert = 'items_table'
    item_id = 'item_id'
    itemToAdd = copy.deepcopy(body)
 
    # Sets all key names from the body
    key = [key for key, val in itemToAdd.items()]
    # Set the first key name to be the column to update
    set_column_insert = key[0]
    # Set the first key value new value
    newSet_value = itemToAdd[key[0]]


    queryStr = sql.SQL("UPDATE {table_name} SET {set_column} = %s WHERE {where_column} = %s RETURNING *").format(table_name=sql.Identifier(table_name_insert), set_column=sql.Identifier(set_column_insert), where_column=sql.Identifier(item_id))
    try:
        cursor = conn.cursor()
        logger.info(f"QueryStr Check: {queryStr, (newSet_value, item_id)}")
        cursor.execute(queryStr, (newSet_value, item_id))
        results = cursor.fetchall()
        cursor.close()

    except (Exception, Error) as error:
        logger.info("Error while connecting to database", error)
        return{
             'statusCode': 500,
             'body': json.dumps({'error': str(error)})
        }
    
    finally:
        conn.close()
        logger.info("Connection is closed")
        return{
             'statusCode': 200,
             'body': json.dumps({'Modified item': str(results)})
        }
    
def lambda_handler(event, context):
    item_id = event['pathParameters'].get('id')

    #Check if there is an id in the parameters, if not return 400

    if not item_id:
            return{
                 'statusCode': 400,
                 'body': json.dumps({'error': 'Missing item ID in path'})
            }
    body = json.loads(event['body'])

    return handle_modifyItem(item_id, body)    

