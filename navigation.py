import marketdata
import main
import byIndustry
import streamlit as st

st.set_page_config(layout="wide")

PAGES = {
    "Market Conditions": marketdata,
    "Market Conditions: Industry View": byIndustry,
    "Economic Conditions": main
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()