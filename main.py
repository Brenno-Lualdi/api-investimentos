import uvicorn
from fastapi import FastAPI
from src.connections_db.control_data_local import DataLocal

app = FastAPI(debug=False)

info_action = {"data": {}}


@app.get("/get-ticker/{ticker}")
async def getTicker(ticker: str):
    dataLocal = DataLocal()
    info_action["data"] = dataLocal.get_data(ticker)
    return info_action


@app.get("/get-tickers")
async def getTickers():
    dataLocal = DataLocal()
    return dataLocal.get_order_datas("oscilacaoCota")


@app.get("/get-stocks-by-order/{order}")
async def getStocksByOrder(order: str):
    dataLocal = DataLocal()
    return dataLocal.get_order_datas(order)


uvicorn.run(app, host="localhost", port=8000)
