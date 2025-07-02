import os
import json
import psycopg2
    
def handle_getAllItems():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items_table WHERE isactive = true")
        results = cursor.fetchall()

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

handle_getAllItems()

def lambda_handler(event, context):
        return handle_getAllItems()    

