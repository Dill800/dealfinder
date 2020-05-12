from flask import Flask, Response, request
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
#import config
import os

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
    
@app.route('/')
def function():
    
    # uncomment for deployment in heroku
    
    chrome_options = webdriver.ChromeOptions();
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    #browser = webdriver.Chrome()

    browser.get('https://www.publix.com/savings/all-deals')

    time.sleep(1)
    
    orig_source = browser.page_source

    try:
        choose_store = browser.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/div/div/button')[0]
        choose_store.click()

        time.sleep(1)

        type_store = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/div/input')[0]
        type_store.send_keys('32612')
        time.sleep(1)
        type_store.send_keys(Keys.ENTER)

        # wait for response
        time.sleep(1)

        village_market = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[2]/div/button')[0]
        village_market.click()
        time.sleep(1)
        browser.get('https://www.publix.com/savings/all-deals/meat')
        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        all = ''

        deal_container = soup.find_all('div', class_='text-block-primary card-title clamp-2')

        for deal in deal_container:
            all += deal.text
            all += '\n'
        
        browser.close()

        print(all)
        print('we good... maybe?')

        return orig_source + '\n' + all
    except:
        print('something is wrong')
        return orig_source + '\n' + 'something went wrong'

@app.route('/sms', methods=['POST'])
def getSales():
    msg = request.form.get('Body')

    
    chrome_options = webdriver.ChromeOptions();
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    

    #msg = 'chicken'

    #browser = webdriver.Chrome()

    browser.get('https://www.publix.com/savings/all-deals')

    time.sleep(1)

    # choose store
    choose_store = browser.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/div/div/button')[0]
    choose_store.click()

    time.sleep(1)

    # enter zip code
    type_store = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/div/input')[0]
    type_store.send_keys('32612')
    time.sleep(1)
    type_store.send_keys(Keys.ENTER)

    time.sleep(1)

    # choose publix near archstone
    village_market = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[2]/div/button')[0]
    village_market.click()
    time.sleep(1)

    # store specified
    browser.get('https://www.publix.com/savings/all-deals')

    time.sleep(2)

    # Check for Feedback popup
    try:
        show_all = browser.find_elements_by_xpath('//*[@id="main"]/div[4]/div[2]/div[2]/div[3]/button')[0]
        show_all.click()
    except:
        # handle
        time.sleep(1)
        exiter = browser.find_elements_by_xpath('//*[@id="fsrInvite"]/section[3]/button[2]')[0]
        exiter.click()
        time.sleep(1)
        show_all = browser.find_elements_by_xpath('//*[@id="main"]/div[4]/div[2]/div[2]/div[3]/button')[0]
        show_all.click()

    # selenium to beautifulsoup
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # itterate thru deals on page
    deal_container = soup.find_all('div', class_='content-wrapper')
    all = ''
    for deal in deal_container:
        
        # add in deal specified by text
        if str(msg).lower() in str(deal.text).lower():

            title = deal.find('div', class_='text-block-primary card-title clamp-2')
            deal_info = deal.find('div', class_='sub-title')

            all += title.text
            if deal_info is not None and len(deal_info.span.text) is not 0:
                all += '\n'
                all += deal_info.span.text

            all += '\n\n'
            
    if len(all) == 0:
        all = 'There are no deals for ' + msg

    #exit browser
    browser.close()

    
    #send client text
    client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])

    client.messages.create(
        to=os.environ['MY_PHONE'],
        from_=os.environ['TWILIO_PHONE'],
        body=all.rstrip()
    )

    return 'done'


def getCategory(category):

    chrome_options = webdriver.ChromeOptions();
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    browser.get('https://www.publix.com/savings/all-deals/' + category)

    time.sleep(1)

    choose_store = browser.find_elements_by_xpath('//*[@id="main"]/div[4]/div[2]/div/div/button')[0]
    choose_store.click()

    time.sleep(1)

    type_store = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/div/input')[0]
    type_store.send_keys('32612')
    time.sleep(1)
    type_store.send_keys(Keys.ENTER)

    # wait for response
    time.sleep(1)

    village_market = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[2]/div/button')[0]
    village_market.click();
    time.sleep(1)
    browser.get('https://www.publix.com/savings/all-deals/' + category)
    time.sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all = ''

    deal_container = soup.find_all('div', class_='content-wrapper')

    for deal in deal_container:
        title = deal.find('div', class_='text-block-primary card-title clamp-2')
        all += title.text

        deal_info = deal.find('div', class_='deal-info')
        if deal_info is not None:
            all += '\n'
            all += deal_info.text

        all += '\n\n'
    
    browser.close()

    return all

if __name__ == '__main__':
    app.run(debug=True)

