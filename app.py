import streamlit as st
import plotly.express as px
from services.market_data import get_historical_data

st.title("Mini Bloomberg Terminal")


symbol = st.text_input("Enter a stock symbol", value="AAPL")


if st.button("Search"):
    if symbol:
        with st.spinner(f"Fetching data for {symbol.upper()}..."):
            
            df = get_historical_data(symbol)
            
            if df.empty:
                st.error(f"No data found for symbol: {symbol.upper()}. Please check and try again.")
            else:
                st.success(f"Successfully loaded data for {symbol.upper()}!")
                
                
                latest_row = df.iloc[-1]
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Latest Close", f"${latest_row['Close']:.2f}")
                col2.metric("Day High", f"${latest_row['High']:.2f}")
                col3.metric("Day Low", f"${latest_row['Low']:.2f}")
                col4.metric("Volume", f"{int(latest_row['Volume']):,}")
                
                
                st.subheader("Historical price chart(1year)")
                chart_df = df.reset_index()
                
                fig = px.line(
                    chart_df, 
                    x="Date", 
                    y="Close", 
                    title=f"{symbol.upper()} Closing Prices Over Time",
                    labels={"Close": "Price (USD)", "Date": "Trading Date"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please enter a valid stock symbol first.")