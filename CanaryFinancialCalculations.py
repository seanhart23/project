import numpy as np
import pandas as pd

class CanaryFinancialCalculations:

    def __init__(self) -> None:
        pass

    def cumulative_returns(df):
        return (1 + df).cumprod()
    
    def covariance(df, ticker, market):
        return df[ticker].cov(df[market])
    
    def variance(df, market):
        return df[market].var()
    
    def daily_drawdown(df):
        roll_max = df.cummax()
        roll_min = df.cummin()
        daily_drawdown = round(((roll_max - roll_min) / roll_max)*100, 2)
        return daily_drawdown
    
    def tracking_error(df, tickers, market):
        track_error = np.sqrt(sum([i**2 for i in df[tickers] - df[market]]))
        return track_error
    
    def beta(covariance, variance):
        return covariance / variance
    
    def sharpe_ratio(df):
        sharpe = (df.mean()*252) / (df.std() * np.sqrt(252))
        return sharpe
    
    def return_on_investment(investment, returns):
        cumulative_profit = investment * returns
        return_oi = (cumulative_profit - investment) / investment
        return(return_oi)
    
    def standard_deviation(df):
        return df.std()


