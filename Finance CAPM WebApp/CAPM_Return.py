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
try:
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    end = datetime.datetime.today()

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    print(SP500.head())
    stocks_df = pd.DataFrame()
    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']
    # stocks_df['Date'] = stocks_df['Date'].apply(lambda x: x.date())
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown('### Price of Stocks')
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        # capm_functions.normalize_plot(stocks_df)
        st.markdown('### Normalized Price of Stocks')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize_plot(stocks_df)))

    stocks_daily_return = capm_functions.daily_return(stocks_df)
    print(stocks_daily_return.head())

    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b,a = capm_functions.calculate_beta(stocks_daily_return, i)

            beta[i] = b
            alpha[i] = a
    print(beta,alpha)

    beta_df= pd.DataFrame(columns=['Stocks', 'Beta Value'])
    beta_df['Stocks'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown('### Calculate Beta Value of Stocks')
        st.dataframe(beta_df, use_container_width=True)

    rf = 0
    rm = stocks_daily_return['sp500'].mean()*252

    return_df = pd.DataFrame()
    return_value = []

    for stock, value in beta.items():
        return_value.append(str(round(rf + (value*(rf-rm)),2))) 
    return_df['Stocks'] = stocks_list
    print("-------------------")
    print(return_value)
    print(stocks_list)
    return_df['Return Value'] = return_value
    

    with col2:
        st.markdown('### Calculate Return using CAPM')
        st.dataframe(return_df, use_container_width=True)
except:
    st.write("Please Select Valid Input")
