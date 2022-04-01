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
        # self.ruling(_email, _password)
        # self.start()

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

    def normalRuling(self, _email, _password):
        email = _email
        password = _password
        self.normalLogin(email, password)

        try:
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='owaSettingsButton']").click()
            self.sleep(1, 2)
        except:
            pass
        try:
            time.sleep(1)
            # self.driver.find_element_by_xpath("(//*[@class='ms-Button ms-Button--action ms-Button--command UWwiiejueEpNL3F_57Ex root-245'])[0]").click()
            # self.driver.find_element_by_xpath("(//*[@class='next nextSelection'])[9]").click()
            self.driver.find_element(By.CLASS_NAME, 'UWwiiejueEpNL3F_57Ex').click()
            self.sleep(1, 2)
        except:
            pass
        try:
            surveyModal = self.driver.find_element(By.XPATH, '//span[text()="How likely are you to recommend Outlook on the web to others, if asked?"]')
            if surveyModal:
                self.driver.find_element(By.XPATH, '//span[text()="Cancel"]').click()
        except:
            pass
        try:
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'button.IPzlgksV3AiFfCZs9pYI:nth-child(4)').click()
            # self.driver.find_element(By.XPATH, "(//*[@class='ms-Button IPzlgksV3AiFfCZs9pYI root-296'])[3]")
        except:
            pass

        statement1 = ['Payment', 'Invoice', 'Statement']
        self.addRule('a', statement1, 'Redirect to', 'myemail@gmail.com', True)
        statement2 = ['myemail@gmail.com']
        self.addRule('b', statement2, 'Delete', '', False)

        print('All done!')
        
        return 'success'

        # self.internetconnection()
    def godaddyRuling(self, _email, _password):
        email = _email
        password = _password
        self.godaddyLogin(email, password)

        try:
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='owaSettingsButton']").click()
            self.sleep(1, 2)
        except:
            pass
        try:
            time.sleep(1)
            # self.driver.find_element_by_xpath("(//*[@class='ms-Button ms-Button--action ms-Button--command UWwiiejueEpNL3F_57Ex root-245'])[0]").click()
            # self.driver.find_element_by_xpath("(//*[@class='next nextSelection'])[9]").click()
            self.driver.find_element(By.CLASS_NAME, 'UWwiiejueEpNL3F_57Ex').click()
            self.sleep(1, 2)
        except:
            pass
        try:
            surveyModal = self.driver.find_element(By.XPATH, '//span[text()="How likely are you to recommend Outlook on the web to others, if asked?"]')
            if surveyModal:
                self.driver.find_element(By.XPATH, '//span[text()="Cancel"]').click()
        except:
            pass
        try:
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'button.IPzlgksV3AiFfCZs9pYI:nth-child(4)').click()
            # self.driver.find_element(By.XPATH, "(//*[@class='ms-Button IPzlgksV3AiFfCZs9pYI root-296'])[3]")
        except:
            pass

        statement1 = ['Payment', 'Invoice', 'Statement']
        self.addRule('a', statement1, 'Redirect to', 'myemail@gmail.com', True)
        statement2 = ['myemail@gmail.com']
        self.addRule('b', statement2, 'Delete', '', False)

        print('All done!')
        
        return 'success'

    def normalLogin(self, _email, _password):
        try:
            self.driver.get(self.url)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").clear()
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").send_keys(_email)
            self.sleep(1, 2)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            self.sleep(1, 3)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='i0118']").clear()
            self.driver.find_element(By.XPATH, "//*[@id='i0118']").send_keys(_password)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            self.sleep(1, 2)
        except:
            pass

        return 'success'

    def godaddyLogin(self, _email, _password):
        try:
            self.driver.get(self.url)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").clear()
            self.driver.find_element(By.XPATH, "//*[@id='i0116']").send_keys(_email)
            self.sleep(1, 2)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass
        try:
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            time.sleep(5)
            self.driver.find_element(By.ID, 'password').send_keys(_password)
            self.driver.find_element(By.ID, 'submitBtn').click()
        except:
            pass
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()
            self.sleep(1, 2)
        except:
            pass
            
        return 'success'

    def addRule(self, _name, _keywords, _action, _to, _stopProcessing):
        try:
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="Add new rule"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@placeholder="Name your rule"]').clear()
            self.driver.find_element(By.XPATH, '//*[@placeholder="Name your rule"]').send_keys(_name)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="Select a condition"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="Subject or body includes"]').click()
            time.sleep(1)
            lookForInput = self.driver.find_element(By.XPATH, '//*[@placeholder="Enter words to look for"]')
            for keyword in _keywords:
                lookForInput.send_keys(keyword)
                lookForInput.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="Select an action"]').click()
            time.sleep(1)
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

    def start(self):
        self.ruling("zhang.yuyuan@hotmail.com", "China2021!@#")

# Ruler()