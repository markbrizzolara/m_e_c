import yfinance as yf
import streamlit as st
import pandas as pd
import os
import datetime
from bokeh.plotting import figure
import altair as alt
from datetime import date
os.environ['FRED_API_KEY'] = '42742c960ab256ab43886794b6405d87'
from fredapi import Fred
fred = Fred()

def app():
    st.title('Economic Conditions')

    start = datetime.datetime.now()-datetime.timedelta(days=5*365)
    end = date.today()

    st.write("""## U.S. Treasury Yield Curve""")
    series = ['DGS1MO','DGS3MO','DGS6MO', 'DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20', 'DGS30']
    maturityDates = [1/12,1/4,1/2,1,2,3,5,7,10,20,30]# in years
    maturityDatesT = ['1m','3m','6m','1y','2y','3y','5y','7y','10y','20y','30y']
    ratesToday = []; ratesLW = []; ratesLM=[]; ratesLY=[]; rates2Y=[]

    for x in series:
        dataR = fred.get_series(x, observation_start=start, observation_end=end)
        ratesToday.append(dataR[len(dataR) - 1]/100)
        ratesLW.append(dataR[len(dataR)-6]/100)
        ratesLM.append(dataR[len(dataR)-21]/100)
        ratesLY.append(dataR[len(dataR)-252]/100)
        rates2Y.append(dataR[len(dataR)-252*2]/100)

    matDF = pd.DataFrame({'Maturity Date': maturityDatesT,'Yield (Today)': ratesToday,'Yield (Week Ago)': ratesLW,'Yield (Month Ago)': ratesLM,'Yield (Last Year)':ratesLY,'Yield (2 Years Ago)':rates2Y})

    data1 = matDF.set_index('Maturity Date')
    data = data1.reset_index().melt('Maturity Date')
    data = data.rename(columns={"variable": "Date", "value": "Yield"})
    c3 = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X('Maturity Date', sort=['1m','3m','6m','1y','2y','3y','5y','7y','10y','20y','30y']),
        y=alt.Y('Yield', axis=alt.Axis(format='%')),
        color=alt.Color('Date',scale=alt.Scale(domain=['Yield (Today)','Yield (Week Ago)','Yield (Month Ago)','Yield (Last Year)','Yield (2 Years Ago)'],range=['blue','#4f4f4f','#a2a2a2','#d2d2d2','#e8e8e8'])),
        tooltip = [alt.Tooltip('Date'),alt.Tooltip('Maturity Date'),alt.Tooltip('Yield',format='.2%')]
    ).interactive()
    st.altair_chart(c3,use_container_width=True)

    #insert table with % change






    st.write("""## Unemployment Rate""")
    ueDF={}
    ueDF['Unemployment Rate'] = fred.get_series('UNRATE',observation_start=start,observation_end=end)
    st.line_chart(ueDF)

    st.write("""## 10-Year Breakeven Inflation Rate""")
    infDF={}
    infDF['10-Year Breakeven Inflation Rate'] = fred.get_series('T10YIE',observation_start=start,observation_end=end)
    st.line_chart(infDF)

    st.write("""## Personal Savings Rate""")
    infDF={}
    infDF['Personal Savings Rate'] = fred.get_series('PSAVERT',observation_start=start,observation_end=end)
    st.line_chart(infDF)

    st.write("""## Delinquency Rate on Consumer Loans""")
    infDF={}
    infDF['Delinquency Rate on Consumer Loans'] = fred.get_series('DRCLACBS',observation_start=start,observation_end=end)
    st.line_chart(infDF)




