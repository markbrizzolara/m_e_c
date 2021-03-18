import streamlit as st
import yfinance as yf
import pandas as pd
import os
from finvizfinance.quote import finvizfinance
import datetime
from datetime import date
os.environ['FRED_API_KEY'] = '42742c960ab256ab43886794b6405d87'
from fredapi import Fred
fred = Fred()

def app():
    st.title('Market Conditions: Industry View')
    st.write("### Select Industries to View:")

    metrics = ['Market Cap', 'Sales', 'Sales past 5Y', 'Gross Margin','Oper. Margin', 'Profit Margin',
                'Debt/Eq', 'Dividend %']
    metrics2 = ['P/E', 'P/S','Insider Trans','Short Float', 'RSI (14)']

    col1,col2,col3=st.beta_columns(3)
    with col1:
        AD = st.checkbox('Aerospace & Defense')
        CD = st.checkbox('Consumer Discretionary')
        AA = st.checkbox('Airlines')
    with col2:
        F = st.checkbox('Financial Institutions')
        A = st.checkbox('Automotive')
        CA = st.checkbox('Cannabis')
    with col3:
        T = st.checkbox('Technology')
        CS = st.checkbox('Consumer Staples')

    if AD:
        st.write("""## Aerospace & Defense""")
        tickersAD = ["NOC", "BA", "LMT", "RTX", "AVAV", "LHX","XAR"]
        tickerTitlesAD = ["Northrop Grumman", "Boeing", "Lockheed Martin", "Raytheon", "Aerovironment", "L3 Harris","A&D ETF"]
        pull(tickersAD,tickerTitlesAD)
        comp(tickersAD,metrics)
        comp(tickersAD, metrics2)
    if F:
        st.write("""## Financial Institutions""")
        tickersF = ["JPM", "BAC", "WFC", "C", "USB", "GS","SCHW","XLF"]
        tickerTitlesF = ["JP Morgan", "Bank of America", "Wells Fargo", "Citigroup", "US Bancorp", "Goldman Sachs","Charles Schwab","Financial Sector ETF"]
        pull(tickersF, tickerTitlesF)
        comp(tickersF, metrics)
        comp(tickersF, metrics2)
    if T:
        st.write("""## Technology""")
        tickersT = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "NFLX","SQ","SHOP","MELI","SNAP","TWTR","UBER","LYFT","XLK"]
        tickerTitlesT = ["Apple", "Microsoft", "Google", "Amazon", "Facebook", "Netflix","Square","Shopify","Mercadolibre","Snapchat","Twitter","Uber","Lyft","Technology ETF"]
        pull(tickersT, tickerTitlesT)
        comp(tickersT, metrics)
        comp(tickersT, metrics2)
    if CD:
        st.write("""## Consumer Discretionary""")
        tickersCD = ["HD", "MCD", "LOW", "TGT", "CMG","SBUX","NKE","XLY"]
        tickerTitlesCD = ["Home Depot","McDonalds", "Lowe's", "Target", "Chipotle","Starbucks","Nike","CD ETF"]
        pull(tickersCD, tickerTitlesCD)
        comp(tickersCD, metrics)
        comp(tickersCD, metrics2)
    if A:
        st.write("""## Automotive""")
        tickersA = ["TM", "TSLA", "HMC", "GM","F","CARZ"]
        tickerTitlesA = ["Toyota","Tesla", "Honda", "General Motors","Ford","Automotive ETF"]
        pull(tickersA, tickerTitlesA)
        comp(tickersA, metrics)
        comp(tickersA, metrics2)
    if CS:
        st.write("""## Consumer Staples""")
        tickersCS = ["PG", "KO", "PEP", "WMT", "MO", "COST","XLP"]
        tickerTitlesCS = ["Procter + Gamble", "Coca Cola", "Pepsi", "Walmart", "Altria", "Costco","Consumer Staples ETF"]
        pull(tickersCS, tickerTitlesCS)
        comp(tickersCS, metrics)
        comp(tickersCS, metrics2)
    if AA:
        st.write("""## Airlines""")
        tickersAA = ["LUV", "DAL", "UAL", "AAL", "JBLU", "SAVE","JETS"]
        tickerTitlesAA = ["Southwest", "Delta", "United", "American", "Jetblue", "Spirit","Airline ETF"]
        pull(tickersAA, tickerTitlesAA)
        comp(tickersAA, metrics)
        comp(tickersAA, metrics2)
    if CA:
        st.write("""## Cannabis""")
        tickersCA = ["IIPR", "CGC", "CRON", "ACB", "TLRY", "APHA", "YOLO"]
        tickerTitlesCA = ["IIPR", "Canopy Growth", "Cronos Group", "Aurora Cannabis", "Tilray", "Aphria", "Cannabis ETF"]
        pull(tickersCA, tickerTitlesCA)
        comp(tickersCA, metrics)
        comp(tickersCA, metrics2)

def pull(tickers,tickerTitles):

    price = [];change = [];mini = [];maxi = [];weekChange = [];monthChange = [];yearChange = [];mktcap = [];yld=[]
    plot = {}
    plotDF = pd.DataFrame(plot)

    for x in tickers:
        data = yf.Ticker(x)
        hist_year = data.history(period="252d", interval="1d")
        hist_fine = data.history(period="1d", interval="1m")
        price.append(hist_fine["Close"][len(hist_fine["Close"]) - 1])
        change.append((hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][
            len(hist_year["Close"]) - 2]) /
                        hist_year["Close"][len(hist_year["Close"]) - 1])
        mini.append(min(hist_year['Close']))
        maxi.append(max(hist_year['Close']))
        weekChange.append((hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][
            len(hist_year["Close"]) - 6]) /
                            hist_year["Close"][len(hist_year["Close"]) - 6])
        monthChange.append(
            (hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][
                len(hist_year["Close"]) - 21]) /
            hist_year["Close"][len(hist_year["Close"]) - 21])
        yearChange.append(
            (hist_fine["Close"][len(hist_fine["Close"]) - 1] - hist_year["Close"][
                len(hist_year["Close"]) - 252]) /
            hist_year["Close"][len(hist_year["Close"]) - 252])
        plotDF[tickerTitles[tickers.index(x)]] = hist_year["Close"] / hist_year["Close"][
            len(hist_year["Close"]) - 252] * 100 - 100
        mktcap.append(data.info['marketCap'])


    summary = {'Company': tickerTitles, 'Ticker': tickers, 'Price': price, 'Daily Change': change,
                 '52 Week Low': mini, '52 Week High': maxi, 'Weekly Change': weekChange,
                 'Monthly Change': monthChange, 'Yearly Change': yearChange, 'Market Cap': mktcap}
    sumDF = pd.DataFrame(summary)
    sumDF = sumDF.sort_values(by=['Daily Change'], ascending=False)
    st.table(sumDF.style.format(
        {'Price': "{:.2f}", 'Daily Change': "{:.2%}", '52 Week Low': "{:.2f}", '52 Week High': "{:.2f}",
         'Weekly Change': "{:.2%}", 'Monthly Change': "{:.2%}", 'Yearly Change': "{:.2%}", 'Market Cap': "{:,.0f}"}).bar(
        subset=['Daily Change', 'Weekly Change', 'Monthly Change', 'Yearly Change'], align='mid',
        color=['#d65f5f', '#5fba7d']).apply(highlight_green, axis=None).apply(highlight_red, axis=None))
    st.line_chart(plotDF)
    return

def comp(tickers, metrics):
    df = pd.DataFrame(index=tickers, columns=metrics)
    for x in tickers:
        stock = finvizfinance(x)
        data = stock.TickerFundament()
        summary = pd.DataFrame(data, index=[0])

        for y in metrics:
            df.loc[x,y] = summary.loc[0,y]

    #df[metrics[0]] = pd.to_numeric(df[metrics[0]])
    #df[metrics[1]] = pd.to_numeric(df[metrics[1]])
    df = df.sort_values(by=metrics[0], ascending=False)
    st.table(df)
    return

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