import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from datetime import date
import hvplot.pandas
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from bokeh.models.formatters import DatetimeTickFormatter
import plotly.express as px

class CanaryFinancialCalculations:

    def __init__(self) -> None:
        pass

    def portfolio_df(tickers, start, end, timeframe, alpaca):
        df = alpaca.get_bars(
            tickers,
            timeframe,
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
    
    def portfolio_pct_chg(df, weight):
        df = df.pct_change()
        df = df.dropna()
        df = df.dot(weight)
        df = pd.DataFrame(df)
        df.columns = ['Portfolio']
        return df
    
    def benchmark_pct_chg(df):
        df = df.pct_change()
        df = df.dropna()
        df = pd.DataFrame(df)
        return df

    def cumulative_returns(df, investment):
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
        return round(df - df2, 2)
    
    def sharpe_ratio(df):
        sharpe = round((df.mean()*252) / (df.std() * np.sqrt(252)), 2)
        sharpe_df = pd.DataFrame(sharpe)
        sharpe_df.columns = ['Sharpe Ratio']
        return sharpe_df
    
    def return_on_investment(df, tickers, investment):
        return round(((df[tickers].iloc[-1] - investment) / investment)*100, 2)
        
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
        df = pd.DataFrame(df)
        df.columns = ['Average Standard Deviation']
        return df
    
    def rolling_correlation(df):
        calculation = round(df.rolling(window=10).corr(), 2)
        correlation_df = pd.DataFrame(calculation)
        correlation_df = correlation_df.dropna()
        return correlation_df
    
    def correlation(df):
        return round(df.corr(), 2)
    
    def portfolio_distribution_chart(tickers, weights):
        chart = px.pie(values=weights, names=tickers, hole=.5, color_discrete_sequence=['#289c40', '#a5e06c', '#0e5b45', '#1d9371'])
        chart.update_layout({
            'plot_bgcolor': '#00221c',
            'paper_bgcolor': '#00221c'
        })
        chart.update_layout(legend={'font': {'color': 'white'}})
        return chart
    
    def cumulative_return_chart(df, tickers, market, date):
        formatter = DatetimeTickFormatter(months='%b %Y')
        first = df.hvplot.line(x=date, y=tickers, value_label='Value', title='Portfolio Cumulative Returns vs SPY', legend='top', color='#289c40', height=500, width=820, xformatter=formatter, yformatter='%.0f')
        second = df.hvplot.line(x=date, y=market, value_label='Value', legend='top', color='#a5e06c', height=500, width=820, xformatter=formatter, yformatter='%.0f')
        overlay = first * second
        overlay.opts(bgcolor='#00221c')
        return overlay
    
    def roi_chart(df, compare, percent):
        chart = df.hvplot.bar(x=compare, y=percent, color='#289c40', title='Portfolio ROI vs. SPY ROI', ylabel='Percentage')
        chart.opts(bgcolor='#00221c')
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
        chart = df.hvplot.line(x='Date', y='Beta', value_label='Beta', color='#289c40', legend='top', height=500, width=820, xformatter=formatter, yformatter=formatter)
        chart.opts(bgcolor='#00221c')
        return chart


    


