import sqlite3
import wikipedia

from deep_translator import GoogleTranslator

from src.connections_db.control_data_local import DataLocal
from src.utils.logger import log

info_action = {}


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

    def get_values_local(self):
        return None

    def get_info_wikipedia(self):
        try:
            text = wikipedia.summary("Empresa: " + info_action["nome"], 3)
            return GoogleTranslator(source="auto", target="pt").translate(text)
        except:
            log.error("Não conseguiu pegar da Wikipédia/traduzir")
            return "Nada encontrado...."

    def get_datas_internet(self):
        try:
            info_action["nome"] = self.soup.find("small").text
        except AttributeError:
            pass
        info_action["info"] = self.get_info_wikipedia()
        info_action["ticker"] = self.ticker.upper()

        return info_action

    def get_tag_along(self):
        self.tag_along = self.soup.find_all("strong", attrs={"class": "value"})[6].text
        return self.tag_along

    def get_liquidez_diaria(self):
        self.liquidez_media_diaria = self.soup.find_all("strong", attrs={"class": "value"})[7].text
        return self.liquidez_media_diaria

    def prepare_data(self):
        info_action["dy"] = _get_value_from_str(str(info_action["dy"]))
        info_action["valorizacao_cota"] = _get_value_from_str(str(info_action["valorizacao_cota"]))
        info_action["preco_min_cota"] = _get_value_from_str(str(info_action["preco_min_cota"]))
        info_action["preco_max_cota"] = _get_value_from_str(str(info_action["preco_max_cota"]))
        info_action["ultimo_pagamento"] = _get_value_from_str(str(info_action["ultimo_pagamento"]))
        info_action["oscilacao_cota"] = _get_value_from_str(str(info_action["oscilacao_cota"]))
        info_action["valor_cota"] = _get_value_from_str(str(info_action["valor_cota"]))


# ------------------------------------------

def get_values_money_bdrs(soup):
    info_action["preco_min_cota"] = soup.find_all("strong")[1].text
    info_action["preco_max_cota"] = soup.find_all("strong")[2].text
    info_action["ultimo_pagamento"] = soup.find_all("span")[33].text
    info_action["valor_cota"] = soup.find('strong').text
    info_action["dy"] = soup.find_all("strong")[3].text
    info_action["valorizacao_cota"] = soup.find_all("strong")[4].text
    info_action["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    info_action["cnpj"] = "none"
    info_action["linkSiteRi"] = "none"

    return info_action


# ----------------------------------------

def get_values_money_etfs(soup):
    info_action["valor_cota"] = soup.find('strong').text
    info_action["dy"] = None
    info_action["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    info_action["preco_min_cota"] = soup.find_all("strong")[1].text
    info_action["preco_max_cota"] = soup.find_all("strong")[2].text
    info_action["ultimo_pagamento"] = None
    info_action["cnpj"] = "none"
    info_action["linkSiteRi"] = "none"

    return info_action


# -----------------------

def get_values_money_stocks(soup):
    try:
        info_action["dy"] = soup.find_all("div", {'title': 'Dividend Yield com base nos últimos 12 meses'})[0].find(
            'strong').text
    except:
        info_action["dy"] = 0
    info_action["preco_min_cota"] = soup.find_all("div", {'title': 'Valor mínimo das últimas 52 semanas'})[0].find(
        'strong').text
    info_action["preco_max_cota"] = soup.find_all("div", {'title': 'Valor máximo das últimas 52 semanas'})[0].find(
        'strong').text

    info_action["ultimo_pagamento"] = (soup.find('div', {"id": "earning-section"})
                                       .select("div > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > "
                                               "td:nth-child(3)"))[0].text
    info_action["valor_cota"] = soup.find_all("div", {'title': 'Valor atual do ativo'})[0].find('strong').text
    info_action["oscilacao_cota"] = \
        soup.find_all("span", {'title': 'Variação do valor do ativo com base no dia anterior'})[0].find('b').text
    try:
        info_action["valorizacao_cota"] = soup.find_all("div", {'title': 'Valorização no preço do ativo com base nos '
                                                                         'últimos 12 meses'})[0].find('strong').text
    except:
        log.error(soup.find_all("strong", attrs={"class": "value"}))
        info_action["valorizacao_cota"] = 0.0
    try:
        info_action["cnpj"] = soup.find_all("small", attrs={"class": "d-block fs-4 fw-100 lh-4"})[0].text
    except:
        log.error(soup.find_all("small", attrs={"class": "d-block fs-4 fw-100 lh-4"}))
        info_action["cnpj"] = None
    try:
        info_action["linkSiteRi"] = soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow",
                                                              "class": "waves-effect waves-light btn btn-small "
                                                                       "btn-secondary"})[0]["href"]
    except:
        log.error(soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow",
                                            "class": "waves-effect waves-light btn btn-small btn-secondary"}))
        info_action["linkSiteRi"] = None

    return info_action


# -----------------------

def get_values_money_fiis(soup):
    info_action["preco_min_cota"] = soup.find_all("strong")[1].text
    info_action["preco_max_cota"] = soup.find_all("strong")[2].text
    info_action["ultimo_pagamento"] = soup.find_all("span")[33].text
    info_action["valor_cota"] = soup.find('strong').text
    info_action["dy"] = soup.find_all("strong")[3].text
    info_action["oscilacao_cota"] = soup.find_all('b')[11].text.strip("\n").lstrip().rstrip()
    info_action["valorizacao_cota"] = soup.find_all("strong", attrs={"class": "value"})[4].text
    info_action["cnpj"] = soup.find_all("strong", attrs={"class": "value"})[28].text
    info_action["linkSiteRi"] = "none"

    return info_action


# --------------------------

def get_all_values_from_nav(soup, ticker, stock_type):
    comand_basics = BasicData(soup, ticker)
    comand_basics.get_datas_internet()

    if 'acoes' in stock_type:
        info_action = get_values_money_stocks(soup)
    elif 'fundos-imobiliarios' in stock_type:
        info_action = get_values_money_fiis(soup)
    elif 'etfs' in stock_type:
        info_action = get_values_money_etfs(soup)
    else:
        info_action = get_values_money_bdrs(soup)

    comand_basics.prepare_data()
    DataLocal().write_data(info_action)
    return info_action
