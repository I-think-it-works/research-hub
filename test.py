import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import seaborn as sns
import math as math
import sys
import logging
import time
import datetime
import yfinance as yf
import efinance as ef
import akshare as ak
import itertools
import warnings
import imfp
import re
import streamlit as st

from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MultipleLocator
from pandas import Timedelta
from abc import abstractmethod
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.stats import t
from statsmodels.tsa.seasonal import STL
from sklearn.decomposition import PCA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import grangercausalitytests
from scipy.stats import pearsonr
from datetime import date
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import MaxNLocator

pd.set_option('display.max_rows', None) 

# 1. Set up your page and add some analysis text
st.set_page_config(page_title="Research Hub", layout="wide")

tab1, tab2 = st.tabs(['Econ','ESG'])

with tab1:

    st.title("Global Asset Performance")
    st.markdown("""
    Welcome to my financial analysis site. Below is the cumulative return of various 
    indexes and assets, normalized to Day 1. 

    *You can write your full financial analysis here using Markdown formatting!*
    """)

    # 2. Cache the data loading so it doesn't slow down your website
    @st.cache_data
    def load_data():
        # Ensure 'Prices until 12312025.xlsx' is in the same folder as this script
        return pd.read_excel('Prices until 12312025.xlsx', index_col=0)

    close_price_raw = load_data()
    price_index_to_day1 = close_price_raw / close_price_raw.iloc[0]

    # 3. Create the Matplotlib Figure
    fontP = font_manager.FontProperties()
    fontP.set_family('SimHei')
    fontP.set_size(7)

    color_code = {
        'S&P500': 'blue',
        'CSI300': 'red',
        'N225': 'lightsteelblue',
        'DAX40': 'purple',
        'HSI': 'salmon',
        'Gold9999': 'gold',
        'SH_gov_bond': 'gray',
        '60_40': 'black',
        'My_port': 'lime'
    }

    line_width = 0.7

    # Use fig, ax instead of plt.figure() for web safety
    fig, ax = plt.subplots(figsize=(13, 6)) 

    for c in price_index_to_day1.columns:
        # Use .get() as a safeguard in case a column name isn't in your color_code dict
        ax.plot(price_index_to_day1.index, price_index_to_day1[c], 
                label=c, color=color_code.get(c, 'black'), linewidth=line_width)

    ax.legend(title='Assets', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Set y-axis and x-axis intervals
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))

    ax.set_title("Asset price - indexed to day 1")
    ax.set_ylabel("Index")

    # Rotate x-axis ticks
    plt.setp(ax.get_xticklabels(), rotation=90)
    fig.tight_layout()

    # 4. Render the chart in Streamlit
    st.pyplot(fig)

with tab2:
    st.write("This content is forthcoming")

pd.options.display.float_format = '{:.4f}'.format
