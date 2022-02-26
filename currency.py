import requests
from bs4 import BeautifulSoup

def currency_covnertion(curr):
    curre = str(curr)
    page = requests.get("https://www.x-rates.com/calculator/?from=" + curr + "&to=USD&amount=1")
    soup = BeautifulSoup(page.text, 'html.parser')

    rate = soup.find(class_="ccOutputTrail").previous_sibling

    return rate


# curr = "CHF"

# cena_w_uds = 10
# cena_w_chf = float(cena_w_uds / float(currency_covnertion(curr)))

# print(cena_w_chf)
