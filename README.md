# Carteira de ações em Streamlit

Painel que acompanha uma carteira de ações com cotações ao vivo. A carteira fica num CSV
(`acoes.csv`, colunas `ticker` e `quantidade`); o app busca os preços no Yahoo Finance e mostra,
para cada papel, o valor atual da posição e a variação em relação ao dia anterior. Uma segunda
aba traça o histórico de fechamento de qualquer ação da carteira no período que você escolher.

Projeto de estudo de Streamlit e da biblioteca `yfinance`.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run main.py
```

Edite `acoes.csv` para montar a sua carteira. Os tickers seguem o padrão do Yahoo Finance
(`PETR4.SA`, `TAEE11.SA`, `^BVSP` para o Ibovespa).

## O que tem

- **Carteira**: um bloco por ação com quantidade, valor atual e valor do dia anterior, com a
  diferença destacada.
- **Histórico**: seleção da ação e do intervalo de datas, gráfico de linha com o fechamento.

Python · Streamlit · yfinance · Pandas · millify
