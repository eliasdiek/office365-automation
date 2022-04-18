from ruler import Ruler
import mysql.connector
import time
from dotenv import load_dotenv
from os.path import join, dirname
import os
import threading

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dbHost = os.environ.get('DB_HOST')
dbUser = os.environ.get('DB_USER')
dbPassword = os.environ.get('DB_PASSWORD')
dbDatabase = os.environ.get('DB_DATABASE')
dbTable = os.environ.get('DB_TABLE')

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

    def ruling(self, _email, _password, _threadName):
        try:
            ruler = Ruler()
            ruler.startRuling(_email, _password, _threadName)
        except:
            print('[bulk-ruler: ruling error]')

    def getData(self):
        mydb = mysql.connector.connect(
            host = dbHost,
            user = dbUser,
            password = dbPassword,
            database = dbDatabase
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM " + dbTable +" WHERE ruled = '0' AND ruling = '0'"
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
                    print('[===================== '+ _threadName +' - Ruling start on 1 record... =====================]')
                    email = result[1]
                    password = result[2]
                    try:
                        self.updateDb(email, 'ruling', 1)
                        self.ruling(email, password, _threadName)
                        self.updateDb(email, 'ruling', 0)
                    except:
                        self.updateDb(email, 'ruling', 0)
                        pass
                else:
                    print('[==============================='+ _threadName +' - No record found ================================]')
                    time.sleep(5)
                    continue
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('[bulk-ruler: error]')
                time.sleep(2)
                continue

if __name__ == '__main__':
    threads = []
    for i in range(TotalNumberOfThreads):
        threads.append(myThread(i, "EMAIL_RULING_THREAD_" + str(i), 3 * i))

    for thread in threads:
        thread.start()