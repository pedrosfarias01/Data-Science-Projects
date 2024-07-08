# Prophet Currency Trend Prediction

## Overview

**Prophet Currency Trend Prediction** is a web application designed to predict currency exchange rates using the Prophet forecasting model. This project demonstrates my proficiency with data science frameworks and web application deployment using Streamlit. The app provides an interactive and intuitive interface for users to visualize historical data and predict future currency trends.

This project aims to:
- Predict future currency exchange rates using historical data.
- Provide an interactive web interface for users to select different currency pairs and forecast periods.
- Utilize the Prophet library for robust time series forecasting.
- Deploy the application using Streamlit for easy accessibility and user interaction.

### Frameworks and Libraries

- **Streamlit**: For building and deploying the interactive web application.
- **yFinance**: To fetch historical currency exchange rate data.
- **Prophet**: For time series forecasting and trend prediction.
- **Pandas**: For data manipulation and preprocessing.
- **Plotly**: For creating interactive plots and visualizations.

### Implementation

1. **Data Fetching and Processing**:
    - Historical exchange rate data is fetched using the `yFinance` library.
    - Data is filtered and preprocessed using `pandas` to fit the requirements of the Prophet model.

2. **Forecasting**:
    - The Prophet model is used to fit the historical data and make future predictions.
    - Users can select the currency pairs and the number of days for forecasting using Streamlit widgets.

3. **Visualization**:
    - Interactive plots are generated using `Plotly` to visualize both historical data and future predictions.

### Streamlit Application

The application is deployed on Streamlit, providing an easy-to-use interface for currency trend prediction. Users can interact with the app by selecting different currency pairs and setting the prediction period. The results are displayed in an interactive plot that shows historical data and future trends.

### How to Use

1. **Open the Application**:
    - Access the application through the deployed Streamlit link [here](https://prophetcurrencytrend.streamlit.app/).

2. **Select Currencies**:
    - Choose the base and quote currencies from the dropdown menus.

3. **Set Prediction Period**:
    - Adjust the slider to set the number of days for the prediction.

4. **View Results**:
    - The application will display the historical data and predicted trends in an interactive plot.

## Conclusion

The Prophet Currency Trend Prediction app is a valuable tool for making informed decisions about currency exchange, whether for travel, investment, or business purposes. By leveraging advanced time series forecasting with Prophet and offering a user-friendly interface via Streamlit, the app enables users to analyze historical trends and predict future exchange rates, helping them choose the best time to buy or sell currency.

Thank you for visiting my project!
