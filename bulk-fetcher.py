from fetcher import Fetcher
import mysql.connector
import time
from dotenv import load_dotenv
from os.path import join, dirname
import os
import pandas as pd
import thread

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dbHost = os.environ.get('DB_HOST')
dbUser = os.environ.get('DB_USER')
dbPassword = os.environ.get('DB_PASSWORD')
dbDatabase = os.environ.get('DB_DATABASE')
dbTable = os.environ.get('DB_TABLE')

FOLDERS = [
    {
        "key": "INBOX",
        "label": "inbox"
    },
    {
        "key": "\"Sent Items\"",
        "label": "sent"
    }
]

def fetching(_email, _password, _folder):
    try:
        fetcher = Fetcher()
        return fetcher.startFetching(_email, _password, _folder)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False

def getData():
    mydb = mysql.connector.connect(
        host = dbHost,
        user = dbUser,
        password = dbPassword,
        database = dbDatabase
    )
    mycursor = mydb.cursor()
    sql = "SELECT * from " + dbTable +" where fetched = '0' AND fetching = '0'"
    mycursor.execute(sql)
    result = mycursor.fetchone()

    return result

def updateDb(_email, _field, _status):
    mydb = mysql.connector.connect(
        host = dbHost,
        user = dbUser,
        password = dbPassword,
        database = dbDatabase
    )
    mycursor = mydb.cursor()
    sql = "UPDATE office365 SET '" + _field +"' = '"+ str(_status) +"' WHERE email = '"+ _email +"'"
    mycursor.execute(sql)
    mydb.commit()
    print("[DB updated, ", mycursor.rowcount, "record(s) affected]")

def main(_delay):
    time.sleep(_delay)
    while(True):
        try:
            result = getData()

            if len(result) > 0:
                print('[===================== ' + str(len(result)) + ' record(s) found, fetching start... =====================]')

                email = result[1]
                password = result[2]
                status = 0

                updateDb(email, 'fetching', 1)

                for folder in FOLDERS:
                    isFetched = fetching(email, password, folder)
                    print('[isFetched]', isFetched)
                    if isFetched:
                        status = 1
                    else:
                        status = 0

                updateDb(email, 'fetched', status)
            else:
                print('[=============================== No record found ================================]')
                time.sleep(5)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print('[bulk-fetcher: error]')
            time.sleep(2)

def test(_email, _password):
    try:
        isFetched = fetching(_email, _password, FOLDERS[0])
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        pass

if __name__ == '__main__':
    try:
        thread.start_new_thread( main, (0) )
        thread.start_new_thread( main, (3) )
    except:
        print("[Error: unable to start thread]")

    # test("zhang.yuyuan@hotmail.com", "China2021!@#")
    # for folder in FOLDERS:
    #     saveResult(['test@test.com', 'test2@test.com'], "test@example.com - " + folder['label'])