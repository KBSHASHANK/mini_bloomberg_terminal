import streamlit as st
from datetime import date

from services.portfolio import (
    add_stock,
    load_portfolio,
    delete_stock
)

st.set_page_config(page_title="Portfolio", page_icon="📈")

st.title("📈 Portfolio Manager")

# -----------------------------
# Add Stock Section
# -----------------------------

st.header("Add Stock")

with st.form("portfolio_form"):

    ticker = st.text_input("Ticker Symbol").upper()

    shares = st.number_input(
        "Shares",
        min_value=0.01,
        value=1.0,
        step=1.0
    )

    buy_price = st.number_input(
        "Buy Price ($)",
        min_value=0.01,
        value=100.0
    )

    purchase_date = st.date_input(
        "Purchase Date",
        value=date.today()
    )

    submitted = st.form_submit_button("Add Stock")

    if submitted:

        if ticker == "":
            st.error("Please enter a ticker symbol.")

        else:

            add_stock(
                ticker=ticker,
                shares=shares,
                buy_price=buy_price,
                purchase_date=str(purchase_date)
            )

            st.success(f"{ticker} added successfully!")

# -----------------------------
# Portfolio Table
# -----------------------------

st.header("Current Portfolio")

portfolio_df = load_portfolio()

if portfolio_df.empty:

    st.info("Your portfolio is empty.")

else:

    st.dataframe(
        portfolio_df,
        use_container_width=True
    )

# -----------------------------
# Delete Stock
# -----------------------------

st.header("Delete Stock")

stock_id = st.number_input(
    "Portfolio ID",
    min_value=1,
    step=1
)

if st.button("Delete"):

    delete_stock(stock_id)

    st.success("Stock deleted successfully!")

    st.rerun()