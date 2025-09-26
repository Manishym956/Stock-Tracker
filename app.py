import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
from tracker import StockTracker, compare_stocks
from model import StockPredictor,evaluate_model_performance
from util import (validate_ticker,get_popular_ticker,validate_date_range,get_period_options,format_currency,format_percentage,format_large_number,calculate_technical_indicators,save_analysis_report,get_sector_performance)
st.set_page_config(
    page_title="Stock Price Tracker & Visualizer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

#css needed

#def main():
