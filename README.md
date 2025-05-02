# API Ações
### API simples que retorna: Preço, DY, ultimo valor em dividendos, preço mínimo em 12 meses, preço maxímo em 12 meses, oscilação diária, oscilação anual, cnpj e link do site de RI.

### Libs Utilizadas:
- Fast API
- numpy
- sqlite3
- beautifulSoup4

### Descrição do Funcionamento:
Ao executar: <code>python main.py</code>, Fast API irá executar localmente na porta 8000(no debug), abrindo as seguintes rotas: 
  - docs (rota padrão do Fast API)
  - get-tickers
  - get-ticker/{nome da ação. exemplo: petr4}
  - get-tickers-by-order/{exemplo: valor_cota}
  - get-values-cryptos

Ao executar: <code>python updateValues.py</code>, será feito web-scraping com bs4(Beautiful Soup) no site <a href="https://statusinvest.com.br">Status Invest</a>, onde irá atualizar os tickers(FIIs, BDRs, ETFs e Ações).


Forked from: https://github.com/ramonpaolo/api-b3