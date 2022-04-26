import dns.resolver
import csv
import time
import os

ts = str(time.time())
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
        directory = './results/verifier'
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + '/' + _filename, 'a', newline='', encoding='utf-8') as f:
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

    def spfLookup(self, _domain):
        spfRecord = ''
        try:
            for x in dns.resolver.resolve(_domain, 'TXT'):
                if 'spf1' in str(x):
                    spfRecord = str(x).split(' ')[1].split(':')[1]
        except:
            spfRecord = 'nospfrecord.com.'
        
        return spfRecord

    def isOffice365FromMX(self, _mxRecord):
        try:
            domainId = _mxRecord.split('.')[::-1][2]
            if domainId == 'outlook':
                return True
            else:
                return False
        except:
            return False

    def isOffice365FromSpf(self, _spfRecord):
        try:
            domainId = _spfRecord.split('.')[::-1][1]
            if domainId == 'outlook':
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
        try:
            domain = _email.split('@')[1].lower()
            # mxRecord = self.mxLookup(domain)
            spfRecord = self.spfLookup(domain)
            # print('[mxRecord]', mxRecord)
            # print('[spfRecord]', spfRecord)
            
            if self.isOffice365FromSpf(spfRecord):
                self.writeCsv('result-office365-' + ts + '.csv', [_email])
                print('[TRUE]', _email, domain, spfRecord)
            else:
                print('[FALSE]', _email, domain, spfRecord)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)