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

TotalNumberOfThreads = 5

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        self.main(self.name, self.counter)

    def fetching(self, _email, _password, _folder, _threadName):
        try:
            fetcher = Fetcher()
            return fetcher.startFetching(_email, _password, _folder, _threadName)
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
        sql = "SELECT * FROM " + dbTable +" WHERE fetched = '0' AND fetching = '0'"
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
        sql = "UPDATE office365 SET "+ _field +" = '"+ str(_status) +"' WHERE email = '"+ _email +"'"
        mycursor.execute(sql)
        mydb.commit()
        print("[DB updated, ", mycursor.rowcount, "record(s) affected]")

    def main(self, _threadName, _delay):
        time.sleep(_delay)
        while(True):
            try:
                result = self.getData()

                if result:
                    print('[===================== '+ _threadName +' - Fetching start on 1 record... =====================]')

                    email = result[1]
                    password = result[2]
                    status = 0

                    self.updateDb(email, 'fetching', 1)

                    try:
                        for folder in FOLDERS:
                            isFetched = self.fetching(email, password, folder, _threadName)
                            print('[isFetched]', isFetched)
                            if isFetched:
                                status = 1
                            else:
                                status = 0

                        self.updateDb(email, 'fetching', 0)
                        self.updateDb(email, 'fetched', status)
                    except:
                        self.updateDb(email, 'fetching', 0)
                        pass
                else:
                    print('[=============================== '+ _threadName +' - No record found ================================]')
                    time.sleep(5)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('[bulk-fetcher: error]')
                time.sleep(2)

if __name__ == '__main__':
    threads = []
    for i in range(TotalNumberOfThreads):
        threads.append(myThread(i, "EMAIL_FETCHING_THREAD_" + str(i), 3 * i))

    for thread in threads:
        thread.start()