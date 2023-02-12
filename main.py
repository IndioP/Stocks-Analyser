import streamlit as st

from yahooquery import Ticker
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    prompt = clean_code(st.text_input("Type the stock code, if you want to make correlation analysis you can place two codes separated by a single whitespace",placeholder='AAPL'))
    if prompt:
        #check_code_consistency(prompt)
        prompt = clean_code(prompt)
        codes = prompt.split()
        if len(codes) > 1:
            dual_stock_analysis(codes)
        else:
            single_stock_analysis(codes[0])
        
        
        
def dual_stock_analysis(codes):
    dfs = {}
    for code in codes:
        dfs[code] = get_stock_history(code,'240d','1d')
        st.title(code)
        draw_simple_statistics(dfs[code])
    
    df = pd.DataFrame()
    for key in dfs:
        dfs[key].index = dfs[key].index.droplevel()
        df[key] = dfs[key]['adjclose']
    tech_rets = df.pct_change()
    plot_pair_grid(tech_rets)
    plot_correlation_matrix(tech_rets)
    plot_risk_vs_expected_return(tech_rets)

def plot_risk_vs_expected_return(rets):
    means = rets.mean()
    stds = rets.std()

    fig,ax = plt.subplots(figsize=(10,4))
    ax.scatter(means, stds,alpha = 0.5)
    ax.set_xlabel('Expected returns')
    ax.set_ylabel('Risk')
    
    for label, x, y in zip(rets.columns, means, stds):
        ax.annotate(
            label, xy = (x, y), xytext = (30, 30),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=-0.3',color='indianred'))
    st.pyplot(fig)
    


def plot_correlation_matrix(df):
    st.title("Correlation Matrix")
    fig,ax = plt.subplots(figsize=(10,4))
    sns.heatmap(df.dropna().corr(),annot=True,ax=ax)
    st.pyplot(fig)
    

def plot_pair_grid(df):
    st.title("PairGrid")
    draw_pairgrid(df)

def draw_pairgrid(df):
    fig = sns.PairGrid(df.dropna())
    fig.map_upper(plt.scatter,color='purple')
    fig.map_lower(sns.kdeplot,cmap='cool_d')
    fig.map_diag(plt.hist,bins=40)
    st.pyplot(fig)

def single_stock_analysis(code):
    df = get_stock_history(code,'240d','1d')
    draw_simple_statistics(df)
    df.index = df.index.droplevel()
    draw_close_price(df)
    draw_volume_graph(df)
    draw_custom_window_boiler_bands(df,'adjclose')
    draw_moving_average(df)
    draw_pct_change(df,'adjclose')
    plot_distplot(df.adjclose.pct_change())
    draw_MACD(df,'adjclose')
    

def calculate_exponential_moving_average(df,span):
    return df.ewm(span=span,adjust=False).mean()

def calculate_MACD(df,column):
    EMA_12 = calculate_exponential_moving_average(df[column],12)
    EMA_26 = calculate_exponential_moving_average(df[column],26)
    MACD = EMA_12 - EMA_26
    signal_line = calculate_exponential_moving_average(MACD,9)
    return EMA_12,EMA_26,MACD,signal_line

def draw_MACD(df,column):
    EMA_12,EMA_26,MACD,signal_line = calculate_MACD(df,column)
    st.title('MACD vs Signal')
    fig,ax = plt.subplots(nrows=2,figsize=(10,4))
    ax[0].plot(EMA_12,color='blue',label='Exponential Moving Average 12')
    ax[0].plot(EMA_26,color='orange',label='Exponential Moving Average 26')
    ax[0].legend()
    ax[1].plot(MACD,label='MACD',color='pink')
    ax[1].plot(signal_line,label='Signal Line',color='Purple')
    ax[1].legend()
    b = st.checkbox(label='show buy sell anotations?')
    if b:
        draw_annotators(signal_line,MACD,df,ax[1])
    st.pyplot(fig)

def draw_annotators(signal,line,df,ax):
    aux = signal - line
    df['temporary_a'] = np.array(aux) > 0
    df['temporary_b'] = np.array(aux.shift(1)) < 0
    df['cross_directions'] = 'none'
    df.loc[~df['temporary_a'] & ~df['temporary_b'], 'cross_directions'] = 'up'
    df.loc[df['temporary_a'] & df['temporary_b'], 'cross_directions'] = 'down'
    for i,row in df.iterrows():
        if row['cross_directions'] == 'up':
            ax.annotate(
                'BUY', 
                xy = (i, signal[i]), xytext = (50, 50),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                arrowprops = dict(arrowstyle = '<-', connectionstyle = 'arc3,rad=-0.3',color='green'))
        elif row['cross_directions'] == 'down':
            ax.annotate(
                "SELL", 
                xy = (i, signal[i]), xytext = (50, -50),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                arrowprops = dict(arrowstyle = '<-', connectionstyle = 'arc3,rad=-0.3',color='indianred'))

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

def draw_custom_window_boiler_bands(df,column):
    
    st.title("custom window moving average with Bollinger Bands")
    length = st.slider('window size',min_value=3,max_value=100,value=20,step=1)
    mv = calculate_moving_average(length,df[column])
    upper = mv+2*mv.std()
    lower = mv-2*mv.std()
    fig,ax = plt.subplots(figsize=(10,4))
    #mv.plot(legend=True,ax=ax,label="mv")
    upper.plot(legend=True,ax=ax,label="upper")
    lower.plot(legend=True,ax=ax,label="lower")
    df[column].plot(legend=True,ax=ax,label=column)
    df[column].plot(figsize=(10,5),title=f'{length} Day Rolling Bollinger Bands').fill_between(df.index,lower,upper,alpha=0.1)
    st.pyplot(fig)
    

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
    code = re.sub(' +', ' ', code)
    return code

#The US and European stock exchanges normally use stock codes of 3-4 letters that often closely represent the company name, like EZJ for Easyjet.
#Brazilian stock codes look like this: IRBR3.SA
#so the code bellow isn't right
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