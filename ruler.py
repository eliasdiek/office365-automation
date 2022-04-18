from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import random
import csv
import mysql.connector
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

RULES = [
    {
        'statement': ['Payment', 'Invoice', 'Statement'],
        'ruleName': 'outlook_ruler_1',
        'action': 'Redirect to',
        'rulerEmail': 'myemail@gmail.com',
        'stopProcessing': True
    },
    {
        'statement': ['myemail@gmail.com'],
        'ruleName': 'outlook_ruler_2',
        'action': "Delete",
        'rulerEmail': '',
        'stopProcessing': False
    }
]

class Ruler():
    def __init__(self):
        DEFAULT_PATH = os.path.join(os.path.dirname(__file__))
        driverPath = DEFAULT_PATH+"/chromedriver"
        self.options = webdriver.ChromeOptions()
        # self.options.setBinary(driverPath)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--window-size=1360,768')
        # self.options.add_argument('--headless')
        # self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-setuid-sandbox')
        self.options.add_argument("--proxy-server='direct://")
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-accelerated-2d-canvas')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("start-maximized")
        self.options.add_argument("-incognito")
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        # self.driver = webdriver.Chrome(options=self.options)
        # self.driver = webdriver.Chrome(driverPath, options=self.options)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.url = 'https://outlook.office.com/mail/'
        self.internetconnection()
        self.sleep(2, 3)

    def internetconnection(self):
        while(True):
            if "No internet" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "This site can’t be reached" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "Your connection was interrupted" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "This page isn’t working" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            break

    def get_element_text_by_xpath(self, xpath, element):
        try:
            return element.find_element_by_xpath(xpath).text
        except:
            return 'N/A'

    def sleep(self, min, max):
        ranum = 0
        ranum = random.randint(min, max)
        time.sleep(ranum)

    def updateDb(_self, _email, _provider, _status):
        mydb = mysql.connector.connect(
            host = dbHost,
            user = dbUser,
            password = dbPassword,
            database = dbDatabase
        )
        mycursor = mydb.cursor()
        sql = "UPDATE office365 SET provider = '"+ _provider +"', ruled = '"+ str(_status) +"' WHERE email = '"+ _email +"'"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    def login(self, _email, _password):
        provider = 'outlook'
        try:
            self.driver.get(self.url)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").clear()
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").send_keys(_email)
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
        except:
            raise Exception("Sorry, error whiling inserting email and clicking next button")
        try:
            time.sleep(5)
            currentUrl = self.driver.current_url

            if "sso.godaddy.com" not in currentUrl:
                # normal office login
                self.driver.find_element(By.XPATH, "//*[@id='i0118']").clear()
                self.driver.find_element(By.XPATH, "//*[@id='i0118']").send_keys(_password)
                self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            else:
                # godaddy login
                provider = 'godaddy'
                self.driver.find_element(By.ID, 'password').send_keys(_password)
                self.driver.find_element(By.ID, 'submitBtn').click()
        except:
            raise Exception("Sorry, error whiling detecting provider")

        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click() # for Stay signed in
            self.sleep(1, 2)
        except:
            raise Exception("Sorry, error whiling clicking submit button")

        return provider

    def startRuling(self, _email, _password, _threadName):
        email = _email
        password = _password
        provider = ''
        try:
            provider = self.login(email, password)
        except:
            raise Exception("Sorry, error whiling logging in")
        status = 1
        print('[Logged in -> provider:]', provider)

        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@id='owaSettingsButton']").click()
            self.sleep(1, 2)
        except:
            status = 0
            raise Exception("Sorry, error whiling clicking settings button")
        try:
            time.sleep(1)
            self.driver.find_element(By.CLASS_NAME, 'UWwiiejueEpNL3F_57Ex').click()
            self.sleep(1, 2)
        except:
            status = 0
            raise Exception("Sorry, error whiling clicking open settings button")
        try:
            surveyModal = self.driver.find_element(By.XPATH, '//span[text()="How likely are you to recommend Outlook on the web to others, if asked?"]')
            if surveyModal:
                self.driver.find_element(By.XPATH, '//span[text()="Cancel"]').click()
        except:
            pass
        try:
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'button.IPzlgksV3AiFfCZs9pYI:nth-child(4)').click()
        except:
            status = 0
            raise Exception("Sorry, error whiling clicking rule menu button")

        try:
            for rule in RULES:
                ruleName = rule['ruleName']
                statement = rule['statement']
                action = rule['action']
                rulerEmail = rule['rulerEmail']
                stopProcessing = rule['stopProcessing']
                status = 0
                print('[***************** Processed rule name ******************]', ruleName)
                isRuled = self.isRuled(ruleName)
                if isRuled:
                    print('[=============== Already ruled! Rule name: '+ ruleName +', Skipping... ===============]')
                    status = 1
                else:
                    self.addRule(ruleName, statement, action, rulerEmail, stopProcessing)
                    status = 1
        except:
            status = 0
            raise Exception("Sorry, error whiling ruling")

        print('[================================='+ _threadName +' - Ruling DONE! =================================]')

        try:
            self.updateDb(email, provider, status)
            print('[================================= DB UPDATED! ==================================]')
        except:
            print('[Error] error whiling updating DB')
            pass
        
        return 'success'

    def addRule(self, _name, _keywords, _action, _to, _stopProcessing):
        try:
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//span[text()="Add new rule"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@placeholder="Name your rule"]').clear()
            self.driver.find_element(By.XPATH, '//*[@placeholder="Name your rule"]').send_keys(_name)
            self.driver.find_element(By.XPATH, '//span[text()="Select a condition"]').click()
            self.driver.find_element(By.XPATH, '//span[text()="Subject or body includes"]').click()
            lookForInput = self.driver.find_element(By.XPATH, '//*[@placeholder="Enter words to look for"]')
            for keyword in _keywords:
                lookForInput.send_keys(keyword)
                lookForInput.send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, '//span[text()="Select an action"]').click()
            self.driver.find_element(By.XPATH, '//span[text()="' + _action +'"]').click()
            time.sleep(1)

            if _to != '':
                targetElem = self.driver.find_element(By.CSS_SELECTOR, 'div.ms-BasePicker-text>input')
                targetElem.send_keys(_to)
                time.sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, 'div.ms-Suggestions-sectionButton>div').click()

            if _stopProcessing:
                self.driver.find_element(By.XPATH, '//span[text()="Stop processing more rules"]').click()

            self.driver.find_element(By.XPATH, '//span[text()="Save"]').click()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass

    def isRuled(self, _ruleName):
        try:
            time.sleep(2)
            elems = self.driver.find_elements(By.CSS_SELECTOR, 'div.ms-Toggle + div > div:nth-child(1)')
            # print('[elems]', elems)
            for elem in elems:
                if elem.text == _ruleName:
                    return True
            
            return False
        except:
            print('[isRuled: error]')
            return False
