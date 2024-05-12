from dotenv import load_dotenv
import os
import time
import mysql.connector as mysql
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def contodb():
    while True:
        try:
            db = mysql.connect(
                host="localhost",
                port=3306,
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            if db.is_connected():
                print("Connected to the database")
                break
        except Error as e:
            print("Not connected to the database yet...")
            time.sleep(5) 
    return db