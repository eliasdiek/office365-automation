from fetcher import Fetcher
import mysql.connector
import time
from dotenv import load_dotenv
from os.path import join, dirname
import os
import pandas as pd
import threading

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
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting " + self.name)
        self.main(self.counter)
        print("Exiting " + self.name)

    def fetching(self, _email, _password, _folder):
        try:
            fetcher = Fetcher()
            return fetcher.startFetching(_email, _password, _folder)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return False

    def getData(self):
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

    def updateDb(self, _email, _field, _status):
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

    def main(self, _delay):
        time.sleep(_delay)
        while(True):
            try:
                result = self.getData()

                if len(result) > 0:
                    print('[===================== ' + str(len(result)) + ' record(s) found, fetching start... =====================]')

                    email = result[1]
                    password = result[2]
                    status = 0

                    self.updateDb(email, 'fetching', 1)

                    for folder in FOLDERS:
                        isFetched = self.fetching(email, password, folder)
                        print('[isFetched]', isFetched)
                        if isFetched:
                            status = 1
                        else:
                            status = 0

                    self.updateDb(email, 'fetched', status)
                else:
                    print('[=============================== No record found ================================]')
                    time.sleep(5)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('[bulk-fetcher: error]')
                time.sleep(2)

thread1 = myThread(1, "Thread-1", 0)
thread2 = myThread(2, "Thread-2", 3)