import streamlit as st 
import pandas as pd 
import yfinance as yf
import datetime
import pandas_datareader.data as web
import capm_functions
st.set_page_config(page_title='CAPM Return Calculator', page_icon="chart_with_upwards_trend" , layout='wide')
st.title("Capital Asset Pricing Model (CAPM) Return Calculator")

#  get input from user 

col1,col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Select 4 Stocks", options=['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA','NFLX', 'NVDA'], 
               default=['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])
with col2:
    year = st.number_input("Number of Years", min_value=1, max_value=10)

# get data from yahoo finance SP500

start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
end = datetime.datetime.today()

SP500 = web.DataReader(['sp500'], 'fred', start, end)
print(SP500.head())
stocks_df = pd.DataFrame()
for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df = data
print(stocks_df.head())