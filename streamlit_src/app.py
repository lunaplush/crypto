import streamlit as st
import matplotlib.pyplot as plt
import os
import sys

#from cryptonitto import get_finance_data
sys.path.append("/home/luna/Luna/Проекты/ML_system_design/crypto")

import cryptonitto
from cryptonitto.get_finance_data import get_finance_data1
import matplotlib
from utils import get_project_root
import numpy as np
from io import BytesIO

symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
                   "amzn", "tsla", "amd", "nvda", "intc"]

# def display_array(arr, colormap='viridis', width=None):
#   """ display a 2D array in streamlit with a color map"""
#
#   # color map
#   cm = matplotlib.cm.get_cmap(colormap)
#
#   # rgb visualization
#   rgb = cm(arr)
#
#   # display in app
#   st.image(rgb, width=width)



def run_app():
   # print(get_project_root())
    st.title("Criptonitto analysys")


    st.sidebar.image(os.path.join("static", "logo_ods.png"))
    st.sidebar.markdown("# Criptonitto")
    st.sidebar.markdown("## https://t.me/cryptonitto_bot")
    symbol = st.sidebar.selectbox("Криптовалюта:", symbols)


    st.text(symbol)
    df_symbol = get_finance_data1(symbol)
    fig, ax = plt.subplots(1,1)
    ax.set_title(symbol)

    ax.plot(df_symbol.Date, df_symbol.Open)
    st.plotly_chart(fig)







if __name__ == "__main__":
    run_app()