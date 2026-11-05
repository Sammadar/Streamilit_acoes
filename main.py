import os
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import yfinance as yf
from millify import millify

st.set_page_config(page_title='Carteira de ações', page_icon='📈', layout='wide')

# A carteira fica no acoes.csv ao lado deste arquivo (ticker, quantidade).
CSV_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acoes.csv')
csv = pd.read_csv(CSV_LOCAL)
carteira = csv.set_index('ticker')['quantidade'].to_dict()


@st.cache_data(ttl=300)
def baixar(ticker, **kwargs):
    """Busca as cotações no Yahoo Finance; devolve um DataFrame vazio se a consulta falhar."""
    try:
        return yf.download(ticker, multi_level_index=False, progress=False, **kwargs)
    except Exception:
        return pd.DataFrame()


tab1, tab2 = st.tabs(['Carteira', 'Histórico de ações'])

with tab1:
    st.title('Carteira')
    for ticker, quantidade in carteira.items():
        dados = baixar(ticker, period='5d')
        st.subheader(ticker)
        if dados.empty or len(dados) < 2:
            st.warning(f'Sem cotação para {ticker} agora. Verifique o ticker ou a conexão com o Yahoo Finance.')
            continue
        fechamento_atual = float(dados['Close'].iloc[-1])
        fechamento_anterior = float(dados['Close'].iloc[-2])
        valor_atual = quantidade * fechamento_atual
        valor_anterior = quantidade * fechamento_anterior
        diferenca = valor_atual - valor_anterior
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Quantidade', millify(quantidade, 2), millify(diferenca, 2))
        with col2:
            st.metric('Valor atual', millify(valor_atual, 2))
        with col3:
            st.metric('Valor anterior', millify(valor_anterior, 2))

with tab2:
    st.title('Histórico de ações')
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.selectbox('Ação', list(carteira.keys()))
    with col2:
        data_inicial = st.date_input('Data inicial', value=datetime.today() - timedelta(days=30))
    with col3:
        data_final = st.date_input('Data final', value='today', max_value='today')
    historico = baixar(ticker, start=data_inicial, end=data_final)
    if historico.empty:
        st.warning(f'Sem histórico para {ticker} nesse período.')
    else:
        st.line_chart(historico['Close'])
