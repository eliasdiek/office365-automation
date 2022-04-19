from verifier import Verifier
import time
import threading

TotalNumberOfThreads = 1

EMAILS = [
    "owen@perennialbuilders.com",
    "office@unionsportssales.com"
]

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        self.main(self.name, self.counter)

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
        for email in EMAILS:
            print('[' + _threadName + ']')
            self.verifying(email, _threadName)
        

if __name__ == '__main__':
    threads = []
    for i in range(TotalNumberOfThreads):
        threads.append(myThread(i, "EMAIL_VERIFYING_THREAD_" + str(i), 3 * i))

    for thread in threads:
        thread.start()