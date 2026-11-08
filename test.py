import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

# 1. Set up your page and add some analysis text
st.set_page_config(page_title="Global Markets Analysis", layout="wide")

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
