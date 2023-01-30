import streamlit as st

from yahooquery import Ticker
import pandas as pd
import re
import matplotlib.pyplot as plt

def main():
    code = clean_code(st.text_input("digite o codigo da ação"))
    if code:
        check_code_consistency(code)
        df = get_stock_history(code)
        draw_simple_statistics(df)
        df.index = df.index.droplevel()
        draw_close_price(df)
        #st.dataframe(df.head())

def draw_simple_statistics(df):
    st.title("Estatisticas simples")
    st.dataframe(df.describe())

def draw_close_price(df):
    st.title("Grafico do closing price")
    fig,ax = plt.subplots(figsize=(10,4))
    df.adjclose.plot(legend=True,ax=ax)
    #fig.legend()
    st.pyplot(fig)

def clean_code(code):
    code = code.strip()
    code = code.upper()
    return code

#The US and European stock exchanges normally use stock codes of 3-4 letters that often closely represent the company name, like EZJ for Easyjet.
def check_code_consistency(code):
    check_code_len(code)
    isAlpha(code)

def check_code_len(code):
    assert(len(code) > 2 and len(code) < 5)

def isAlpha(code):
    assert(re.search('[^A-Z]',code) == None)

def get_stock_history(code,period='120d',interval='1d'):
    return Ticker(code).history(period = period,  interval = interval)

if __name__=='__main__':
    main()