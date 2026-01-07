import logging
from datetime import datetime

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

logging.basicConfig(level=logging.INFO)

# Create database engine and declarative base for ORM mapping
engine = create_engine('sqlite:///financial_data.db', echo=False)
Base = declarative_base()

amazon = yf.Ticker("AMZN")
apple = yf.Ticker("AAPL")
tesla = yf.Ticker("TSLA")

# Simple API connectivity test ===
# live_price = amazon.info['regularMarketPrice']
# print("Amazon Current Market Price:", live_price)

firstdate = datetime(2025, 12, 15)
lastdate = datetime(2025, 12, 31)

# amazondata = amazon.history(start=firstdate, end=lastdate)
# print(amazondata)

# appledata = apple.history(start=firstdate, end=lastdate)
# print(appledata)

# tesladata = tesla.history(start=firstdate, end=lastdate)
# print(tesladata)


def get_stock_data(stock, start_date, end_date):
  return stock.history(start=start_date, end=end_date)


dfam = get_stock_data(amazon, firstdate, lastdate)

dfap = get_stock_data(apple, firstdate, lastdate)

dfts = get_stock_data(tesla, firstdate, lastdate)

dfamcheck = dfam.isnull().sum().sum()

if dfamcheck > 0:
  logging.warning(f"There are {dfamcheck} empty cells in the dataframe")

dfapcheck = dfap.isnull().sum().sum()

if dfapcheck > 0:
  logging.warning(f"There are {dfapcheck} empty cells in the dataframe")

dftscheck = dfts.isnull().sum().sum()

if dftscheck > 0:
  logging.warning(f"There are {dftscheck} empty cells in the dataframe")


class StockPrice(Base):
  __tablename__ = "stock_prices"
  id = Column(Integer, primary_key=True)
  symbol = Column(String, nullable=False)
  date = Column(DateTime, nullable=False)
  open = Column(Float, nullable=False)
  high = Column(Float, nullable=False)
  low = Column(Float, nullable=False)
  close = Column(Float, nullable=False)
  volume = Column(Integer, nullable=False)
  dividends = Column(Float, nullable=False)
  stock_splits = Column(Float, nullable=False)


# Create database tables if they do not already exist
Base.metadata.create_all(engine)

# Initialize database session
Session = sessionmaker(bind=engine)
session = Session()

dataframes = [
    ("AMZN", dfam),
    ("AAPL", dfap),
    ("TSLA", dfts),
]

objects = [
    StockPrice(
        symbol=symbol,
        date=row.name,
        open=row["Open"],
        high=row["High"],
        low=row["Low"],
        close=row["Close"],
        volume=row["Volume"],
        dividends=row["Dividends"],
        stock_splits=row["Stock Splits"],
    ) for symbol, df in dataframes for _, row in df.iterrows()
]

# Stage all ORM objects for database insertion
session.add_all(objects)

try:
  session.commit()
  logging.info("Stock data successfully written to the database.")
  logging.info(f"Total rows inserted: {len(objects)}")
except Exception as e:
  logging.error(f"Database commit failed while inserting stock data: {e}")

  session.rollback()
finally:
  session.close()

amazon_summary = {
    "Last Close": dfam["Close"].iloc[-1],
    "Daily Change": dfam["Close"].iloc[-1] - dfam["Close"].iloc[-2],
    "Mean Close": dfam["Close"].mean(),
    "High/Low": (dfam["High"].max(), dfam["Low"].min()),
    "Total Volume": dfam["Volume"].sum(),
    "Volatility": dfam["Close"].std()
}

logging.info(f"Amazon Summary: {amazon_summary}")

apple_summary = {
    "Last Close": dfap["Close"].iloc[-1],
    "Daily Change": dfap["Close"].iloc[-1] - dfap["Close"].iloc[-2],
    "Mean Close": dfap["Close"].mean(),
    "High/Low": (dfap["High"].max(), dfap["Low"].min()),
    "Total Volume": dfap["Volume"].sum(),
    "Volatility": dfap["Close"].std()
}

logging.info(f"Apple Summary: {apple_summary}")

tesla_summary = {
    "Last Close": dfts["Close"].iloc[-1],
    "Daily Change": dfts["Close"].iloc[-1] - dfts["Close"].iloc[-2],
    "Mean Close": dfts["Close"].mean(),
    "High/Low": (dfts["High"].max(), dfts["Low"].min()),
    "Total Volume": dfts["Volume"].sum(),
    "Volatility": dfts["Close"].std()
}

logging.info(f"Tesla Summary: {tesla_summary}")








