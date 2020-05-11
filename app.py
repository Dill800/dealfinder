from flask import Flask, Response, request
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import config
import os

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
'''

print('== Starting... ==')
browser = webdriver.Chrome()
browser.get('https://www.publix.com/savings/all-deals/meat')
choose_store = browser.find_elements_by_xpath('//*[@id="main"]/div[4]/div[2]/div/div/button')[0]
choose_store.click()

time.sleep(1)

type_store = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/div/input')[0]
type_store.send_keys('32612')
time.sleep(1)
type_store.send_keys(Keys.ENTER)

# wait for response
time.sleep(2)

village_market = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[2]/div/button')[0]
village_market.click();
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

browser.get('https://www.publix.com/savings/all-deals/produce')
time.sleep(1)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

deal_container = soup.find_all('div', class_='text-block-primary card-title clamp-2')

for deal in deal_container:
    all += deal.text
    all += '\n'

print(all)
'''
'''
client = Client(os.environ['ACCOUNT_SID'] or config.values['account_sid'], os.environ['AUTH_TOKEN'] or config.values['auth_token'])


client.messages.create(
    to=os.environ['MY_PHONE'] or config.values['my_phone'],
    from_=os.environ['TWILIO_PHONE'] or config.values['twilio_phone'],
    body=all
)
'''





app = Flask(__name__)


@app.route('/')
def function():
    
    '''
    chrome_options = webdriver.ChromeOptions();
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    '''

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

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
        village_market.click();
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
        # OK SO IT ALL WORKS UP TO HERE..... IF WE CAN GET LUCKY WITH THE DEPLOY LOCATION
        # INFO IS STORED IN ALL VAR

        return orig_source + '\n' + all
    except:
        return orig_source + '\n' + 'something went wrong'

@app.route("/sms", methods=['POST'])
def sms_reply():
    '''
    #fetch the message
    msg = request.form.get('Body')
    # create reply
    resp = MessagingResponse()
    answer = getCategory(msg)
    #print(str(answer))
    #default timeout is 15 seconds
    resp.message("You said {}".format(msg))
    '''

    msg = request.form.get('Body')
    answer = getCategory(msg)

    client = Client(config.values['account_sid'], config.values['auth_token'])


    client.messages.create(
        to=config.values['my_phone'],
        from_=config.values['twilio_phone'],
        body=answer
    )

    '''
    f = open("stuff.txt", "a")
    f.write(answer)
    print(answer)
    f.close()
    '''

    return "done loading"

@app.route('/binch')
def fun():
    resp = MessagingResponse()
    resp.message('fuck this man')

    print('this is being called... fallback')

    return str(resp)

@app.route('/yagga')
def yagga():
    return getCategory('meat')

def getCategory(category):

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)

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

    deal_container = soup.find_all('div', class_='text-block-primary card-title clamp-2')

    for deal in deal_container:
        all += deal.text
        all += '\n'
    
    browser.close()

    return all


@app.route('/scrape', methods=['GET'])
def scrape():
    print('== This is where we start scraping ==')

    response = get('https://www.publix.com/savings/all-deals/meat')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(soup)

    deal_container = soup.find_all('div', class_='deal-count')

    for deal in deal_container:
        print("***************")
        print(deal)

    return 'success!'

if __name__ == '__main__':
    app.run(debug=True)

