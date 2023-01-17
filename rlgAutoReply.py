from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from time import sleep, time

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Config
EMAIL = ''
PASSWORD = ''
MESSAGE = 'This is auto message. If you okay with prices directly add me. Im not checking chat messages.'
REFRESH_TIMEOUT = 180

def init():
    
    firefox_options = FirefoxOptions()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options, service=Service(executable_path='geckodriver.exe'))
    driver.set_window_size(2620, 1080)

    driver.get("https://rocket-league.com/login")
    driver.find_element("id", "acceptPrivacyPolicy").click()
    driver.find_element("name", "email").send_keys(EMAIL)
    driver.find_element("name", "password").send_keys(PASSWORD)
    driver.find_element("name", "submit").click()

    driver.get("https://rocket-league.com/chat")
    source = BeautifulSoup(driver.page_source,"lxml")

    sleep(1)
    tempTime = time()
    while True:
        sleep(1)
        source = BeautifulSoup(driver.page_source,"lxml")
        newMessage = source.find('a', {'class': 'rlg-chat__thread --new'}) or source.find('a', {'class': 'rlg-chat__thread --is-user --new --not-archived'})
        
        if  newMessage != None: # Eger yeni mesaj var ise
            newMessage = str(newMessage).strip().replace('\n','')
            messageSource = BeautifulSoup(newMessage,"html.parser")
            userName = messageSource.find('img')['alt']
            print('New message from ', userName)
            driver.find_element("id", 'message-thread-' + userName).click()
            sleep(1)
            driver.execute_script("window.scrollTo(0, 300)")
            sleep(0.5)
            driver.find_element("id", 'messagetext').send_keys(MESSAGE)
            driver.find_element("id", 'user-message-send-reply').click()

        if time() - tempTime > REFRESH_TIMEOUT:
            driver.refresh()
            tempTime = time()
            
if __name__ == '__main__':
    init()