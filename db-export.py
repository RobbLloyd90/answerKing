import os
import json
import psycopg2
import dotenv

loadenv()

def dbConnect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))
    return connection

def dbRead():
    try:
        conn = dbConnect()
        cursor = conn.cursor()

        with open(dump_file_path, 'r') as f:
                sql = f.read()
                cursor.execute(sql)
                print("Db imported successfully")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        if 'cur' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()