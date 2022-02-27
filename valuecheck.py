import requests
from bs4 import BeautifulSoup
import re

def get_stock_value(symbol):
    
    url = "https://finance.yahoo.com/quote/"+ symbol + "?p="+ symbol + "&.tsrc=fin-srch"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find_all('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find('fin-streamer').text

    return price

def growth_percent(symbol):

    url = "https://finance.yahoo.com/quote/"+ symbol + "?p="+ symbol + "&.tsrc=fin-srch"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find_all('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find('fin-streamer').text
    rate_of_growth = soup.find_all('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find_all('fin-streamer')[1].text
    
    percent = float(rate_of_growth)/float(price)

    return percent

def response_check(symbol):

    url = "https://finance.yahoo.com/quote/"+ symbol + "?p="+ symbol + "&.tsrc=fin-srch"

    response = requests.get(url)

    return response
