import requests
from bs4 import BeautifulSoup

def get_stock_value(symbol):
    
    url = "https://finance.yahoo.com/quote/"+ symbol + "?p="+ symbol + "&.tsrc=fin-srch"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find_all('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find('fin-streamer').text

    return price