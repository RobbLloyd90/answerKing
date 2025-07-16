import os
import json
import psycopg2
from psycopg2 import Error, sql
import logging

def connect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))    
    return connection

def handle_builds_queryStr(body, item_id):
    fieldName = None
    value = None
    for key, val in body.items():
        fieldName = key
        value = val
    queryStr = sql.SQL("UPDATE items_table SET {field} = %s WHERE item_id = %s RETURNING *").format(field=sql.Identifier(fieldName)).as_string(connect())
    return queryStr, value

def handle_modify_item(query, param, item_id):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (param, item_id))
        results = cursor.fetchall()

    except (Exception, Error) as error:
        return{
             'statusCode': 500,
             'body': json.dumps({'error': str(error)})
        }
    
    finally:
        cursor.close()
        conn.commit()
        conn.close()
        return{
             'statusCode': 200,
             'body': json.dumps({'Modified item': str(results)})
        }
    
def lambda_handler(event, context):
    item_id = event['pathParameters'].get('id')

    if not item_id:
            return{
                 'statusCode': 400,
                 'body': json.dumps({'error': 'Missing item ID in path'})
            }
    
    body = json.loads(event['body'])
    query, param = handle_builds_queryStr(body, item_id)
    return handle_modify_item(query, param, item_id)    