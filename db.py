from dotenv import load_dotenv
import psycopg2.extras
import psycopg2
import os

load_dotenv()
def connect():
    conn = psycopg2.connect(
        host= os.getenv('DB_HOST'),
        database= os.getenv('DB_NAME'),
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        sslmode='require',
        )
    return conn

def upload_metadata(filename:str, fileURL:str,hostName_id:int, datetime, object:int):
    '''Uploads Screenshot Metadata to postgres Database on a Remote Local Server'''
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            query='INSERT INTO logs (fileName,fileURL,hostname_id,dateAndTime,detectedObject_id) VALUES (%s, %s, %s,%s, %s)',
            vars=(filename, fileURL, hostName_id, datetime, object)
            )
        conn.commit()
        cur.close()
    except psycopg2.InterfaceError as e:
        print('{} - connection will be reset'.format(e))
        # Close old connection 
        if conn:
            if cur:
                cur.close()
            conn.close()
        conn = None
        cur = None
        #Reconnect
        conn = connect()
        conn.cursor()
