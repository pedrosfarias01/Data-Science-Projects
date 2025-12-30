import requests
import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly

# Disable SSL warnings for corporate proxy
requests.packages.urllib3.disable_warnings()

pd.options.display.float_format = '{:.2f}'.format

########################################### HEADER #########################################

def main_header():
    st.set_page_config(page_title="Prophet - Currency Prediction", layout="wide")
    st.title("🪙 Prophet Currency Trend")
    st.markdown("<p style='font-size: 11px;'> ProphetCurrencyTrend 2.0 © 2024</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px;'> Created by: Pedro Farias</p>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .header-buttons { display: flex; gap: 10px; margin-bottom: 10px; }
        .header-buttons a { text-decoration: none; color: white; background-color: #0e76a8; padding: 8px 12px; border-radius: 4px; font-size: 14px; font-weight: bold; }
        .header-buttons a.github { background-color: #333; }
        </style>
        <div class="header-buttons">
            <a href="https://www.linkedin.com/in/pedrosfarias/" target="_blank">LinkedIn</a>
            <a href="https://github.com/pedrosfarias01" target="_blank" class="github">GitHub</a>
        </div>
    """, unsafe_allow_html=True)

########################################### MAIN #########################################

def main():
    st.title("Time Series Prediction - Currency Exchange Rates")
    
    base, target = currency_selection()
    df = load_data(base, target)
    
    if df.empty:
        st.warning("Unable to load data. Please try again or select different currencies.")
        st.stop()

    periods = st.slider("Select prediction periods (days):", min_value=30, max_value=365, value=365)
    plot1, forecast = prophet_predict(df, periods)
    
    if plot1 is None or forecast.empty:
        st.error("Unable to generate predictions. Please try again.")
        st.stop()

    # Key predictions
    st.subheader("Key Predictions")
    future_predictions = forecast[len(df):].copy()
    current_value = df['y'].iloc[-1]
    
    tomorrow = future_predictions.iloc[0]
    next_week = future_predictions.iloc[6] if len(future_predictions) > 6 else future_predictions.iloc[-1]
    next_month = future_predictions.iloc[29] if len(future_predictions) > 29 else future_predictions.iloc[-1]
    next_6m = future_predictions.iloc[179] if len(future_predictions) > 179 else future_predictions.iloc[-1]
    next_year = future_predictions.iloc[-1]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Tomorrow", f"{tomorrow['yhat']:.4f}", f"{((tomorrow['yhat'] - current_value) / current_value * 100):.2f}%")
    with col2:
        st.metric("Next Week", f"{next_week['yhat']:.4f}", f"{((next_week['yhat'] - current_value) / current_value * 100):.2f}%")
    with col3:
        st.metric("Next Month", f"{next_month['yhat']:.4f}", f"{((next_month['yhat'] - current_value) / current_value * 100):.2f}%")
    with col4:
        st.metric("6 Months", f"{next_6m['yhat']:.4f}", f"{((next_6m['yhat'] - current_value) / current_value * 100):.2f}%")
    with col5:
        st.metric("1 Year", f"{next_year['yhat']:.4f}", f"{((next_year['yhat'] - current_value) / current_value * 100):.2f}%")

    # Graph
    st.subheader("Detailed Forecast Graph")
    st.markdown(f"""
    - **Yellow dots**: Historical exchange rate data points
    - **Dark blue line**: The main forecast prediction
    - **Light blue shaded area**: Uncertainty interval
    
    The forecast shows the expected trend for the next {periods} days (approximately {periods//365} year{'s' if periods > 365 else ''}).
    *Note: The wider the shaded area, the more uncertainty in the prediction. Long-term forecasts become less reliable.*
    """)
    st.plotly_chart(plot1)

########################################### FUNCTIONS #########################################

def load_data(base, target):
    """Fetch currency data from Frankfurter API (European Central Bank)"""
    try:
        url = f"https://api.frankfurter.app/2015-01-01..?from={base}&to={target}"
        response = requests.get(url, verify=False, timeout=30)
        data = response.json()
        
        rates = {date: values[target] for date, values in data['rates'].items()}
        df = pd.DataFrame(list(rates.items()), columns=['ds', 'y'])
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.sort_values('ds').reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def prophet_predict(df, periods):
    """Generate Prophet predictions"""
    if df.empty or len(df) < 2:
        return None, pd.DataFrame()
    
    with st.spinner('Fitting model and calculating forecasts...'):
        m = Prophet(weekly_seasonality=False)
        m.fit(df)
        future = m.make_future_dataframe(periods=periods, freq='D')
        forecast = m.predict(future)
        fig = plot_plotly(m, forecast)
        
        # Change dots color to yellow
        fig.data[0].marker.color = 'gold'
        
        return fig, forecast

def currency_selection():
    """Currency pair selection UI"""
    currencies = {
        "AUD": "Australian Dollar",
        "BGN": "Bulgarian Lev",
        "BRL": "Brazilian Real",
        "CAD": "Canadian Dollar",
        "CHF": "Swiss Franc",
        "CNY": "Chinese Renminbi Yuan",
        "CZK": "Czech Koruna",
        "DKK": "Danish Krone",
        "EUR": "Euro",
        "GBP": "British Pound",
        "HKD": "Hong Kong Dollar",
        "HUF": "Hungarian Forint",
        "IDR": "Indonesian Rupiah",
        "ILS": "Israeli New Shekel",
        "INR": "Indian Rupee",
        "ISK": "Icelandic Króna",
        "JPY": "Japanese Yen",
        "KRW": "South Korean Won",
        "MXN": "Mexican Peso",
        "MYR": "Malaysian Ringgit",
        "NOK": "Norwegian Krone",
        "NZD": "New Zealand Dollar",
        "PHP": "Philippine Peso",
        "PLN": "Polish Złoty",
        "RON": "Romanian Leu",
        "SEK": "Swedish Krona",
        "SGD": "Singapore Dollar",
        "THB": "Thai Baht",
        "TRY": "Turkish Lira",
        "USD": "United States Dollar",
        "ZAR": "South African Rand",
    }
    
    options = [f"{code} - {name}" for code, name in currencies.items()]
    codes = list(currencies.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        base_idx = st.selectbox("From:", range(len(options)), index=codes.index("GBP"), format_func=lambda i: options[i])
    with col2:
        target_idx = st.selectbox("To:", range(len(options)), index=codes.index("BRL"), format_func=lambda i: options[i])

    if base_idx == target_idx:
        st.error("Please select two different currencies.")
        st.stop()
    
    return codes[base_idx], codes[target_idx]
