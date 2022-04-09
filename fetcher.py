import os
import imaplib
import email
from email.header import decode_header
import pandas as pd

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

    def startFetching(self, _email, _password, _folder):
        try:
            isLoggedIn = self.login(_email, _password)
        except:
            raise Exception("Sorry, error whiling logging in")

        if isLoggedIn:
            try:
                status, messages = self.imap.select(_folder)
                # print('[ddd]', self.imap.list()) # show available mailboxes
                print('[' + _folder + ' STATUS: ', status + ']')
                messages = int(messages[0])
                print('[Number of messages in ' + _folder + ': ' + str(messages) + ']')
                print('============================================================')

                FromEmails = []

                for i in range(messages, messages - 5, -1):
                    res, msg = self.imap.fetch(str(i), "(RFC822)")
                    for response in msg:
                        if isinstance(response, tuple):
                            try:
                                msg = email.message_from_bytes(response[1])
                                From, encoding = decode_header(msg.get("From"))[0]
                                
                                if isinstance(From, bytes):
                                    From = From.decode(encoding)
                                Temp = From.strip().split(' ')
                                Temp.reverse()
                                FromEmail = Temp[0].replace("<", "").replace(">", "")

                                if FromEmail.find('@') != -1:
                                    if FromEmail != '':
                                        FromEmails.append(FromEmail)
                                    print("From: ", FromEmail)
                            except:
                                pass
                
                uniqueEmails = list(set(FromEmails))

                print('[All scand emails from ' + _folder + ': ' + str(len(FromEmails)) + ', Number of unique emails:' + str(len(uniqueEmails)) + ']')

                isSaved = self.saveResult(uniqueEmails, _email + ' - ' + _folder)
                print('[======== Result saved in the results directory ========]')

                if isSaved:
                    return True
                else:
                    return False
            except:
                return False
        else:
            print('[Login is not True]')
            return False
