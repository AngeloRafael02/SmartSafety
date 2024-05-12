from dotenv import load_dotenv
import psycopg2.extras
import psycopg2
import os

# only for testing
import datetime
import time

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

# for debugging modules
if __name__ == '__main__':
    Stime = time.time()
    ## Put Function to test Here
    upload_metadata("picture.jpg","test1/picture.jpg",2, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),1)
    Etime = time.time()
    print(f"Execution time: {Etime-Stime} seconds")
