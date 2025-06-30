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
    st.markdown("<p style='font-size: 11px;'> ProphetCurrencyTrend 2.0 © 2024</p>", unsafe_allow_html=True)
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

    # Get prediction periods
    periods = st.slider("Select prediction periods (days):", min_value=30, max_value=365, value=90)
    
    # Generate predictions
    plot1, forecast = prophet_predict_graph(df, periods)

    # Display key predictions first
    st.subheader("Key Predictions")
    
    # Get only future predictions
    future_predictions = forecast[len(df):].copy()
    
    # Get today's value (last historical point)
    current_value = df['y'].iloc[-1]
    
    # Get predictions for key dates
    tomorrow = future_predictions.iloc[0]
    next_week = future_predictions.iloc[6] if len(future_predictions) > 6 else future_predictions.iloc[-1]
    next_month = future_predictions.iloc[29] if len(future_predictions) > 29 else future_predictions.iloc[-1]
    
    # Create three columns for the metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Tomorrow's Prediction",
            f"{tomorrow['yhat']:.4f}",
            f"{((tomorrow['yhat'] - current_value) / current_value * 100):.2f}%"
        )
    
    with col2:
        st.metric(
            "Next Week",
            f"{next_week['yhat']:.4f}",
            f"{((next_week['yhat'] - current_value) / current_value * 100):.2f}%"
        )
    
    with col3:
        st.metric(
            "Next Month",
            f"{next_month['yhat']:.4f}",
            f"{((next_month['yhat'] - current_value) / current_value * 100):.2f}%"
        )

    # Then display the graph section
    st.subheader("Detailed Forecast Graph")
    
    st.markdown(f"""
    
    - **Blue dots**: Historical exchange rate data points
    - **Dark blue line**: The main forecast prediction
    - **Light blue shaded area**: Uncertainty interval - represents the range of possible values
                
    The forecast shows the expected trend for the next {periods} days, taking into account historical price patterns, weekly seasonality patterns and overall market trends.
    
    *Note: The wider the shaded area gets, the more uncertainty in the prediction. Financial markets can be volatile and affected by many external factors.*
    """)
    
    st.plotly_chart(plot1)

########################################### FUNCTIONS #########################################

def load_and_process_data(pair, years_period=10):

    data = yf.download(tickers=pair, period='max', interval='1d')
    current_year = pd.Timestamp.now().year
    df = data[data.index.astype('datetime64[ns]').year >= (current_year - years_period)]
    df = df.reset_index()
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']

    return df

def prophet_predict_graph(df, periods):
    with st.spinner('Fitting time series model and calculating forecasts...'):
        progress_bar = st.progress(0)
        
        # Fitting the model to historical data
        progress_bar.progress(25)
        m = Prophet(weekly_seasonality=False)
        model = m.fit(df)
        
        # Preparing future dates for prediction
        progress_bar.progress(50)
        future = m.make_future_dataframe(periods=periods, freq='D')
        
        # Generating forecasts
        progress_bar.progress(75)
        forecast = m.predict(future)
        
        # Creating the visualization
        progress_bar.progress(100)
        fig = plot_plotly(m, forecast)  # Use plotly for interactive plotting
        
        # Clear the progress bar
        progress_bar.empty()
        
        return fig, forecast

def currency_selection():
    currencies = ['GBP', 'USD', 'EUR', 'JPY', 'BRL', 'CAD', 'AUD']
    currency1 = st.selectbox("Select Currency 1:", currencies, index=0)
    currency2 = st.selectbox("Select Currency 2:", currencies, index=4)

    if currency1 == currency2:
        st.error("Please select two different currencies.")
        st.stop()  
    else:
        currency_pair = f"{currency1}{currency2}=X"

    return currency_pair