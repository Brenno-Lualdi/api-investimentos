import numpy
import requests
from lists import fiis, bdrs, stocks, etfs
from bs4 import BeautifulSoup
from get_data_internet import get_all_values_from_nav
from src.utils.logger import log

totalLengthStocks = len(stocks) + len(fiis) + len(bdrs) + len(etfs)
total_stocks = stocks
total_stocks = numpy.append(total_stocks, fiis)
total_stocks = numpy.append(total_stocks, bdrs)
total_stocks = numpy.append(total_stocks, etfs)

log.debug("Rodando dnv")
for x in range(1, totalLengthStocks):
    ticker = total_stocks[x]

    if ticker in stocks:
        stock_type = 'acoes'
    elif ticker in fiis:
        stock_type = 'fundos-imobiliarios'
    elif ticker in etfs:
        stock_type = 'etfs'
    else:
        stock_type = 'bdrs'

    url = f"https://statusinvest.com.br/{stock_type}/{ticker}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    nav = BeautifulSoup(response.text, "html5lib")
    infoAction = get_all_values_from_nav(nav, ticker.upper(), stock_type)
