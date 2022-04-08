import os
import time
import random
import csv
import mysql.connector
from dotenv import load_dotenv
from os.path import join, dirname
import os
import imaplib
import email
from email.header import decode_header
import webbrowser

from numpy import isin

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dbHost = os.environ.get('DB_HOST')
dbUser = os.environ.get('DB_USER')
dbPassword = os.environ.get('DB_PASSWORD')
dbDatabase = os.environ.get('DB_DATABASE')
dbTable = os.environ.get('DB_TABLE')

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

    def startFetching(self, _email, _password, _folder):
        try:
            isLoggedIn = self.login(_email, _password)
        except:
            raise Exception("Sorry, error whiling logging in")

        if isLoggedIn:
            status, messages = self.imap.select(_folder)
            # print('[ddd]', self.imap.list()) # show available mailboxes
            print('[' + _folder + ' STATUS: ', status + ']')
            messages = int(messages[0])
            print('[Number of messages in ' + _folder + ': ' + str(messages) + ']')
            print('============================================================')

            FromEmails = []

            for i in range(messages, 0, -1):
                res, msg = self.imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        try:
                            msg = email.message_from_bytes(response[1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding)
                            From, encoding = decode_header(msg.get("From"))[0]
                            if isinstance(From, bytes):
                                From = From.decode(encoding)
                            Temp = From.strip().split(' ')
                            Temp.reverse()
                            FromEmail = Temp[0].replace("<", "").replace(">", "")

                            if FromEmail.find('@') != -1:
                                # print("[Subject: ", subject + "]")
                                if FromEmail != '':
                                    FromEmails.append(FromEmail)
                                print("From: ", FromEmail)
                        except:
                            pass
            
            print('[All scand emails from ' + _folder + ': ' + str(len(FromEmails)) + ']')
        
        return True
