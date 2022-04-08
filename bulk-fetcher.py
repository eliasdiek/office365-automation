from fetcher import Fetcher
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

FOLDERS = ["INBOX", "\"Sent Items\""]

def fetching(_email, _password, _folder):
    try:
        fetcher = Fetcher()
        fetcher.startFetching(_email, _password, _folder)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

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
            sql = "SELECT * from " + dbTable +" where fetched = '0'"
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # print('[result]', result)
            if len(result) > 0:
                print('[====================== ' + str(len(result)) + ' record(s) found, fetching start... ======================]')
                for item in result:
                    email = item[1]
                    password = item[2]
                    provider = item[3]
                    fetching(email, password)
            else:
                print('[=============================== No record found ================================]')
                time.sleep(5)
                continue
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print('[bulk-fetcher: error]')
            time.sleep(2)
            continue

def test():
    fetching("rose@bensemann.co.nz", "Swans0n1234!", FOLDERS[0])
    # mystr = '"Nick Scali" <Feedback@nickscali.com.au> '
    # temp = mystr.strip().split(' ')
    # temp.reverse()
    # print('[result]', temp[0])

if __name__ == '__main__':
    test()