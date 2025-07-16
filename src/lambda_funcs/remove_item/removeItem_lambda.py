import os
import json
import psycopg2
from psycopg2 import Error, sql
import logging

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

def handle_removeItems(item_id):
    logger.info("Connecting to the database")
    conn = connect()
    logger.info("Connection Established")

    queryStr = sql.SQL("UPDATE items_table SET isactive = false WHERE item_id = %s RETURNING item_id, name, isactive")

    try:
        cursor = conn.cursor()
        cursor.execute(queryStr, (item_id))
        results = cursor.fetchall()
        logger.info(f"Deleted item: {results}")

        return{
             'statusCode': 200,
             'body': json.dumps({'Deleted item': str(results)})
        }


    except (Exception, Error) as error:
        logger.info("Error while connecting to database", error)
        return{
             'statusCode': 500,
             'body': json.dumps({'error': str(error)})
        }
    
    finally:
        cursor.close()
        conn.close()
        logger.info("Connection is closed")
    
def lambda_handler(event, context):
    #Ensure on AWS that the API-Gateway method is set to Delete
    item_id = event['pathParameters'].get('id')
    if not item_id:
            return{
                 'statusCode': 400,
                 'body': json.dumps({'error': 'Missing item ID in path'})
            }
    return handle_removeItems(item_id)    

