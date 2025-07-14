import os
import json
import psycopg2
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connectDB():
    
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))    
    return connection
    
def handle_getAll():
    logger.info("establishing connection")
    connection = connectDB()
    
    logger.info("Connection established")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT category FROM category_table WHERE isactive = true")
        results = cursor.fetchall()
        logger.info("Results should be stored")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return{
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(error)})
        }    
    finally:
        cursor.close()
        connection.close()
        print("PostgreSQ: connection is closed")

        return{
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(results)
        }

def lambda_handler(event, context):
        logger.info("Getting all categories")
        return handle_getAll()    

