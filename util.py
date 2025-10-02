import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Union
import re
import os
import json
import warnings
warnings.filterwarnings('ignore')

def validate_ticker(ticker:str):
    if not ticker or not isinstance(ticker,str):
        return False
    pattern=r'^[A-Z]{1,5}[0-9]*$'
    return bool(re.match(pattern,ticker.upper()))
def get_popular_ticker()->List[str]:
    return [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B',
        'UNH', 'JNJ', 'V', 'PG', 'JPM', 'MA', 'HD', 'CVX', 'PFE', 'ABBV',
        'BAC', 'KO', 'AVGO', 'PEP', 'TMO', 'COST', 'WMT', 'DHR', 'ABT',
        'VZ', 'ADBE', 'CRM', 'ACN', 'NFLX', 'TXN', 'NKE', 'QCOM', 'CMCSA',
        'AMD', 'INTC', 'HON', 'AMGN', 'PM', 'UNP', 'IBM', 'SPGI', 'LOW'  
    ]
def get_sector_performance()->dict[str,str]:
    return {
        "Technology":["AAPL","MSFT","GOOGL","AMZN","META","NVDA","ADBE","CRM","NFLX","TXN","QCOM","CMCSA","AMD","INTC","INTC","AVGO"],
        "Healthcare":["UNH,""JNJ","PFE","ABBV","TMO","ABT","AMGN","DHR"],
        "Finance":["BRK-B","JPM","V","MA","BAC","SPGI"],
        "Consumer Cyclical":["PG","KO","PEP","COST","WMT"],
        "Industrials":["HON","UNP"],
        "Energy":["CVX"],
        "Professional Services":["ACN"],
        "Information Technology":["IBM"]
    }
def validate_date_range(start_date:str,end_date:str)->Tuple[bool,str]:
    try:
        start=pd.to_datetime(start_date)
        end=pd.to_datetime(end_date)
        if start>=end:
            return False,"Start date must be before end date."
        if start>datetime.now():
            return False,"Start date cannot be in the future."
        if end>datetime.now():
            return False,"End date cannot be in the future."
        if(end-start).days>3650:
            return False,"Date range cannot exceed 10 years."
        return True,""
    except Exception as e:
        return False,"Invalid date format. Use YYYY-MM-DD."
def get_period_options()->Dict[str,str]:
    return {
        '1d':'1 Day',
        '5d': '5 Days',
        '1mo': '1 Month',
        '3mo': '3 Months',
        '6mo': '6 Months',
        '1y': '1 Year',
        '2y': '2 Years',
        '5y': '5 Years',
        '10y': '10 Years',
        'ytd': 'Year to Date',
        'max': 'Maximum Available'
    }
def format_currency(value:Union[float,int],currency:str='USD')->str:
    if pd.isna(value) or value is None:
        return "N/A"
    if currency == 'USD':
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"
def format_percentage(value:float,decimals:int=2)->str:
    if pd.isna(value) or value is None:
        return "N/A"
    return f"{value*100:.{decimals}f}%"
def format_large_number(calue: Union[float,int])->str:
    if pd.isna(value) or value is None:
        return "N/A"
    if abs(value)>=1e12:
        return f"{value/1e12:.2f}T"
    elif abs(value)>=1e9:
        return f"{value/1e9:.2f}B"
    elif abs(value)>=1e6:
        return f"{value/1e6:.2f}M"
    elif abs(value)>=1e3:
        return f"{value/1e3:.2f}K"
    else:
        return f"{value:.2f}"