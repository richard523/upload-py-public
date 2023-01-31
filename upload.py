import mysql.connector
import dotenv
import os
import random
from profanity_filter import filter

# importing our secret keys from .env
dotenv.load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
ANON_NAME = os.getenv("ANON_NAME")
ANON_ID = os.getenv("ANON_ID")
MYSQL_PORT = os.getenv("MYSQL_PORT")


def upload_to_db(imgurl, prompt, name, timesent, providerAccountId):
    prompt = filter(prompt)
    try:
        mydb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )
        mycursor = mydb.cursor()

        sql = f"""INSERT INTO Generation (id, imgurl, prompt, name, timesent, providerAccountId) 
        VALUES (\"{random.randint(0,10000000000)}\", \"{imgurl}\", \"{prompt}\", \"{name}\", \"{timesent}\", \"{providerAccountId}\")"""
        
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table. This is the error: {}".format(error))
        print("Attempting to upload as anonymous:")
        try:
            mydb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
            )
            mycursor = mydb.cursor()
            sql = f"""INSERT INTO Generation (id, imgurl, prompt, name, timesent, providerAccountId) 
            VALUES (\"{random.randint(0,10000000000)}\", \"{imgurl}\", \"{prompt}\", \"{ANON_NAME}\", \"{timesent}\", \"{ANON_ID}\")"""
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table as anonymous. This is the error: {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")