import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Bittu@9119"
DB_NAME = "news_data"

def connect_to_database():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def close_database_connection(conn):
    conn.close()
