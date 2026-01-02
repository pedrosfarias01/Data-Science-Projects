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
    st.markdown("<p style='font-size: 11px;'> Prophet Currency Trend © 2024</p>", unsafe_allow_html=True)
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

    periods = 365
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

    # Price Indicator Section
    st.subheader("💰 Price Indicator")
    
    # Calculate price zones based on historical percentiles (last 90 days)
    lookback_days = 90
    recent_prices = df['y'].tail(lookback_days)
    
    # Use percentiles: bottom 30% = good, middle 40% = normal, top 30% = high
    price_low = recent_prices.quantile(0.30)   # Below this = good price
    price_high = recent_prices.quantile(0.70)  # Above this = high price
    price_min = recent_prices.min()
    price_max = recent_prices.max()
    
    # Create the price bar visualization and status side by side
    col_bar, col_status = st.columns([2, 1])
    
    with col_bar:
        bar_fig = create_price_bar(current_value, price_low, price_high, price_min, price_max)
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with col_status:
        if current_value >= price_high:
            st.success(f"""
            🟢 **Great Rate!**  
            **Current Rate:** {current_value:.2f}  
            Above the 70th percentile of last {lookback_days} days  
            *(Great: > {price_high:.2f} | Bad: < {price_low:.2f})*
            """)
        elif current_value <= price_low:
            st.error(f"""
            🔴 **Low Rate**  
            **Current Rate:** {current_value:.2f}  
            Below the 30th percentile of last {lookback_days} days  
            *(Great: > {price_high:.2f} | Bad: < {price_low:.2f})*
            """)
        else:
            st.info(f"""
            🟡 **Normal Rate**  
            **Current Rate:** {current_value:.2f}  
            Within typical range of last {lookback_days} days  
            *(Great: > {price_high:.2f} | Bad: < {price_low:.2f})*
            """)
    
    # Explanation in expander below the bar
    with st.expander("💡 What does this mean?"):
        if current_value >= price_high:
            st.markdown(f"""
            ### ✅ Good for: Converting {base} → {target}
            - You'll get **more {target}** for each {base}
            - **1 {base} = {current_value:.2f} {target}** (higher than usual!)
            
            ### ❌ Bad for: Converting {target} → {base}
            - You'll need **more {target}** to get 1 {base}
            - Wait for the rate to drop if you want to convert {target} → {base}
            """)
        elif current_value <= price_low:
            st.markdown(f"""
            ### ❌ Bad for: Converting {base} → {target}
            - You'll get **less {target}** for each {base}
            - **1 {base} = {current_value:.2f} {target}** (lower than usual)
            - Consider waiting for the rate to increase
            
            ### ✅ Good for: Converting {target} → {base}
            - You'll need **less {target}** to get 1 {base}
            - Good time to convert {target} → {base}
            """)
        else:
            st.markdown(f"""
            ### 🔄 Normal conditions for both directions
            - **{base} → {target}**: 1 {base} = {current_value:.2f} {target}
            - **{target} → {base}**: 1 {target} = {1/current_value:.2f} {base}
            
            The rate is within the typical range. Neither particularly good nor bad timing for either direction.
            """)
    
    # Trend Analysis Section
    with st.expander("📈 Trend Analysis & Recommendation"):
        # Calculate recent trends
        last_7_days = df['y'].tail(7).mean()
        prev_7_days = df['y'].tail(14).head(7).mean()
        last_30_days = df['y'].tail(30).mean()
        prev_30_days = df['y'].tail(60).head(30).mean()
        
        weekly_change = ((last_7_days - prev_7_days) / prev_7_days) * 100
        monthly_change = ((last_30_days - prev_30_days) / prev_30_days) * 100
        
        # Get Prophet's forecast
        forecast_tomorrow = tomorrow['yhat']
        forecast_week = next_week['yhat']
        forecast_month = next_month['yhat']
        
        tomorrow_change = ((forecast_tomorrow - current_value) / current_value) * 100
        week_change = ((forecast_week - current_value) / current_value) * 100
        month_change = ((forecast_month - current_value) / current_value) * 100
        
        # Display trend info
        col_past, col_future = st.columns(2)
        
        with col_past:
            st.markdown("### 📊 Recent Trend")
            weekly_icon = "📈" if weekly_change > 0 else "📉"
            monthly_icon = "📈" if monthly_change > 0 else "📉"
            st.markdown(f"""
            - **Last 7 days:** {weekly_icon} {weekly_change:+.2f}%
            - **Last 30 days:** {monthly_icon} {monthly_change:+.2f}%
            """)
        
        with col_future:
            st.markdown("### 🔮 Forecast")
            tomorrow_icon = "📈" if tomorrow_change > 0 else "📉"
            week_icon = "📈" if week_change > 0 else "📉"
            month_icon = "📈" if month_change > 0 else "📉"
            st.markdown(f"""
            - **Tomorrow:** {tomorrow_icon} {forecast_tomorrow:.2f} ({tomorrow_change:+.2f}%)
            - **Next week:** {week_icon} {forecast_week:.2f} ({week_change:+.2f}%)
            - **Next month:** {month_icon} {forecast_month:.2f} ({month_change:+.2f}%)
            """)
        
        # Generate recommendation
        st.markdown("### 💡 Recommendation")
        
        # Logic for recommendation
        trend_up = weekly_change > 0.5 and month_change > 0
        trend_down = weekly_change < -0.5 and month_change < 0
        forecast_up = week_change > 0.5
        forecast_down = week_change < -0.5
        
        if current_value >= price_high:
            if forecast_down:
                st.warning(f"""
                **For {base} → {target}:** The rate is great now, but forecast suggests it might drop. 
                """)
            else:
                st.success(f"""
                **For {base} → {target}:** Excellent time to exchange! Rate is high and trend looks stable/positive.
                """)
        elif current_value <= price_low:
            if forecast_up:
                st.info(f"""
                **For {base} → {target}:** Rate is low, but forecast suggests improvement.
                **Consider waiting** a few days for a better rate.
                """)
            else:
                st.error(f"""
                **For {base} → {target}:** Rate is low and not expected to improve soon.
                **Wait if possible**, or exchange only if urgent.
                """)
        else:
            if forecast_up:
                st.info(f"""
                **For {base} → {target}:** Rate is normal, but forecast suggests it might increase.
                **Consider waiting** for a potentially better rate.
                """)
            elif forecast_down:
                st.warning(f"""
                **For {base} → {target}:** Rate is normal, but forecast suggests it might decrease.
                **Consider exchanging soon** before the rate drops.
                """)
            else:
                st.info(f"""
                **For {base} → {target}:** Rate is normal with no strong trend either way.
                **Exchange when convenient** - timing is neutral.
                """)

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

def create_price_bar(current_price, price_low, price_high, price_min, price_max):
    """Creates a simple horizontal bar price indicator based on historical percentiles"""
    import plotly.graph_objects as go
    
    # Use historical min/max as bar boundaries
    bar_min = price_min
    bar_max = price_max
    
    # Determine status based on percentiles
    if current_price >= price_high:
        status = "Great Rate"
        status_color = "#22c55e"
    elif current_price <= price_low:
        status = "Low Rate"
        status_color = "#ef4444"
    else:
        status = "Normal Rate"
        status_color = "#3b82f6"
    
    fig = go.Figure()
    
    # Add colored bar segments (red = low 30%, yellow = middle 40%, green = high 30%)
    fig.add_shape(type="rect", x0=bar_min, x1=price_low, y0=0.4, y1=0.6,
                  fillcolor='#ef4444', line=dict(width=0))
    fig.add_shape(type="rect", x0=price_low, x1=price_high, y0=0.4, y1=0.6,
                  fillcolor='#fbbf24', line=dict(width=0))
    fig.add_shape(type="rect", x0=price_high, x1=bar_max, y0=0.4, y1=0.6,
                  fillcolor='#22c55e', line=dict(width=0))
    
    # Add border
    fig.add_shape(type="rect", x0=bar_min, x1=bar_max, y0=0.4, y1=0.6,
                  line=dict(color="#64748b", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Add current price marker (just the dot, price is shown in status container)
    fig.add_trace(go.Scatter(
        x=[current_price], y=[0.5],
        mode='markers',
        marker=dict(size=18, color='white', line=dict(color='#1e293b', width=3)),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add status label
    fig.add_annotation(
        x=current_price, y=0.85,
        text=f"<b>{status}</b>",
        showarrow=False,
        font=dict(size=14, color='white'),
        bgcolor=status_color,
        borderpad=8,
        opacity=0.9
    )
    
    # Add range labels (min and max from last 90 days)
    fig.add_annotation(x=bar_min, y=0.15, text=f"Min: {bar_min:.2f}",
                       showarrow=False, font=dict(size=10, color='#94a3b8'))
    fig.add_annotation(x=bar_max, y=0.15, text=f"Max: {bar_max:.2f}",
                       showarrow=False, font=dict(size=10, color='#94a3b8'))
    
    fig.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 1]),
        showlegend=False
    )
    
    return fig

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
        base_idx = st.selectbox("From:", range(len(options)), index=codes.index("USD"), format_func=lambda i: options[i])
    with col2:
        target_idx = st.selectbox("To:", range(len(options)), index=codes.index("BRL"), format_func=lambda i: options[i])

    if base_idx == target_idx:
        st.error("Please select two different currencies.")
        st.stop()
    
    return codes[base_idx], codes[target_idx]
