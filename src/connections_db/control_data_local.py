import os
import sqlite3

from src.utils.logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "tickers.db")


class DataLocal:
    def get_data(self, ticker: str):
        db = sqlite3.connect(DB_PATH)
        data = db.execute(f"select * from dataStock where ticker='{ticker.upper()}'").fetchall()
        db.close()
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

    def get_order_datas(self, order: str):
        db = sqlite3.connect(DB_PATH)
        datas = db.execute(f"select * from dataStock order by {order}").fetchall()
        db.close()
        datas_in_json = []
        for x in datas:
            if x[0] != "":
                datas_in_json.append({"data": {
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
        return {"result": datas_in_json}

    def write_data(self, info_action):
        db = sqlite3.connect(DB_PATH)
        try:
            if len(db.execute(f"select * from dataStock where ticker='{info_action['ticker']}'").fetchall()) >= 1:
                db.execute(
                    f"update dataStock SET dy={info_action['dy']}, precoMinimoCotaEmUmAno={info_action['preco_min_cota']}, "
                    f"precoMaximoCotaEmUmAno={info_action['preco_max_cota']}, dividendoEmUmAno="
                    f"{info_action['ultimo_pagamento']}, oscilacaoCota={info_action['oscilacao_cota']}, valorCota="
                    f"{info_action['valor_cota']}, cnpj='{info_action['cnpj']}', linkSiteRi='{info_action['linkSiteRi']}', "
                    f"valorizacaoCotaUmAno={info_action['valorizacao_cota']}, tagAlong={info_action['tag_along']}, "
                    f"setor='{info_action['setor']}', subSetor='{info_action['sub_setor']}', segmento='{info_action['segmento']}' "
                    f"where ticker='{info_action['ticker']}'")
                log.debug("Ação atualizada")
            else:
                db.execute(
                    f"insert into dataStock values('{info_action['nome']}','Nada sobre....','{info_action['ticker']}',"
                    f"{info_action['dy']},{info_action['preco_min_cota']},{info_action['preco_max_cota']}, "
                    f"{info_action['ultimo_pagamento']}, {info_action['oscilacao_cota']},{info_action['valor_cota']}, "
                    f"'{info_action['linkSiteRi']}', {info_action['valorizacao_cota']}, '{info_action['cnpj']}', {info_action['tag_along']}, "
                    f"'{info_action['setor']}', '{info_action['sub_setor']}', '{info_action['segmento']}');")
                log.debug("Ação inserida")
        except:
            log.error(f"Erro ao inserir/atualizar a ação {info_action['ticker']}")
        db.commit()
        db.close()
        return info_action
