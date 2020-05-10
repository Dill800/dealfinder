from flask import Flask, Response
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

print('== Starting... ==')

browser = webdriver.Chrome()
browser.get('https://www.publix.com/savings/all-deals/meat')
choose_store = browser.find_elements_by_xpath('//*[@id="main"]/div[4]/div[2]/div/div/button')[0]
choose_store.click()

type_store = browser.find_elements_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/div/input')[0]
type_store.send_keys('32612')
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

deal_container = soup.find_all('div', class_='text-block-primary card-title clamp-2')

for deal in deal_container:
    print(deal.text)

browser.get('https://www.publix.com/savings/all-deals/produce')
time.sleep(1)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

deal_container = soup.find_all('div', class_='text-block-primary card-title clamp-2')

for deal in deal_container:
    print(deal.text)






'''

app = Flask(__name__)


@app.route('/')

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

'''