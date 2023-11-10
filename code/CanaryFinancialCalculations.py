import numpy as np
import pandas as pd
import hvplot.pandas
from datetime import datetime, timedelta
import plotly.express as px
import altair as alt
from vega_datasets import data
import pandas_datareader as web

class CanaryFinancialCalculations:

    def __init__(self) -> None:
        pass

    def cumulative_returns(df, investment):
        calculation = (1 + df).cumprod()
        profit = (investment * calculation)
        profit_df = pd.DataFrame(profit)
        profit_df.columns = ['Profit']
        return profit_df
    
    def covariance(df, tickers, market):
        covariance_rolling = df[tickers].rolling(window=21).cov(df[market])
        return covariance_rolling
    
    def variance(df, market):
        rolling_variance = df[market].rolling(window=21).var()
        return rolling_variance
    
    def beta(covariance, variance):
        user_beta = covariance / variance
        user_beta_df = pd.DataFrame(user_beta)
        user_beta_df.columns = ['Beta']
        user_beta_df = user_beta_df.dropna()
        return user_beta_df
    
    def daily_drawdown(df):
        roll_max = df.cummax()
        roll_min = df.cummin()
        daily_drawdown = round(((roll_max - roll_min) / roll_max)*100, 2)
        return daily_drawdown
    
    def tracking_error(df, df2):
        return (df - df2)
    
    def sharpe_ratio(df):
        sharpe = (df.mean()*252) / (df.std() * np.sqrt(252))
        sharpe_df = pd.DataFrame(sharpe)
        sharpe_df.columns = ['Sharpe Ratio']
        return sharpe_df
    
    def return_on_investment(df, tickers, investment):
        return ((df[tickers].iloc[-1] - investment) / investment)*100
        
    
    def annual_return(df, ticker):
        total_return = (df[ticker].iloc[-1] - df[ticker].iloc[0]) / df[ticker].iloc[0]
        annual_return = (((1 + total_return)**(1/5))-1)*100
        return annual_return
    
    def standard_deviation(df):
        rolling_std = df.rolling(window = 21).std()
        rolling_std_df = pd.DataFrame(rolling_std)
        rolling_std_df = rolling_std_df.dropna()
        return rolling_std_df
    
    def portfolio_distribution_chart(tickers, weights):
        chart = px.pie(values=weights, names=tickers, hole=.5)
        return chart
    

    


