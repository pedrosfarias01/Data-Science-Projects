import streamlit as st
from streamlit import set_page_config, title, text, write, button, success, caption
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go

pd.options.display.float_format = '{:.2f}'.format

def main_header():
    set_page_config(
    page_title="Prophet - Currency Prediction",
    layout="wide",
    )

    st.title("🪙 Prophet Currency Trend")
    st.markdown("<p style='font-size: 11px;'> ProphetCurrencyTrend 1.1.0 © 2024</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px;'> Created by: Pedro Farias</p>", unsafe_allow_html=True)

    # Add LinkedIn and GitHub buttons
    st.markdown("""
        <style>
        .header-buttons {
            display: flex;
            justify-content: flex-start;
            gap: 10px;
            margin-bottom: 10px;
        }
        .header-buttons a {
            text-decoration: none;
            color: white;
            background-color: #0e76a8;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
        }
        .header-buttons a.github {
            background-color: #333;
        }
        </style>
        <div class="header-buttons">
            <a href="https://www.linkedin.com/in/pedrosfarias/" target="_blank">LinkedIn</a>
            <a href="https://github.com/pedrosfarias01" target="_blank" class="github">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

########################################### MAIN + MENUS #########################################

def main():

    st.title("Time Series Prediction - Currency Exchange Rates")

    currency_pair = currency_selection()

    # Load and process data
    df = load_and_process_data(currency_pair, years_period=10)

    # Display the prediction graph
    st.subheader("Prediction Graph")
    periods = st.slider("Select prediction periods (days):", min_value=30, max_value=365, value=90)
    st.subheader(periods)
    plot1 = prophet_predict_graph(df, periods)
    st.plotly_chart(plot1)

########################################### FUNCTIONS #########################################

def load_and_process_data(pair, years_period=10):

    data = yf.download(tickers=pair, period='max', interval='1d')
    df = data[data.index.year >= (pd.to_datetime("now").year - years_period)]
    df = df.reset_index()
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']

    return df

def prophet_predict_graph(df, periods):

    m = Prophet(weekly_seasonality=False)
    model = m.fit(df)

    future = m.make_future_dataframe(periods=periods, freq='D')
    forecast = m.predict(future)

    fig = plot_plotly(m, forecast)  # Use plotly for interactive plotting
    return fig

def currency_selection():
    # Select currency pairs
    currencies = ['GBP', 'USD', 'EUR', 'JPY', 'BRL', 'CAD', 'AUD']
    currency1 = st.selectbox("Select Currency 1:", currencies, index=0)
    currency2 = st.selectbox("Select Currency 2:", currencies, index=4)

    # Ensure that the selected currencies are not the same
    if currency1 == currency2:
        st.error("Please select two different currencies.")
    else:
        currency_pair = f"{currency1}{currency2}=X"

    return currency_pair