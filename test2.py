{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "679b6be6",
   "metadata": {},
   "outputs": [],
   "source": [
    "# !pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6a3e98ea",
   "metadata": {},
   "outputs": [],
   "source": [
    "# %%writefile test.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fd5fd8d7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# Package setups\n",
    "# ========================================================================="
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "618b8a58",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from matplotlib import font_manager\n",
    "import matplotlib.mlab as mlab\n",
    "import matplotlib.dates as mdates\n",
    "import seaborn as sns\n",
    "import math as math\n",
    "import sys\n",
    "import logging\n",
    "import time\n",
    "import datetime\n",
    "import yfinance as yf\n",
    "import efinance as ef\n",
    "import akshare as ak\n",
    "import itertools\n",
    "import warnings\n",
    "import imfp\n",
    "import re\n",
    "import streamlit as st\n",
    "\n",
    "from matplotlib.ticker import PercentFormatter\n",
    "from matplotlib.ticker import MultipleLocator\n",
    "from pandas import Timedelta\n",
    "from abc import abstractmethod\n",
    "from scipy.optimize import minimize\n",
    "from scipy.stats import norm\n",
    "from scipy.stats import t\n",
    "from statsmodels.tsa.seasonal import STL\n",
    "from sklearn.decomposition import PCA\n",
    "from statsmodels.tsa.stattools import adfuller\n",
    "from statsmodels.graphics.tsaplots import plot_acf\n",
    "from statsmodels.tsa.stattools import acf\n",
    "from statsmodels.tsa.stattools import grangercausalitytests\n",
    "from scipy.stats import pearsonr\n",
    "from datetime import date\n",
    "from matplotlib.ticker import StrMethodFormatter\n",
    "from matplotlib.ticker import MaxNLocator\n",
    "\n",
    "pd.set_option('display.max_rows', None) \n",
    "\n",
    "pd.options.display.float_format = '{:.4f}'.format"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d384482e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# General layout setup\n",
    "# ========================================================================="
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dda21982",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Set up your page and add some analysis text\n",
    "st.set_page_config(page_title=\"Research Hub\", layout=\"wide\")\n",
    "\n",
    "tab1, tab2 = st.tabs(['Econ','ESG'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a3c9ce70",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# Tab Econ\n",
    "# ========================================================================="
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cb148716",
   "metadata": {},
   "outputs": [],
   "source": [
    "with tab1:\n",
    "\n",
    "    st.title(\"Global Asset Performance\")\n",
    "    st.markdown(\"\"\"\n",
    "    Welcome to my financial analysis site. Below is the cumulative return of various \n",
    "    indexes and assets, normalized to Day 1. \n",
    "\n",
    "    *You can write your full financial analysis here using Markdown formatting!*\n",
    "    \"\"\")\n",
    "\n",
    "    # 2. Cache the data loading so it doesn't slow down your website\n",
    "    @st.cache_data\n",
    "    def load_data():\n",
    "        # Ensure 'Prices until 12312025.xlsx' is in the same folder as this script\n",
    "        return pd.read_excel('Prices until 12312025.xlsx', index_col=0)\n",
    "\n",
    "    close_price_raw = load_data()\n",
    "    price_index_to_day1 = close_price_raw / close_price_raw.iloc[0]\n",
    "\n",
    "    # 3. Create the Matplotlib Figure\n",
    "    fontP = font_manager.FontProperties()\n",
    "    fontP.set_family('SimHei')\n",
    "    fontP.set_size(7)\n",
    "\n",
    "    color_code = {\n",
    "        'S&P500': 'blue',\n",
    "        'CSI300': 'red',\n",
    "        'N225': 'lightsteelblue',\n",
    "        'DAX40': 'purple',\n",
    "        'HSI': 'salmon',\n",
    "        'Gold9999': 'gold',\n",
    "        'SH_gov_bond': 'gray',\n",
    "        '60_40': 'black',\n",
    "        'My_port': 'lime'\n",
    "    }\n",
    "\n",
    "    line_width = 0.7\n",
    "\n",
    "    # Use fig, ax instead of plt.figure() for web safety\n",
    "    fig, ax = plt.subplots(figsize=(13, 6)) \n",
    "\n",
    "    for c in price_index_to_day1.columns:\n",
    "        # Use .get() as a safeguard in case a column name isn't in your color_code dict\n",
    "        ax.plot(price_index_to_day1.index, price_index_to_day1[c], \n",
    "                label=c, color=color_code.get(c, 'black'), linewidth=line_width)\n",
    "\n",
    "    ax.legend(title='Assets', bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "\n",
    "    # Set y-axis and x-axis intervals\n",
    "    ax.yaxis.set_major_locator(MultipleLocator(1))\n",
    "    ax.xaxis.set_major_locator(mdates.YearLocator(2))\n",
    "\n",
    "    ax.set_title(\"Asset price - indexed to day 1\")\n",
    "    ax.set_ylabel(\"Index\")\n",
    "\n",
    "    # Rotate x-axis ticks\n",
    "    plt.setp(ax.get_xticklabels(), rotation=90)\n",
    "    fig.tight_layout()\n",
    "\n",
    "    # 4. Render the chart in Streamlit\n",
    "    st.pyplot(fig)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3eb22acd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# Tab ESG\n",
    "# ========================================================================="
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fb8fd1ce",
   "metadata": {},
   "outputs": [],
   "source": [
    "with tab2:\n",
    "    st.write(\"This content is forthcoming\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
