import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import pandas as pd
from datetime import date

alpaca_api_key = 'PK306FA7SFOSMY9LBUZ4'
alpaca_secret_key = 'oNujbWMi3ZLrZuVggRN1DnZBLs38EJO00cwyOgsE'
base_url = 'https://paper-api.alpaca.markets'

alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    base_url,
    api_version="v2")

tickers = ["AAPL", "TSLA", "GOOGL", "AMD", "AMC"]
timeframe = '1Day'
initial_investment = 10000

start_date = pd.Timestamp("2018-10-23", tz="America/New_York").isoformat()
end_date = pd.Timestamp("2023-10-23", tz="America/New_York").isoformat()

portfolio_df = alpaca.get_bars(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
).df

res = portfolio_df.pivot(columns='symbol', values='close')
res.index = pd.to_datetime(res.index.strftime('%Y-%m-%d'))