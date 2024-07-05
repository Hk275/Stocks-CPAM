import plotly.express as px
import numpy as np

# Function to plot the interactive CAPM model

def interactive_plot(df):
    fig = px.line(title='CAPM Model')
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    
    fig.update_layout(width=450, margin = dict(l=20,r=20,t=20,b=20), legend=dict(orientation='h',
                      yanchor = 'bottom', y = 1.02, xanchor='right', x=1,))
    return fig


# Normalized plot based on the initial price of the stock

def normalize_plot(df_2): 
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df 


# Function to calculate daily return 

def daily_return(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df[i][j] = ((df[i][j] - df[i][j-1])/df[i][j-1])*100
        df[i][0] = 0
    return df

# function to calculate beta 
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean()*252

    b,a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b,a 