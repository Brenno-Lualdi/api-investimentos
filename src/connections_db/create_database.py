import sqlite3

dbTickers = sqlite3.connect("database/tickers.db")
dbTickers.execute("create table dataStock(nome text, info text, ticker text, dy number, precoMinimoCotaEmUmAno "
                  "number, precoMaximoCotaEmUmAno number, dividendoEmUmAno number, oscilacaoCota number, "
                  "valorCota number ,linkSiteRi text, valorizacaoCotaUmAno number, cnpj text);")
dbTickers.commit()
