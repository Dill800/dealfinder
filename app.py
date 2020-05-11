from flask import Flask, Response, request
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
#import config
import os

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route('/')
def function():
    
    chrome_options = webdriver.ChromeOptions();
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    browser.get('https://www.publix.com/savings/all-deals/meat')

    time.sleep(1)
    
    orig_source = browser.page_source

    try:
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

        return orig_source + '\n' + all
    except:
        return orig_source + '\n' + 'something went wrong'

@app.route('/test')
def test():
    return getCategory('meat')

@app.route("/sms", methods=['POST'])
def sms_reply():

    msg = request.form.get('Body')
    answer = getCategory(msg)

    #loophole works
    client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])


    client.messages.create(
        to=os.environ['MY_PHONE'],
        from_=os.environ['TWILIO_PHONE'],
        body=answer
    )

    return "done loading"

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

