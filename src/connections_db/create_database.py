import sqlite3

db_tickers = sqlite3.connect("database/tickers.db")
db_tickers.execute("create table dataStock(nome text, info text, ticker text, dy number, precoMinimoCotaEmUmAno "
                   "number, precoMaximoCotaEmUmAno number, dividendoEmUmAno number, oscilacaoCota number, "
                   "valorCota number ,linkSiteRi text, valorizacaoCotaUmAno number, cnpj text);")
db_tickers.commit()
