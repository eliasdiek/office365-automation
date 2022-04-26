from verifier import Verifier
import time
import threading
import csv

TotalNumberOfThreads = 3
InputFiles = [
    "./input/verifier/emails_1.csv",
    "./input/verifier/emails_2.csv",
    "./input/verifier/emails_3.csv",
]
class myThread(threading.Thread):
    def __init__(self, threadID, name, inputFile, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inputFile = inputFile
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        self.main(self.name, self.counter)

    def readCsv(self, _filename):
        result = []
        with open(_filename, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                result.append(row)

        return result

    def verifying(self, _email, _threadName):
        try:
            verifier = Verifier()
            return verifier.startVerifying(_email, _threadName)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return False

    def main(self, _threadName, _delay):
        time.sleep(_delay)
        contacts = self.readCsv(self.inputFile)
        for contact in contacts:
            email = contact[0]
            # print('[' + _threadName + ']')
            self.verifying(email, _threadName)
        

if __name__ == '__main__':
    threads = []
    for i in range(TotalNumberOfThreads):
        threads.append(myThread(i, "EMAIL_VERIFYING_THREAD_" + str(i), InputFiles[i], 3 * i))

    for thread in threads:
        thread.start()