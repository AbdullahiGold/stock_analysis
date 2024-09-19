import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.fundamentaldata import FundamentalData
import datetime

# Calculate stock data basic metrics
def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

# Streamlit Page layout
st.set_page_config(layout="wide")
st.title("Stock Analysis Dashboard")
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'NVDA')
end_date = st.sidebar.date_input('End Date', datetime.date.today())
start_date = st.sidebar.date_input('Start Date', end_date - datetime.timedelta(days=30))
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick Chart', 'Line Chart'])

st.sidebar.header("Purpose")
info = st.sidebar.info("This dashboard is built for in-depth stock market analysis. It allows users to input any stock ticker, select a date range, and instantly view essential financial information in an easy-to-understand format.")

# Download stock data
data = yf.download(ticker, start=start_date, end=end_date)

# Ensure data is not empty before calculating metrics
if not data.empty:
    last_close, change, pct_change, high, low, volume = calculate_metrics(data)
    st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} USD ({pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} USD")
    col2.metric("Low", f"{low:.2f} USD")
    col3.metric("Volume", f"{volume:,}")

    # Plot stock data based on selected chart type
    if chart_type == 'Candlestick Chart':
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
        fig.update_layout(title=f'{ticker} Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
    elif chart_type == 'Line Chart':
        fig = px.line(data, x=data.index, y='Adj Close', title=f'{ticker} Line Chart')


    st.plotly_chart(fig)
else:
    st.error(f"No data available for {ticker} from {start_date} to {end_date}.")

# Tabs for additional data
pricing_data, project_insights = st.tabs(["Pricing Data", "Project Insights"])

with pricing_data:
    st.header("Price Movements")
    data['% Change'] = data['Adj Close'].pct_change()
    data.dropna(inplace=True)
    st.write(data)
    annual_return = data['% Change'].mean() * 252 * 100
    st.write(f'Annual Return: {annual_return:.2f}%')
    stdev = np.std(data['% Change']) * np.sqrt(252)
    st.write(f'Standard Deviation: {stdev*100:.2f}%')
    st.write(f'Risk-Adjusted Return: {annual_return / (stdev*100):.2f}')

with project_insights:
    st.title('Problems Solved')
    st.write('The Stock Analysis Dashboard solves the problem of scattered and time-consuming data gathering by centralizing essential financial information in one place. Users can effortlessly access stock price trends, financial statements, and key metrics without needing to visit multiple sources. Additionally, the dashboard simplifies complex financial analysis by offering visual and quantitative tools, such as interactive charts and risk/return metrics. This integration of data and analysis tools into a user-friendly interface makes financial insights accessible to both novice and experienced users.')
    st.title('Challenges Faced')
    st.write(
        'While developing the dashboard, one of the primary challenges was ensuring that the data from various sources was consistently accurate and up-to-date. This required careful handling of data synchronization and validation to maintain the integrity of the information presented to users. Additionally, the task of calculating financial metrics and presenting them in a way that is both informative and easy to understand posed a design challenge. Balancing the need for detailed analysis with a clean, intuitive user interface was critical to making the dashboard effective for users with varying levels of financial expertise.')
    st.title("Client's Pain Points")
    st.write(
        "The Stock Analysis Dashboard was designed to address specific client pain points, particularly the inefficiencies and complexities of financial data gathering and analysis. Clients often struggle with the time-consuming task of collecting and analyzing stock data from multiple sources. The dashboard alleviates this by consolidating all relevant data in one place, making the analysis process more efficient. Furthermore, by providing tools for visualizing data and calculating key financial metrics, the dashboard meets the client's need for a more robust and user-friendly analysis platform.")
    st.title("Impact on Client's Business")
    st.write(
        "The creation of this dashboard significantly enhances the client’s ability to make informed investment decisions, which can lead to improved financial outcomes. By streamlining data access and analysis, the dashboard increases operational efficiency, allowing the client to focus on strategic decision-making rather than data collection. Ultimately, this tool provides a competitive advantage by offering a comprehensive and easy-to-use solution for financial analysis, making it an invaluable addition to the client’s business.")

