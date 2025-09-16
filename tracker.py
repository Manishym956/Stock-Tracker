import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from typing import Optional, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class StockTracker:
    def __init__(self,ticker:str,period:str='1yr'):
        self.ticker=ticker
        self.period=period
        self.data=None
        self.ticker_obj=None
    
    def fetch_data(self,start_date: Optional[str]=None,end_date: Optional[str]=None )->pd.DataFrame:
        try:
            self.ticker_obj= yf.Ticker(self.ticker)
            if start_date and end_date:
                self.data=self.ticker_obj.history(start=start_date,end=end_date)
            else:
                self.data=self.ticker_obj.history(period=self.period)
            if self.data.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")
            
            self.data["SMA_20"]=self.data['close'].rolling(window=20).mean()
            self.data["SMA_50"]=self.data['close'].rolling(window=50).mean()
            self.data["Daily Return"]=self.data['close'].pct_change()
            return self.data
        except Exception as e:
            print(f"Error fetching data for ticker {self.ticker}:{str(e)}")
            return pd.DataFrame()
    def get_company_info(self)->dict:
        if not self.ticker_obj:
            self.ticker_obj= yf.Ticker(self.ticker)
        try:
            info=self.ticker_obj.info
            return {
                "Name":info.get("longName","N/A"),
                "Sector":info.get("sector","N/A"),
                "Industry":info.get("industry","N/A"),
                "Market Cap":info.get("marketCap","N/A"),
                "PE Ratio":info.get("trailingPE","N/A"),
                "Dividend Yield":info.get("dividendYield","N/A")
            }
        except Exception as e:
            print(f"Error fetching company info for ticker {self.ticker}:{str(e)}")
            return {}
    def plot_price_trend(self,save_path:Optional[str]=None, figsize:Tuple[int,int]=(12,8))->None:
        if self.data is None or self.data.empty:
            print("No data to plot. Please fetch data first.")
            return
        plt.style.use('seaborn-v0_8')
        fig,(ax1,ax2)=plt.subplots(2,1,figsize=figsize,gridspec_kw={'height_ratois':[3,1]})


