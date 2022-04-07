from ruler import Ruler
import mysql.connector
import time
from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dbHost = os.environ.get('DB_HOST')
dbUser = os.environ.get('DB_USER')
dbPassword = os.environ.get('DB_PASSWORD')
dbDatabase = os.environ.get('DB_DATABASE')
dbTable = os.environ.get('DB_TABLE')

def ruling(_email, _password):
    try:
        ruler = Ruler()
        ruler.startRuling(_email, _password)
    except:
        print('[auto-ruler: ruling error]')

def main():
    while(True):
        try:
            mydb = mysql.connector.connect(
                host = dbHost,
                user = dbUser,
                password = dbPassword,
                database = dbDatabase
            )
            mycursor = mydb.cursor()
            sql = "SELECT * from " + dbTable +" where ruled = '0'"
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # print('[result]', result)
            if len(result) > 0:
                print('[====================== ' + str(len(result)) + ' record(s) found, ruling start... ======================]')
                for item in result:
                    email = item[1]
                    password = item[2]
                    ruling(email, password)
            else:
                print('[=============================== No record found ================================]')
                time.sleep(5)
                continue
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print('[auto-ruler: error]')
            time.sleep(2)
            continue

if __name__ == '__main__':
    main()
    # test()