from flask import Flask, render_template, request, jsonify
app = Flask(__name__, '/static')
import pandas as pd
import numpy as np
from alpaca import Alpaca
from utilities import data_creation, create_d3_line_data, create_d3_beta_data, create_d3_bar_data
from CanaryFinancialCalculations import CanaryFinancialCalculations
from datetime import date, timedelta

a = Alpaca()
BENCHMARK_PORTFOLIOS = ['IGM', 'PSI', 'QQQ', 'SPY']
ALL_PORTFOLIOS = ['Your Portfolio'] + BENCHMARK_PORTFOLIOS
INITIAL_INVESTMENT = 10000
TIME = 365*5 # all portfolio calculations will start 5 years back from the time the user inputs stock data
TIMEFRAME = '1D' # all stock data from alpaca api will show a single datapoint for 1 day

@app.route('/', methods = ["GET", "POST"])
def hello_world():
   # getting input with stocksname = in HTML form
    if request.method == "POST":
       stocks_input = request.form.get("stockname")
       
       # parsing stocks input
       global stocks_portfolio
       stocks_portfolio = [x.strip() for x in stocks_input.split(',')] 
       
       start_date = pd.Timestamp(date.today() - timedelta(days = TIME), tz="America/New_York").isoformat()
       end_date = pd.Timestamp(date.today().isoformat(), tz="America/New_York").isoformat()

       global canary 
       # initialize the canary with the user's pick of stocks, start and end times of the investment period, and the initial investment amount
       canary = CanaryFinancialCalculations(stocks_portfolio, start_date, end_date, INITIAL_INVESTMENT)

       user_roi = CanaryFinancialCalculations.return_on_investment(canary.user_cumulative_returns, 'Profit', INITIAL_INVESTMENT)
       user_annual_returns = CanaryFinancialCalculations.annual_return(CanaryFinancialCalculations.weighted_df(canary.user_portfolio_df, canary.weights), 'Portfolio')
       user_sharpe_ratio = CanaryFinancialCalculations.sharpe_ratio(canary.user_portfolio_pct_chg)[0]

       # calculate average beta
       user_covariance = CanaryFinancialCalculations.covariance(canary.comparing_portfolios_pct_chg, "Portfolio", "SPY")
       user_variance = CanaryFinancialCalculations.variance(canary.comparing_portfolios_pct_chg, "SPY")
       user_avg_beta =  round(CanaryFinancialCalculations.beta(user_covariance, user_variance).mean(),2)[0]

       # Calculate ave std
       user_std = round(CanaryFinancialCalculations.standard_deviation(canary.user_portfolio_pct_chg).mean(),2)[0]

       # calculate tracking error
       benchmark_annual_returns = CanaryFinancialCalculations.annual_return(canary.benchmark_df, 'SPY')
       tracking_error = round(user_annual_returns-benchmark_annual_returns,2)
       
       return render_template("portfolio.html", roi=user_roi,
                               annual_return = user_annual_returns,
                                 sharpe_ratio = user_sharpe_ratio, 
                                 avg_beta = user_avg_beta, 
                                 std = user_std,
                                 tracking_err = tracking_error
                                 )
    return render_template("form.html")
    
@app.route('/get_piechart_data')
def get_piechart_data():
   piechart_data= []
   # assuming equal weights for all stocks
   weight = 1/len(stocks_portfolio)
   global stocks_distribution
   stocks_distribution = round(weight * 100, 2) * np.ones(len(stocks_portfolio))

   global weights
   weights = (1/len(stocks_portfolio) * np.ones(len(stocks_portfolio))).tolist()

   piechart_data= []
   data_creation(piechart_data, stocks_distribution, stocks_portfolio)
   return jsonify(piechart_data)

@app.route('/get_closing_data')
def get_closing_data():
    res = a.get_closing_data(days_from_today=365*5, tickers=stocks_portfolio)
    res.reset_index(inplace=True)
    return jsonify(create_d3_line_data(stocks_portfolio, res, stocks_portfolio))

@app.route('/get_cumulative_returns_data')
def get_cumulative_returns_data():
    all_portfolios_df = a.get_cumulative_returns_since(days_from_today=365*5, stocks_portfolio=stocks_portfolio, investment=10000)
    all_portfolios_df.columns = ALL_PORTFOLIOS
    all_portfolios_df.reset_index(inplace=True)
    return jsonify(create_d3_line_data(ALL_PORTFOLIOS, all_portfolios_df, stocks_portfolio))

@app.route('/get_rolling_beta_data')
def get_rolling_beta_data():
    custom_portfolio = a.get_closing_data(days_from_today=365*5, tickers=stocks_portfolio)
    custom_daily_returns = a.get_daily_returns(custom_portfolio, weights)

    market_data = a.get_closing_data(365*5, ['SPY'])
    market_data_daily_returns = a.get_daily_returns(market_data)

    daily_returns = pd.concat([custom_daily_returns, market_data_daily_returns], join='inner', axis=1)
    daily_returns.columns = ['Your Portfolio', 'SPY']
    
   # get covariance, variance, beta
    rolling_covariance = daily_returns['Your Portfolio'].rolling(window=21).cov(daily_returns['SPY'])
    rolling_variance = daily_returns['SPY'].rolling(window=21).var()
    rolling_beta = rolling_covariance / rolling_variance

    return jsonify(create_d3_beta_data(rolling_beta))

@app.route('/get_portolio_roi_data')
def get_portfolio_roi_data():
    all_portfolios_df = a.get_cumulative_returns_since(days_from_today=365*5, stocks_portfolio=stocks_portfolio, investment=INITIAL_INVESTMENT)
    roi = all_portfolios_df.apply(lambda column: round((column.iloc[-1]-INITIAL_INVESTMENT)/INITIAL_INVESTMENT * 100,2), axis=0)
   
    return jsonify(create_d3_bar_data(roi))

@app.route('/get_correlation_heatmap_data')
def get_correlation_heatmap_data():
    global weights
    weights = (1/len(stocks_portfolio) * np.ones(len(stocks_portfolio))).tolist()

    custom_portfolio_closing = a.get_closing_data(days_from_today=365*5, tickers=stocks_portfolio)
    custom_daily_returns = a.get_daily_returns(custom_portfolio_closing, weights)
    
    benckmark_closing = a.get_closing_data(days_from_today=365*5, tickers=BENCHMARK_PORTFOLIOS)
    benchmark_daily_returns = benckmark_closing.apply(lambda column: a.get_daily_returns(column))
    
    all_daily_returns = pd.concat([custom_daily_returns, benchmark_daily_returns], axis=1)
    all_daily_returns.columns = ALL_PORTFOLIOS

    # calculate the correlation matrix and reshape
    df_corr = all_daily_returns.corr().stack().reset_index()

    # rename the columns
    df_corr.columns = ['FEATURE_1', 'FEATURE_2', 'CORRELATION']
    data_compiled = []
    for _, row in df_corr.iterrows():
        data = {
            'group': row['FEATURE_1'], 
            'variable': row['FEATURE_2'],
            'value': row['CORRELATION'],
        }
        data_compiled.append(data)
    
    return jsonify(data_compiled)

# ONLY USE BELOW ON LOCAL MACHINE

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)