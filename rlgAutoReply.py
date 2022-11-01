from bs4 import BeautifulSoup
import os
from proto import MESSAGE
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Config
EMAIL = ''
PASSWORD = ''
MESSAGE = 'This is auto message. If you okay with prices directly add me. Im not checking chat messages.'

def init():
    
    firefox_options = FirefoxOptions()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options, executable_path='geckodriver.exe')
    driver.set_window_size(2620, 1080)

    driver.get("https://rocket-league.com/login")
    driver.find_element_by_id("acceptPrivacyPolicy").click()
    driver.find_element_by_name("email").send_keys(EMAIL)
    driver.find_element_by_name("password").send_keys(PASSWORD)
    driver.find_element_by_name("submit").click()

    driver.get("https://rocket-league.com/chat")
    source = BeautifulSoup(driver.page_source,"lxml")

    sleep(1)
    
    while True:
        sleep(1)
        source = BeautifulSoup(driver.page_source,"lxml")
        newMessage = source.find('a', {'class': 'rlg-chat__thread --new'}) or source.find('a', {'class': 'rlg-chat__thread --is-user --new --not-archived'})
        
        if  newMessage != None: # Eger yeni mesaj var ise
            newMessage = str(newMessage).strip().replace('\n','')
            messageSource = BeautifulSoup(newMessage,"html.parser")
            userName = messageSource.find('img')['alt']
            print('New message from ', userName)
            driver.find_element_by_id('message-thread-' + userName).click()
            sleep(1)
            driver.execute_script("window.scrollTo(0, 300)")
            sleep(0.5)
            driver.find_element_by_id('messagetext').send_keys(MESSAGE)
            driver.find_element_by_id('user-message-send-reply').click()
            
if __name__ == '__main__':
    init()