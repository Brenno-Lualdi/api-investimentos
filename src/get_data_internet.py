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
            text = wikipedia.summary(info_action["nome"], 3)
            return GoogleTranslator(source="auto", target="pt").translate(text)
        except:
            log.error(f'Não conseguiu pegar informação da {info_action["nome"]} na Wikipédia/traduzir')
            return "Nada encontrado...."

    def get_datas_internet(self):
        try:
            info_action["nome"] = self.soup.find("small").text
        except AttributeError:
            pass
        info_action["info"] = self.get_info_wikipedia()
        info_action["ticker"] = self.ticker.upper()

        return info_action

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
        info_action["tag_along"] = _get_value_from_str(str(info_action["tag_along"]))


# ------------------------------------------

def get_values_money_bdrs(soup):
    info_action["cnpj"] = "none"
    info_action["linkSiteRi"] = "none"

    return info_action


# ----------------------------------------

def get_values_money_etfs(soup):
    info_action["dy"] = None
    info_action["ultimo_pagamento"] = None
    info_action["cnpj"] = "none"
    info_action["linkSiteRi"] = "none"

    return info_action


# -----------------------

def get_generic_money_values(soup):
    try:
        info_action["dy"] = soup.find_all("div", {'title': 'Dividend Yield com base nos últimos 12 meses'})[0].find(
            'strong').text
    except:
        info_action["dy"] = 0
    try:
        info_action["preco_min_cota"] = soup.find_all("div", {'title': 'Valor mínimo das últimas 52 semanas'})[0].find(
            'strong').text
    except:
        info_action["preco_min_cota"] = 0
    try:
        info_action["preco_max_cota"] = soup.find_all("div", {'title': 'Valor máximo das últimas 52 semanas'})[0].find(
            'strong').text
    except:
        info_action["preco_max_cota"] = 0

    try:
        info_action["ultimo_pagamento"] = (soup.find('div', {"id": "earning-section"})
                                           .select("div > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > "
                                                   "td:nth-child(3)"))[0].text
    except:
        info_action["ultimo_pagamento"] = 0

    try:
        info_action["valor_cota"] = soup.find_all("div", {'title': 'Valor atual do ativo'})[0].find('strong').text
    except:
        info_action["valor_cota"] = 0
    try:
        oscilation = soup.find_all("div", {'title': 'Variação do valor do ativo com base no dia anterior'})[0]
        signal = '+' if 'upward' in oscilation.find('i').text else '-'
        info_action["oscilacao_cota"] = signal + oscilation.find('b').text
    except:
        info_action["oscilacao_cota"] = 0
    try:
        info_action["valorizacao_cota"] = soup.find_all("div", {'title': 'Valorização no preço do ativo com base nos '
                                                                         'últimos 12 meses'})[0].find('strong').text
    except:
        info_action["valorizacao_cota"] = 0.0
    try:
        info_action["cnpj"] = soup.find_all("small", attrs={"class": "d-block fs-4 fw-100 lh-4"})[0].text
    except:
        info_action["cnpj"] = None
    try:
        info_action["linkSiteRi"] = soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow",
                                                              "class": "waves-effect waves-light btn btn-small "
                                                                       "btn-secondary"})[0]["href"]
    except:
        info_action["linkSiteRi"] = None

    try:
        info_action["tag_along"] = (soup.select('#main-2 > div:nth-child(4) > div > div.mb-5 > div > div > '
                                                'div:nth-child(2) > div > div > div > strong'))[0].text.replace(' %',
                                                                                                                '')
    except:
        info_action["tag_along"] = 0

    return info_action


# -----------------------

def get_values_money_fiis(soup):
    info_action["cnpj"] = soup.find_all("strong", attrs={"class": "value"})[28].text
    info_action["linkSiteRi"] = "none"

    pre_setor = soup.find_all("div", {'class': 'company'})[0] \
        .select('div > div.card.bg-main-gd-h.white-text.rounded.pt-1.pb-1 > div')[0]

    try:
        info_action["setor"] = pre_setor.select('div:nth-child(1) > div > div > div > a > strong')[0].text
    except:
        info_action["setor"] = None

    try:
        info_action["sub_setor"] = pre_setor.select('div:nth-child(2) > div > div > div > a > strong')[0].text
    except:
        info_action["sub_setor"] = None

    try:
        info_action["segmento"] = pre_setor.select('div:nth-child(3) > div > div > div > a > strong')[0].text
    except:
        info_action["segmento"] = None

    return info_action


# --------------------------

def get_values_stocks(soup):
    try:
        pre_setor = soup.find_all("div", {'id': 'company-section'})[0] \
            .select('div:nth-child(1) > div > div.card.bg-main-gd-h.white-text.rounded.ov-hidden.pt-0.pb-0 > div')[0]
    except:
        pre_setor = soup.find_all("div", {'class': 'company'})[0] \
            .select('div > div.card.bg-main-gd-h.white-text.rounded.pt-1.pb-1 > div')[0]
    try:
        info_action["setor"] = pre_setor.select('div:nth-child(1) > div > div > div > a > strong')[0].text
    except:
        info_action["setor"] = None

    try:
        info_action["sub_setor"] = pre_setor.select('div:nth-child(2) > div > div > div > a > strong')[0].text
    except:
        info_action["sub_setor"] = None

    try:
        info_action["segmento"] = pre_setor.select('div:nth-child(3) > div > div > div > a > strong')[0].text
    except:
        info_action["segmento"] = None


def get_all_values_from_nav(soup, ticker, stock_type):
    comand_basics = BasicData(soup, ticker)
    info_action = {}  # Initialize info_action as an empty dictionary
    comand_basics.get_datas_internet()
    info_action = get_generic_money_values(soup)

    if 'acoes' in stock_type:
        get_values_stocks(soup)
        pass
    elif 'fundos-imobiliarios' in stock_type:
        get_values_money_fiis(soup)
    elif 'etfs' in stock_type:
        get_values_money_etfs(soup)
    else:
        get_values_money_bdrs(soup)

    comand_basics.prepare_data()
    DataLocal().write_data(info_action)
    return info_action
