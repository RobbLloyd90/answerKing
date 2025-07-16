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

def handle_removeCategory(id):
    conn = connect()
    newSet_value = "false"

    queryStr = sql.SQL("UPDATE category_table SET isActive = %s WHERE category_id = %s RETURNING category_id, category")

    try:
        cursor = conn.cursor()
        logger.info(f"{queryStr,(newSet_value, id)}")
        cursor.execute(queryStr, (newSet_value, id))

        results = cursor.fetchall()
        logger.info(f"Deleted Category: {results}")

        return{
             'statusCode': 200,
             'body': json.dumps({'Deleted Category': str(results)})
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
    id = event['pathParameters'].get('id')
    if not id:
            return{
                 'statusCode': 400,
                 'body': json.dumps({'error': 'Missing Category ID in path'})
            }
    return handle_removeCategory(id)    

