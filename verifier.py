import dns.resolver
import csv

class Verifier:
    def __init__(self):
        self.domain = 'https://www.google.com'

    def readCsv(self, _filename):
        result = []
        with open(_filename, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                result.append(row)

        return result

    def writeCsv(self, _filename, _row):
        with open(_filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter =',')
            writer.writerow(_row)

    def mxLookup(self, _domain):
        mxRecord = ''
        try:
            for x in dns.resolver.resolve(_domain, 'MX'):
                mxRecord = x.to_text().split(' ')[1]
        except:
            mxRecord = 'nomxrecord.com.'

        return mxRecord

    def isOffice365(self, _mxRecord):
        try:
            domainId = _mxRecord.split('.')[::-1][2]
            if domainId == 'outlook':
                return True
            else:
                return False
        except:
            return False

    def isGodaddy(self, _mxRecord):
        try:
            domainId = _mxRecord.split('.')[::-1][2]
            domainAppendix = _mxRecord.split('.')[::-1][1]
            
            if domainId == 'secureserver' and domainAppendix == 'net':
                return True
            else:
                return False
        except:
            return False

    def removeDuplicatedDomains(self, _filename):
        contacts = self.readCsv(_filename)
        temp = []

        for contact in contacts:
            email = contact[0]
            domain = email.split('@')[1].lower()

            if domain not in temp:
                temp.append(domain)
                self.writeCsv('initial-3.unique.csv', [email])

    def startVerifying(self, _email, _threadName):
        # self.writeCsv('/verifier-result/result-office365.csv', ['email', 'domain', 'mxRecord'])

        try:
            domain = _email.split('@')[1].lower()
            mxRecord = self.mxLookup(domain)
            
            if self.isOffice365(mxRecord):
                # self.writeCsv('/verifier-result/result-office365.csv', [_email, domain, mxRecord])
                print('[TRUE]', _email, domain, mxRecord)
            else:
                print('[FALSE]', _email, domain, mxRecord)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)