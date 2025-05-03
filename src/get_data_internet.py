import sqlite3
import wikipedia

from deep_translator import GoogleTranslator

from src.utils.logger import log

infoAction = {}
dataJson = {}


def _get_value_from_str(value: str) -> float:
    """
    Convert a string value to a float, handling commas and percentage signs.
    """
    try:
        return float(value.replace(",", ".").replace("%", "").replace("R$ ", ""))
    except ValueError:
        return 0.0


class BasicData:
    def __init__(self, soup, ticker: str):
        self.soup = soup
        self.ticker = ticker

    def getValuesLocal(self):
        return None

    def getInfoWikipedia(self):
        try:
            text = wikipedia.summary("Empresa: " + infoAction["nome"], 3)
            return GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            log.error("Não conseguiu pegar da Wikipédia/traduzir")
            return "Nada encontrado...."

    def getDatasInternet(self):
        try:
            infoAction["nome"] = self.soup.find("small").text
        except AttributeError:
            pass
        infoAction["info"] = self.getInfoWikipedia()
        infoAction["ticker"] = self.ticker.upper()

        return infoAction

    def getTagAlong(self):
        self.tagAlong = self.soup.find_all("strong", attrs={"class": "value"})[6].text
        return self.tagAlong

    def getLiquidezDiaria(self):
        self.liquidezMediaDiaria = self.soup.find_all("strong", attrs={"class": "value"})[7].text
        return self.liquidezMediaDiaria

    def writeData(self, infoAction):
        db = sqlite3.connect("./database/tickers.db")

        infoAction["dy"] = _get_value_from_str(str(infoAction["dy"]))
        infoAction["valorizacaoCota"] = _get_value_from_str(str(infoAction["valorizacaoCota"]))
        infoAction["preco_min_cota"] = _get_value_from_str(str(infoAction["preco_min_cota"]))
        infoAction["preco_max_cota"] = _get_value_from_str(str(infoAction["preco_max_cota"]))
        infoAction["ultimo_pagamento"] = _get_value_from_str(str(infoAction["ultimo_pagamento"]))
        infoAction["oscilacao_cota"] = _get_value_from_str(str(infoAction["oscilacao_cota"]))
        infoAction["valor_cota"] = _get_value_from_str(str(infoAction["valor_cota"]))

        if len(db.execute(f"select * from dataStock where ticker='{self.ticker}'").fetchall()) >= 1:
            db.execute(
                f"update dataStock SET dy={infoAction['dy']}, precoMinimoCotaEmUmAno={infoAction['preco_min_cota']}, precoMaximoCotaEmUmAno={infoAction['preco_max_cota']}, dividendoEmUmAno={infoAction['ultimo_pagamento']}, oscilacaoCota={infoAction['oscilacao_cota']}, valorCota={infoAction['valor_cota']}, cnpj='{infoAction['cnpj']}', linkSiteRi='{infoAction['linkSiteRi']}', valorizacaoCotaUmAno={infoAction['valorizacaoCota']} where ticker='{infoAction['ticker']}'")
            log.debug("Ação atualizada")
        else:
            db.execute(
                f"insert into dataStock values('{infoAction['nome']}','Nada sobre....','{infoAction['ticker']}',{infoAction['dy']},{infoAction['preco_min_cota']},{infoAction['preco_max_cota']}, {infoAction['ultimo_pagamento']}, {infoAction['oscilacao_cota']},{infoAction['valor_cota']}, '{infoAction['linkSiteRi']}', {infoAction['valorizacaoCota']}, '{infoAction['cnpj']}');")
            log.debug("Ação inserida")
        db.commit()
        return infoAction


# ------------------------------------------

def getValuesMoneyBdrs(soup):
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[33].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = soup.find_all("strong")[3].text
    infoAction["valorizacaoCota"] = soup.find_all("strong")[4].text
    infoAction["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    infoAction["cnpj"] = "none"
    infoAction["linkSiteRi"] = "none"

    return infoAction


def getAllValuesBdrs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyBdrs(soup)
    comandBasics.writeData(infoAction)
    return infoAction


# ----------------------------------------

def getValuesMoneyEtfs(soup):
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = None
    infoAction["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = None
    infoAction["cnpj"] = "none"
    infoAction["linkSiteRi"] = "none"

    return infoAction


def getAllValuesEtfs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyEtfs(soup)
    comandBasics.writeData(infoAction)
    return infoAction


# -----------------------

def getValuesMoneyStocks(soup):
    try:
        infoAction["dy"] = soup.find_all("strong")[3].text
    except IndexError:
        infoAction["dy"] = soup.find("strong")
    except:
        infoAction["dy"] = 0
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[32].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    try:
        infoAction["valorizacaoCota"] = soup.find_all("strong", attrs={"class": "value"})[4].text
    except:
        log.error(soup.find_all("strong", attrs={"class": "value"}))
        infoAction["valorizacaoCota"] = 0.0
    try:
        infoAction["cnpj"] = soup.find_all("small", attrs={"class": "d-block fs-4 fw-100 lh-4"})[0].text
    except:
        log.error(soup.find_all("small", attrs={"class": "d-block fs-4 fw-100 lh-4"}))
        infoAction["cnpj"] = None
    try:
        infoAction["linkSiteRi"] = soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow",
                                                             "class": "waves-effect waves-light btn btn-small btn-secondary"})[
            0]["href"]
    except:
        log.error(soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow",
                                            "class": "waves-effect waves-light btn btn-small btn-secondary"}))
        infoAction["linkSiteRi"] = None

    return infoAction


def getAllValuesStocks(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyStocks(soup)
    comandBasics.writeData(infoAction)
    return infoAction


# -----------------------

def getValuesMoneyFiis(soup):
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[33].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = soup.find_all("strong")[3].text
    infoAction["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    infoAction["valorizacaoCota"] = soup.find_all("strong", attrs={"class": "value"})[4].text
    infoAction["cnpj"] = soup.find_all("strong", attrs={"class": "value"})[28].text
    infoAction["linkSiteRi"] = "none"

    return infoAction


def getAllValuesFiis(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyFiis(soup)
    comandBasics.writeData(infoAction)
    return infoAction
