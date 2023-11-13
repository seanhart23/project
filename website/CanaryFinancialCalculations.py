import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from bokeh.models.formatters import DatetimeTickFormatter
import plotly.express as px
import os

class CanaryFinancialCalculations:

    def __init__(self, user_input_tickers, start_date, end_date, initial_investment) -> None:

         # Set Alpaca API key and secret
        ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
        ALPACA_API_KEY = 'PKY1WQKOQS3LU0FD379C'
        ALPACA_SECRET_KEY = 'cA7lkkOK9rNV6yThD48TdqJhMVgbDY80fiYWR5Mr'

        # Create the Alpaca API object
        self.api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=ALPACA_BASE_URL, api_version='v2')
        # Constant representing the frequency of data from alpaca 
        self.TIMEFRAME = '1D'

        # when the canary object is initialized, initialize the attributes of the user's portfolio
        self.initial_investment = initial_investment
        self.stocks_portfolio = user_input_tickers
        self.weights = [(1 / len(self.stocks_portfolio))] * len(self.stocks_portfolio)
        self.user_portfolio_df = self.portfolio_df(user_input_tickers, start_date, end_date, self.TIMEFRAME)
        self.user_portfolio_pct_chg = self.portfolio_pct_chg(self.user_portfolio_df, self.weights)
        self.user_cumulative_returns = self.cumulative_returns(self.user_portfolio_pct_chg, initial_investment)

        # initialize benchmark portfolio attributes
        benchmark= ["SPY", "QQQ", "PSI", "IGM"]
        self.benchmark_df = self.portfolio_df(benchmark, start_date, end_date, self.TIMEFRAME)
        self.benchmark_chg = self.benchmark_pct_chg(self.benchmark_df)

        self.comparing_portfolios_pct_chg = self.pct_change_comparison(self.user_portfolio_pct_chg, self.benchmark_chg)

    def portfolio_df(self, tickers, start, end, timeframe):
        df = self.api.get_bars(
            tickers,
            timeframe,
            adjustment='all',
            start=start,
            end=end
        ).df
        df = df.pivot(columns='symbol', values='close')
        df.index = df.index.date
        df.index.name='Date'
        return df
    
    def weighted_df(df, weight):
        df = df.dot(weight)
        df = pd.DataFrame(df)
        df.columns = ['Portfolio']
        df.index.name='Date'
        return df
    
    def portfolio_pct_chg(self, df, weight):
        df = df.pct_change()
        df = df.dropna()
        df = df.dot(weight)
        df = pd.DataFrame(df)
        df.columns = ['Portfolio']
        return df
    
    def benchmark_pct_chg(self, df):
        df = df.pct_change()
        df = df.dropna()
        df = pd.DataFrame(df)
        return df

    def cumulative_returns(self, df, investment):
        calculation = (1 + df).cumprod()
        profit = round(investment * calculation, 2)
        profit_df = pd.DataFrame(profit)
        profit_df.columns = ['Profit']
        return profit_df
    
    def cumulative_returns_benchmark(df, investment, ticker):
        calculation = (1 + df[ticker]).cumprod()
        profit = round(investment * calculation, 2)
        profit_df = pd.DataFrame(profit)
        profit_df.columns = [ticker]
        return profit_df
    
    def comparing_cumulative_returns(df, df2):
        compared = pd.concat([df, df2], axis=1, join='inner')
        compared.columns = ['Portfolio', 'SPY']
        compared = compared.round()
        compared = compared.reset_index()
        return compared
    
    def pct_change_comparison(self, df, df2):
        compare = pd.concat([df, df2], axis=1, join='inner')
        return compare
    
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
    
    def avg_beta(df):
        return round(df.mean(),2)
    
    def daily_drawdown(df):
        roll_max = df.cummax()
        roll_min = df.cummin()
        daily_drawdown = round(((roll_max - roll_min) / roll_max)*100, 2)
        return daily_drawdown
    
    def tracking_error(df, df2):
        return round(df - df2, 2)
    
    def sharpe_ratio(df):
        sharpe = round((df.mean()*252) / (df.std() * np.sqrt(252)), 2)
        return sharpe
    
    def return_on_investment(df, tickers, investment):
        return round(((df[tickers].iloc[-1] - investment) / investment)*100, 2)
    
    def roi_comparison(df, df2, df3, df4, df5):
        compared = pd.DataFrame({
            'Compared': ['Portfolio', 'SPY', 'IGM', 'PSI', 'QQQ'],
            'Percentage': [df, df2, df3, df4, df5]
        })
        return compared
        
    def annual_return(df, ticker):
        total_return = (df[ticker].iloc[-1] - df[ticker].iloc[0]) / df[ticker].iloc[0]
        annual_return = round((((1 + total_return)**(1/5))-1)*100, 2)
        return annual_return
    
    def standard_deviation(df):
        rolling_std = round(df.rolling(window = 21).std()*1000, 2)
        rolling_std_df = pd.DataFrame(rolling_std)
        rolling_std_df = rolling_std_df.dropna()
        return rolling_std_df
    
    def standard_deviation_mean(df):
        df = round(df.mean(), 2)
        return df
    
    def rolling_correlation(df):
        calculation = round(df.rolling(window=10).corr(), 2)
        correlation_df = pd.DataFrame(calculation)
        correlation_df = correlation_df.dropna()
        return correlation_df
    
    def correlation(df):
        return round(df.corr(), 2)
    
    def portfolio_distribution_chart(tickers, weights):
        chart = px.pie(values=weights, title='Portfolio Distribution', names=tickers, hole=.5, 
                       color_discrete_sequence=['#289c40', '#a5e06c', '#0e5b45', '#1d9371'])
        chart.update_layout({
            'plot_bgcolor': '#00221c',
            'paper_bgcolor': '#00221c'
        })
        chart.update_layout(legend={'font': {'color': 'white'}})
        chart.update_layout(title={'font': {'color': 'white'}})
        chart.update_layout(title_x=0.487)
        chart.update_layout(width=500)
        return chart
    
    def cumulative_return_chart(df, tickers, market, date):
        formatter = DatetimeTickFormatter(months='%b %Y')
        first = df.hvplot.line(x=date, y=tickers, title='Portfolio Cumulative Returns vs SPY', 
                               color='#289c40', height=500, width=820, xformatter=formatter, yformatter='%.0f')
        second = df.hvplot.line(x=date, y=market, color='#a5e06c', height=500, 
                                width=820, xformatter=formatter, yformatter='%.0f')
        overlay = first * second
        overlay.opts(ylabel='Value')
        overlay.opts(bgcolor='#00221c')
        overlay.opts(hooks=[lambda p, _: p.state.update(border_fill_color='#1d9371')])
        return overlay
    
    def roi_chart(df, compare, percent):
        chart = df.hvplot.bar(x=compare, y=percent, color='#289c40', title='Portfolio ROI vs. SPY ROI', ylabel='Percentage')
        chart.opts(bgcolor='#00221c')
        chart.opts(hooks=[lambda p, _: p.state.update(border_fill_color='#1d9371')])
        return chart
    
    def correlation_scatter_chart(df):
        sns.pairplot(df, hue='Portfolio', palette='Greens')
        plt.suptitle("Portfolio's Correlation To Benchmarks", y=1.02)
        return plt.show()
    
    def correlation_heatmap(df):
        plt.figure(figsize=(8,6))
        sns.heatmap(df, annot=True, cmap='Greens', fmt='.2f', linewidths=.5)
        plt.title('Portfolio Correlation Plot')
        return plt.show()
    
    def beta_chart(df):
        formatter = DatetimeTickFormatter(months='%b %Y')
        chart = df.hvplot.line(x='Date', y='Beta', value_label='Beta', color='#289c40', legend='top', height=500, width=820, xformatter=formatter, )
        chart.opts(bgcolor='#00221c')
        chart.opts(hooks=[lambda p, _: p.state.update(border_fill_color='#1d9371')])
        return chart


    


