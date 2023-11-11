import numpy as np
import pandas as pd
import hvplot.pandas
from datetime import datetime, timedelta
import plotly.express as px
import altair as alt
from vega_datasets import data
import pandas_datareader as web
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.models.formatters import DatetimeTickFormatter

class CanaryFinancialCalculations:

    def __init__(self) -> None:
        pass

    def cumulative_returns(df, investment):
        calculation = (1 + df).cumprod()
        profit = (investment * calculation)
        profit_df = pd.DataFrame(profit)
        profit_df.columns = ['Profit']
        return profit_df
    
    def cumulative_returns_benchmark(df, investment, ticker):
        calculation = (1 + df[ticker]).cumprod()
        profit = (investment * calculation)
        profit_df = pd.DataFrame(profit)
        profit_df.columns = [ticker]
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
        return round(((df[tickers].iloc[-1] - investment) / investment)*100, 2)
        
    
    def annual_return(df, ticker):
        total_return = (df[ticker].iloc[-1] - df[ticker].iloc[0]) / df[ticker].iloc[0]
        annual_return = (((1 + total_return)**(1/5))-1)*100
        return annual_return
    
    def standard_deviation(df):
        rolling_std = df.rolling(window = 21).std()
        rolling_std_df = pd.DataFrame(rolling_std)
        rolling_std_df = rolling_std_df.dropna()
        return rolling_std_df
    
    def rolling_correlation(df):
        calculation = df.rolling(window=10).corr()
        correlation_df = pd.DataFrame(calculation)
        correlation_df = correlation_df.dropna()
        return correlation_df
    
    def correlation(df):
        return df.corr()
    
    def portfolio_distribution_chart(tickers, weights):
        chart = px.pie(values=weights, names=tickers, hole=.5, color_discrete_sequence=['#008000', '#90ee90', '#ffff00', '#cccc00'])
        chart.update_layout({
            'plot_bgcolor': '#003300',
            'paper_bgcolor': '#003300'
        })
        chart.update_layout(legend={'font': {'color': 'white'}})
        return chart
    
    def cumulative_return_chart(df, tickers, market, date):
        formatter = DatetimeTickFormatter(months='%b %Y')
        first = df.hvplot.line(x=date, y=tickers, value_label='Value', title='Portfolio Cumulative Returns vs SPY', legend='top', color='#9acd32', height=500, width=820, xformatter=formatter, yformatter='%.0f')
        second = df.hvplot.line(x=date, y=market, value_label='Value', legend='top', color='yellow', height=500, width=820, xformatter=formatter, yformatter='%.0f')
        overlay = first * second
        overlay.opts(bgcolor='#003300')
        return overlay
    
    def roi_chart(df, compare, percent):
        chart = df.hvplot.bar(x=compare, y=percent, color='#9acd32', title='Portfolio ROI vs. SPY ROI', ylabel='Percentage')
        chart.opts(bgcolor='#003300')
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
        chart = df.hvplot.line(x='Date', y='Beta', value_label='Beta', color='#9acd32', legend='top', height=500, width=820, xformatter=formatter, yformatter=formatter)
        chart.opts(bgcolor='#003300')
        return chart


    


