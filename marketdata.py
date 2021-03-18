import streamlit as st
import yfinance as yf
import pandas as pd
import os
import altair as alt
import datetime
from datetime import date
os.environ['FRED_API_KEY'] = '42742c960ab256ab43886794b6405d87'
from fredapi import Fred
fred = Fred()

def app():
    st.title('Market Conditions')

    ####################################   Overall Market Conditions   ####################################################
    st.write("""## Major Indices""")
    tickers = ["SPY","DIA","ONEQ","IWM","VT"]
    tickerTitles = ["S&P 500","DJ Ind. Avg.","NASDAQ Comp.","Russell 2000","Total World"]
    price=[];change=[];mini=[];maxi=[];weekChange=[];monthChange=[]; yearChange=[]
    plot1 = {}
    plot1DF = pd.DataFrame(plot1)

    for x in tickers:
        data = yf.Ticker(x)
        hist_year = data.history(period="252d",interval="1d")
        hist_fine = data.history(period="1d", interval="1m")
        price.append(hist_fine["Close"][len(hist_fine["Close"])-1])
        change.append((hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][len(hist_year["Close"]) - 2]) /
                      hist_year["Close"][len(hist_year["Close"]) - 1])
        mini.append(min(hist_year['Close']))
        maxi.append(max(hist_year['Close']))
        weekChange.append((hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][len(hist_year["Close"]) - 6]) /
                      hist_year["Close"][len(hist_year["Close"]) - 6])
        monthChange.append(
            (hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][len(hist_year["Close"]) - 21]) /
            hist_year["Close"][len(hist_year["Close"]) - 21])
        yearChange.append(
            (hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][len(hist_year["Close"]) - 252]) /
            hist_year["Close"][len(hist_year["Close"]) - 252])
        plot1DF[tickerTitles[tickers.index(x)]] = hist_year["Close"] / hist_year["Close"][len(hist_year["Close"]) - 252] * 100 - 100

    summary = {'Index': tickerTitles,'Ticker': tickers,'Price': price,'Daily Change':change,'52 Week Low': mini,'52 Week High': maxi,'Weekly Change':weekChange,'Monthly Change':monthChange,'Yearly Change':yearChange}
    sumDF = pd.DataFrame(summary)
    st.table(sumDF.style.format({'Price':"{:.2f}", 'Daily Change':"{:.2%}",'52 Week Low':"{:.2f}",'52 Week High':"{:.2f}",'Weekly Change':"{:.2%}",'Monthly Change':"{:.2%}",'Yearly Change':"{:.2%}"}).bar(subset=['Daily Change','Weekly Change','Monthly Change','Yearly Change'],align='mid',color=['#d65f5f', '#5fba7d']).apply(highlight_green, axis=None).apply(highlight_red, axis=None))
    st.line_chart(plot1DF)

    ####################################   Conditions by Sector   #########################################################
    st.write("""## Major Sectors""")
    tickersS = ["XLE","XLF","XLU","XLI","XLK","XLV","XLY","XLP","XLB","XLRE","XLC"]
    tickerTitlesS = ["Energy","Financials", "Utilities","Industrials","Technology","Health Care","Consumer Discretionary","Consumer Staples","Materials","Real Estate","Communication Services"]
    priceS=[];changeS=[];miniS=[];maxiS=[];weekChangeS=[];monthChangeS=[]; yearChangeS=[]
    plot2 = {}
    plot2DF = pd.DataFrame(plot2)

    for x in tickersS:
        dataS = yf.Ticker(x)
        hist_yearS = dataS.history(period="252d",interval="1d")
        hist_fineS = dataS.history(period="1d", interval="1m")
        priceS.append(hist_fineS["Close"][len(hist_fineS["Close"])-1])
        changeS.append((hist_fineS["Close"][len(hist_fineS["Close"]) - 1] - hist_yearS["Close"][len(hist_yearS["Close"]) - 2]) /
                      hist_yearS["Close"][len(hist_yearS["Close"]) - 1])
        miniS.append(min(hist_yearS['Close']))
        maxiS.append(max(hist_yearS['Close']))
        weekChangeS.append((hist_fineS["Close"][len(hist_fineS["Close"]) - 1] - hist_yearS["Close"][len(hist_yearS["Close"]) - 6]) /
                      hist_yearS["Close"][len(hist_yearS["Close"]) - 6])
        monthChangeS.append(
            (hist_fineS["Close"][len(hist_fineS["Close"]) - 1] - hist_yearS["Close"][len(hist_yearS["Close"]) - 21]) /
            hist_yearS["Close"][len(hist_yearS["Close"]) - 21])
        yearChangeS.append(
            (hist_fineS["Close"][len(hist_fineS["Close"]) - 1] - hist_yearS["Close"][len(hist_yearS["Close"]) - 252]) /
            hist_yearS["Close"][len(hist_yearS["Close"]) - 252])
        plot2DF[tickerTitlesS[tickersS.index(x)]] = hist_yearS["Close"] / hist_yearS["Close"][
            len(hist_yearS["Close"]) - 252] * 100 - 100

    summaryS = {'Sector': tickerTitlesS,'Ticker': tickersS,'Price': priceS,'Daily Change':changeS,'52 Week Low': miniS,'52 Week High': maxiS,'Weekly Change':weekChangeS,'Monthly Change':monthChangeS,'Yearly Change':yearChangeS}
    sumDFS = pd.DataFrame(summaryS)
    sumDFS = sumDFS.sort_values(by=['Daily Change'],ascending=False)
    st.table(sumDFS.style.format({'Price':"{:.2f}", 'Daily Change':"{:.2%}",'52 Week Low':"{:.2f}",'52 Week High':"{:.2f}",'Weekly Change':"{:.2%}",'Monthly Change':"{:.2%}",'Yearly Change':"{:.2%}"}).bar(subset=['Daily Change','Weekly Change','Monthly Change','Yearly Change'],align='mid',color=['#d65f5f', '#5fba7d']).apply(highlight_green, axis=None).apply(highlight_red, axis=None))
    st.line_chart(plot2DF)

def highlight_green(x):
    c1 = 'color: #5fba7d'
    c2 = ''
    mask = x['Price'] > ((x['52 Week High'] - x['52 Week Low']) * 0.95 + x['52 Week Low'])
    df1 = pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[mask,'52 Week High'] = c1
    return df1

def highlight_red(x):
    c1 = 'color: #d65f5f'
    c2 = ''
    mask = x['Price'] < ((x['52 Week High'] - x['52 Week Low']) * 0.1 + x['52 Week Low'])
    df1 = pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[mask,'52 Week Low'] = c1
    return df1