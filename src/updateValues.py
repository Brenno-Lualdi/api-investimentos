import numpy
import requests
from lists import fiis, bdrs, stocks, etfs
from bs4 import BeautifulSoup
from get_data_internet import getAllValuesFiis, getAllValuesStocks, getAllValuesEtfs, getAllValuesBdrs
from src.utils.logger import log

totalLengthStocks = len(stocks) + len(fiis) + len(bdrs) + len(etfs)
totalStocks = stocks
totalStocks = numpy.append(totalStocks, fiis)
totalStocks = numpy.append(totalStocks, bdrs)
totalStocks = numpy.append(totalStocks, etfs)

log.debug("Rodando dnv")
for x in range(1, totalLengthStocks):
    typeStock = totalStocks[x]
    if typeStock in stocks:

        response = requests.get(
            f"https://statusinvest.com.br/acoes/{typeStock}", headers={"User-Agent": "Mozilla/5.0"})
        nav = BeautifulSoup(response.text, "html5lib")

        infoAction = getAllValuesStocks(nav, stocks[x].upper())
        log.debug(f"Atualizando a ação: {typeStock}")

    elif typeStock in fiis:

        response = requests.get(
            f"https://statusinvest.com.br/fundos-imobiliarios/{typeStock}", headers={"User-Agent": "Mozilla/5.0"})
        nav = BeautifulSoup(response.text, "html5lib")

        infoAction = getAllValuesFiis(nav, typeStock.upper())
        log.debug(f"Atualizando o fundo: {typeStock}")

    elif typeStock in etfs:
        response = requests.get(
            f"https://statusinvest.com.br/etfs/{typeStock}", headers={"User-Agent": "Mozilla/5.0"})
        nav = BeautifulSoup(response.text, "html5lib")

        infoAction = getAllValuesEtfs(nav, typeStock.upper())
        log.debug(f"Atualizando o ETF: {typeStock}")

    else:
        response = requests.get(
            f"https://statusinvest.com.br/bdrs/{typeStock}", headers={"User-Agent": "Mozilla/5.0"})
        nav = BeautifulSoup(response.text, "html5lib")

        infoAction = getAllValuesBdrs(nav, typeStock.upper())
        log.debug(f"Atualizando o BDR: {typeStock}")
