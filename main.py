import uvicorn
from fastapi import FastAPI
from src.connections_db.get_data_local import DataLocal

app = FastAPI(debug=False)

infoAction = {"data": {}}


@app.get("/get-ticker/{ticker}")
async def getTicker(ticker: str):
    dataLocal = DataLocal()
    infoAction["data"] = dataLocal.getData(ticker)
    return infoAction


@app.get("/get-tickers")
async def getTickers():
    dataLocal = DataLocal()
    return dataLocal.getOrderDatas("oscilacaoCota")


@app.get("/get-stocks-by-order/{order}")
async def getStocksByOrder(order: str):
    dataLocal = DataLocal()
    return dataLocal.getOrderDatas(order)


uvicorn.run(app, host="localhost", port=8000)
