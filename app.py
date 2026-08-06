import streamlit as st
import pandas as pd
import plotly.express as px
from services.market_data import get_historical_data
from services.database import init_db, load_historical_data, save_historical_data

# Initialize the SQLite database on app start
init_db()

st.title("Mini Bloomberg Terminal")

symbol = st.text_input("Enter a stock symbol", value="AAPL").upper()
force_refresh = st.sidebar.button("Force Refresh from API")

if st.button("Search"):
    if symbol:
        df = pd.DataFrame()
        source_used = "Local Cache (SQLite)"

        # 1. Check local SQLite database first (unless force refresh is clicked)
        if not force_refresh:
            df = load_historical_data(symbol)

        # 2. If local cache is empty or force refresh was requested, fetch from API
        if df.empty or force_refresh:
            with st.spinner(f"Fetching data for {symbol}..."):
                df = get_historical_data(symbol)
                if not df.empty:
                    # Save fetched data into SQLite for future cache hits
                    save_historical_data(symbol, df)
                    source_used = "Live API (Yahoo Finance)"

        # 3. Render metrics and chart if data is available
        if df.empty:
            st.error(f"No data found for symbol: {symbol}. Please check and try again.")
        else:
            st.success(f"Successfully loaded data for {symbol}!")
            st.sidebar.info(f"Data Source: **{source_used}**")
            
            latest_row = df.iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Latest Close", f"${latest_row['Close']:.2f}")
            col2.metric("Day High", f"${latest_row['High']:.2f}")
            col3.metric("Day Low", f"${latest_row['Low']:.2f}")
            col4.metric("Volume", f"{int(latest_row['Volume']):,}")
            
            st.subheader("Historical price chart (1 year)")
            chart_df = df.reset_index()
            
            fig = px.line(
                chart_df, 
                x="Date", 
                y="Close", 
                title=f"{symbol} Closing Prices Over Time",
                labels={"Close": "Price (USD)", "Date": "Trading Date"}
            )
            
            st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Please enter a valid stock symbol first.")