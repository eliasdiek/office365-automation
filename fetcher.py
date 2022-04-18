import os
import imaplib
import email
from email.header import decode_header
import pandas as pd

excludeList = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "aol.com",
    "sct-15-20-4755-11-msonline-outlook-cd57b.templateTenant",
    "linkedin.com",
    "reply.linkedin.com"
]

class Fetcher():
    def __init__(self):
        try:
            self.imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def login(self, _email, _password):
        try:
            result = self.imap.login(_email, _password)
            print('[login: ', result[0] + ']')
            if result[0] == 'OK':
                return True
            else:
                return False
        except:
            return False

    def saveResult(self, _result, _fileName):
        try:
            directory = './results'
            if not os.path.exists(directory):
                os.makedirs(directory)

            df = pd.DataFrame(_result)
            df.to_csv(directory + '/' + _fileName + '.csv',index=False)

            return True
        except:
            return False

    def getEmail(self, _message, _who):
        try:
            msg = email.message_from_bytes(_message)
            EmailStr, encoding = decode_header(msg.get(_who))[0]
            
            if isinstance(EmailStr, bytes):
                EmailStr = EmailStr.decode(encoding)
            Temp = EmailStr.strip().split('<')
            Temp.reverse()
            Email = Temp[0].replace("<", "").replace(">", "")

            if Email.find('@') != -1:
                domain = Email.split('@')[1]
                if Email != '' and domain not in excludeList:
                    print("" + _who + ": ", Email)
                    return Email
                else:
                    return ''
            else:
                return ''
        except:
            return ''

    def startFetching(self, _email, _password, _folder):
        try:
            isLoggedIn = self.login(_email, _password)
        except:
            raise Exception("Sorry, error whiling logging in")

        if isLoggedIn:
                status, messages = self.imap.select(_folder['key'])
                # print('[ddd]', self.imap.list()) # show available mailboxes
                print('[' + _folder['key'] + ' STATUS: ', status + ']')
                messages = int(messages[0])
                print('[Number of messages in ' + _folder['key'] + ': ' + str(messages) + ']')
                print('============================================================')

                Emails = []

                for i in range(messages, 0, -1):
                    res, msg = self.imap.fetch(str(i), "(RFC822)")
                    for response in msg:
                        if isinstance(response, tuple):
                            if _folder['key'] == 'INBOX':
                                FromEmail = self.getEmail(response[1], 'From')
                                if FromEmail != '':
                                    Emails.append(FromEmail)
                            else:
                                ToEmail = self.getEmail(response[1], 'To')
                                if ToEmail != '':
                                    Emails.append(ToEmail)

                                BccEmail = self.getEmail(response[1], 'Bcc')
                                if BccEmail != '':
                                    Emails.append(BccEmail)

                            CcEmail = self.getEmail(response[1], 'Cc')
                            if CcEmail != '':
                                Emails.append(CcEmail)
                
                uniqueEmails = list(set(Emails))

                print('[All scand emails from ' + _folder['key'] + ': ' + str(len(Emails)) + ', Number of unique emails:' + str(len(uniqueEmails)) + ']')

                isSaved = self.saveResult(uniqueEmails, _email + ' - ' + _folder['label'])
                print('[======== Result saved in the results directory ========]')

                if isSaved:
                    return True
                else:
                    return False

        else:
            print('[Login is not True]')
            return False
