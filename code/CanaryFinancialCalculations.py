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
        profit_df.columns = ['profit']
        return profit_df
    
    def covariance(df, tickers, market):
        covariance_rolling = df[tickers].rolling(window=21).cov(df[market])
        return covariance_rolling
    
    def variance(df, market):
        rolling_variance = df[market].rolling(window=21).var()
        return rolling_variance
    
    def daily_drawdown(df):
        roll_max = df.cummax()
        roll_min = df.cummin()
        daily_drawdown = round(((roll_max - roll_min) / roll_max)*100, 2)
        return daily_drawdown
    
    def tracking_error(df, tickers, market):
        trackingerror_i = (df[tickers] - df[market]).rolling(window=21).std()
        trackingerror_df = trackingerror_i.to_frame()
        trackingerror_df = trackingerror_df.dropna()
        trackingerror_df.columns = ['tracking error']
        return trackingerror_df
    
    def beta(covariance, variance):
        user_beta = covariance / variance
        user_beta_df = pd.DataFrame(user_beta)
        user_beta_df.columns = ['beta']
        user_beta_df = user_beta_df.dropna()
        return user_beta_df
    
    def sharpe_ratio(df):
        sharpe = (df.mean()*252) / (df.std() * np.sqrt(252))
        return sharpe
    
    def return_on_investment(investment, returns):
        cumulative_profit = investment * returns
        return_oi = (cumulative_profit - investment) / investment
        return(return_oi)
    
    def annual_return(df):
        return (1+df)**.2-1
    
    def standard_deviation(df):
        rolling_std = df.rolling(window = 21).std()
        rolling_std_df = pd.DataFrame(rolling_std)
        rolling_std_df = rolling_std_df.dropna()
        return rolling_std_df
    

    


