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

def queryFormat(body):
    CategoryToAdd = body
    category = CategoryToAdd['category']
    isActive = CategoryToAdd['isActive']

    formattedQuery = (category, isActive)
    return formattedQuery


def handle_createCategory(queryData):
    logger.info("Connecting to the database")
    conn = connect()
    logger.info("Connection Established")

    try:
        cursor = conn.cursor()
        queryStr = """INSERT INTO category_table(category, isActive) VALUES(%s,%s) RETURNING *;"""
        cursor.execute(queryStr, queryData)
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
             'statusCode': 201,
             'body': json.dumps({'New Category Created': str(results)})
        }
        
    
def lambda_handler(event, context):
    body = json.loads(event['body'])
    logger.info(body)
    queryData = queryFormat(body)
    return handle_createCategory(queryData)      

