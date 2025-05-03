import sqlite3

from src.utils.logger import log


class DataLocal:
    def getData(self, ticker: str):
        db = sqlite3.connect("./database/tickers.db")
        data = db.execute(f"select * from dataStock where ticker='{ticker.upper()}'").fetchall()
        log.debug(data[0])
        return {
            "nome": data[0][0],
            "info": data[0][1],
            "ticker": data[0][2],
            "dy": data[0][3],
            "preco_min_cota": data[0][4],
            "preco_max_cota": data[0][5],
            "ultimo_pagamento": data[0][6],
            "oscilacao_cota": data[0][7],
            "valor_cota": data[0][8],
            "linkSiteRi": data[0][9],
            "valorizacaoCota": data[0][10],
            "cnpj": data[0][11],
        }

    def getOrderDatas(self, order: str):
        db = sqlite3.connect("./database/tickers.db")
        datas = db.execute(f"select * from dataStock order by {order}").fetchall()
        datasInJson = []
        for x in datas:
            if x[0] != "":
                datasInJson.append({"data": {
                    "nome": x[0],
                    "info": x[1],
                    "ticker": x[2],
                    "dy": x[3],
                    "preco_min_cota": x[4],
                    "preco_max_cota": x[5],
                    "ultimo_pagamento": x[6],
                    "oscilacao_cota": x[7],
                    "valor_cota": x[8],
                    "linkSiteRi": x[9],
                    "valorizacaoCota": x[10],
                    "cnpj": x[11]}
                })
        return {"result": datasInJson}
