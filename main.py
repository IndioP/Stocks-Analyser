import streamlit as st

from yahooquery import Ticker
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    code = clean_code(st.text_input("digite o codigo da ação"))
    if code:
        check_code_consistency(code)
        df = get_stock_history(code)
        draw_simple_statistics(df)
        df.index = df.index.droplevel()
        draw_close_price(df)
        draw_volume_graph(df)
        draw_custom_window_moving_average(df)
        draw_moving_average(df)
        draw_pct_change(df,'adjclose')
        plot_distplot(df.adjclose.pct_change())
        #st.dataframe(df.head())

def draw_pct_change(df,column):
    st.title("percentage change")
    fig,ax = plt.subplots(figsize=(10,4))
    df[column].pct_change().plot(legend=True,linestyle='--',marker='o',ax=ax)
    st.pyplot(fig)
    
def plot_distplot(value):
    st.title("distplot")
    fig,ax = plt.subplots(figsize=(10,4))
    sns.distplot(value,bins=100,ax=ax)
    st.pyplot(fig)

def calculate_moving_average(length,values_list):
    return values_list.rolling(window=length).mean()

def draw_custom_window_moving_average(df):
    st.title("custom window moving average")
    length = st.slider('window size',min_value=5,max_value=100,value=10,step=1)
    mv = calculate_moving_average(length,df['volume'])
    draw_simple_graph(mv)

def draw_moving_average(df):
    st.title("moving average")
    
    mv_10 = calculate_moving_average(10,df['volume'])
    mv_20 = calculate_moving_average(20,df['volume'])
    mv_50 = calculate_moving_average(50,df['volume'])
    mvs = pd.concat([mv_10,mv_20,mv_50],axis=1,keys=['moving average with window 10','moving average with window 20','moving average with window 50'])
    draw_simple_graph(mvs)

def draw_simple_statistics(df):
    st.title("Estatisticas simples")
    st.dataframe(df.describe())

def draw_close_price(df):
    st.title("Adjclosing graph")
    draw_simple_graph(df['adjclose'])

def draw_volume_graph(df):
    st.title("Volume Graph")
    draw_simple_graph(df['volume'])

def draw_simple_graph(df):
    fig,ax = plt.subplots(figsize=(10,4))
    df.plot(legend=True,ax=ax)
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