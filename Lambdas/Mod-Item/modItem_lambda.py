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

def handle_setQueryData(body, item_id):
    for key, value in body.items():
    # Set the first key name to be the column to update
        set_column_insert = key
    # Set the first key value new value
        newSet_value = value

    queryStr = sql.SQL("UPDATE item_table SET {set_column} = %s WHERE item_id = %s RETURNING *").format(set_column=sql.Identifier(set_column_insert))
    query = (queryStr, (newSet_value, item_id))
    return query

def handle_modifyItem(query):
    logger.info("Connecting to the database")
    conn = connect()
    logger.info("Connection Established")

    try:
        cursor = conn.cursor()
        logger.info(f"QueryStr Check: {query}")
        cursor.execute(query)
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
    query = handle_setQueryData(body, item_id)
    return handle_modifyItem(query)    

