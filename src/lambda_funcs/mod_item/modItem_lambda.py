import os
import json
import psycopg2
from psycopg2 import Error, sql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Connects to the database
def connect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))    
    return connection

#Sorts and sets the PSQL Query
def handle_setQueryData(body, item_id):
    set_column_insert = None
    newSet_value = None
    for key, value in body.items():
        set_column_insert = key
        newSet_value = value
    queryStr = sql.SQL("UPDATE items_table SET name = %s WHERE item_id = %s RETURNING *").as_string(connect())
    return queryStr, newSet_value

#Takes a PSQL String and parameters with Id and modify the items table
def handle_modifyItem(query, param, item_id):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (param, item_id))
        results = cursor.fetchall()

    except (Exception, Error) as error:
        logger.info("Error while connecting to database", error)
        return{
             'statusCode': 500,
             'body': json.dumps({'error': str(error)})
        }
    
    finally:
        cursor.close()
        conn.commit()
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
    query, param = handle_setQueryData(body, item_id)
    return handle_modifyItem(query, param, item_id)    

