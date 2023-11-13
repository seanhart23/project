import os
import pandas as pd
import alpaca_trade_api as tradeapi
import numpy as np
from datetime import date,timedelta, datetime
    
class Alpaca:
    def __init__(self) -> None:

         # Set Alpaca API key and secret
        ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
        ALPACA_API_KEY = 'PKY1WQKOQS3LU0FD379C'
        ALPACA_SECRET_KEY = 'cA7lkkOK9rNV6yThD48TdqJhMVgbDY80fiYWR5Mr'

        # Create the Alpaca API object
        self.api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=ALPACA_BASE_URL, api_version='v2')

    def get_closing_data(self, days_from_today, tickers):
        # Format current date as ISO format
        
        # TODO: WILL HAVE DYNAMIC VALUES IN FUTURE
        days_ago = pd.Timestamp(date.today() - timedelta(days = days_from_today), tz="America/New_York").isoformat()
        today = pd.Timestamp(date.today().isoformat(), tz="America/New_York").isoformat()
        
        # Set timeframe to "1Day" for Alpaca API
        timeframe = "1Day"

          # Get current closing prices for stocks in portfolio
        df_portfolio = self.api.get_bars(
            tickers, 
            timeframe, 
            adjustment='all',
            start = days_ago,
            end = today
        ).df
        df_portfolio.reset_index(inplace=True)
        res = df_portfolio.pivot(index='timestamp', columns='symbol', values='close')
        res.index = pd.to_datetime(res.index.strftime('%Y-%m-%d'))
        res.reset_index(inplace=True)
        res['timestamp'] = res['timestamp'].dt.floor('D')
        res.set_index('timestamp', inplace=True)
        return res

    def get_cumulative_returns(self, ticker_df, investment, weights=None):
        daily_returns = ticker_df.pct_change()
        daily_returns.dropna(inplace=True)
        if weights: 
            daily_returns = daily_returns.dot(weights)
        cumulative_returns = (1 + daily_returns).cumprod()
        cumulative_returns = cumulative_returns * investment
        return cumulative_returns
    
    def get_cumulative_returns_since(self, days_from_today, stocks_portfolio, investment):
        custom_portfolio_closing = self.get_closing_data(days_from_today=days_from_today, tickers=stocks_portfolio)
        weights = (1/len(stocks_portfolio) * np.ones(len(stocks_portfolio))).tolist()
        custom_cumulative_returns = self.get_cumulative_returns(custom_portfolio_closing, investment, weights)  
        custom_cumulative_returns.columns = ['Your Portfolio']     

        benchmark_portfolios = ['IGM', 'PSI', 'QQQ', 'SPY']
        # get closing data of the benchmarks
        benchmark_df = self.get_closing_data(days_from_today, benchmark_portfolios)
        benchmark_cumulative_returns = benchmark_df.apply(lambda column:  self.get_cumulative_returns(column, investment))   
    
        # join the custom portfolios and benchmark portfolios
        all_portfolios_df = pd.concat([custom_cumulative_returns, benchmark_cumulative_returns], join='inner', axis=1)
        all_portfolios_df.columns = ['Your Portfolio'] + benchmark_portfolios

        return all_portfolios_df
    
    def get_daily_returns(self, closing_df, weights=None):
        daily_returns = closing_df.pct_change()
        if weights:
            daily_returns = daily_returns.dot(weights)
        daily_returns.dropna(inplace=True)

        return daily_returns
    


    
 
        




