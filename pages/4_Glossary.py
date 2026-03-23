import streamlit as st
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.switch_page("app.py")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

from data_setup import get_data

st.set_page_config(page_title="CEO Dashboard", layout="wide")
with st.sidebar:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Login.py")

st.markdown("""
<style>
/* Main page background */
[data-testid="stAppViewContainer"] {
    background-color: #A0D1FF;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #055296;
}


/* Remove column padding completely */
[data-testid="column"] {
    padding-left: 0px !important;
    padding-right: 0px !important;
}

/* Reduce space inside metric */
[data-testid="stMetric"] {
    padding: 5px 5px !important;
}

/* Reduce metric value size */
[data-testid="stMetricValue"] {
    font-size: 36px !important;
    font-weight:600 !important;
}

[data-testid="stMetricLabel"] {
    font-size: 16px !important;
}

/* Optional: reduce delta size */
[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Sidebar text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Filters text */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: white !important;
}

/* Logout button */
[data-testid="stSidebar"] .stButton > button {
    background-color: black !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Logout button hover */
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #222222 !important;
}

</style>
""", unsafe_allow_html=True)

st.subheader("📖 KPI Glossary For CEO Dashboard")
# ================= CEO Dashboard Metric Definitions ================= #

col1 , col2 = st.columns(2)
with col1:  
    with st.expander("📦 Total Orders"):
        st.write("**Meaning:** Total number of unique orders placed by customers.")
        st.write("**Formula:** COUNT(DISTINCT order_id)")
with col2: 
    with st.expander("💰 Total Net Revenue"):
        st.write("**Meaning:** Revenue after deducting refunds.")
        st.write("**Formula:** SUM(price_usd) - SUM(refund_amount_usd)")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("🌐 Total Sessions"):
        st.write("**Meaning:** Total number of website visits.")
        st.write("**Formula:** COUNT(DISTINCT website_session_id)")
with col2:
    with st.expander("👥 Total Customers"):
        st.write("**Meaning:** Total unique customers who placed orders.")
        st.write("**Formula:** COUNT(DISTINCT user_id)")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("📊 Profit Margin %"):
        st.write("**Meaning:** Percentage of profit earned from total revenue.")
        st.write("**Formula:** (Total Profit / Total Revenue) * 100")
with col2:
    with st.expander("📦 Total Order Items"):
        st.write("**Meaning:** Total number of items sold across all orders.")
        st.write("**Formula:** COUNT(order_item_id)")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("🔁 Refund Item Rate %"):
        st.write("**Meaning:** Percentage of items that were refunded.")
        st.write("**Formula:** (Refunded Items / Total Items) * 100")
with col2:
    with st.expander("🔁 Refund Order Rate %"):
        st.write("**Meaning:** Percentage of orders that had at least one refund.")
        st.write("**Formula:** (Refunded Orders / Total Orders) * 100")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("👥 Repeat Customer %"):
        st.write("**Meaning:** Percentage of customers who made more than one purchase.")
        st.write("**Formula:** (Repeat Customers / Total Customers) * 100")
with col2:
    with st.expander("🆕 One Time Customer %"):
        st.write("**Meaning:** Percentage of customers who purchased only once.")
        st.write("**Formula:** (One-time Customers / Total Customers) * 100")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("💵 Total Profit"):
        st.write("**Meaning:** Earnings after subtracting total cost from revenue.")
        st.write("**Formula:** Total Revenue - Total Cost")
with col2:
    with st.expander("💸 Total Cost"):
        st.write("**Meaning:** Total cost incurred to fulfill orders.")
        st.write("**Formula:** SUM(cogs_usd) - SUM(order_item_refund_cost)")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("↩️ Total Refund"):
        st.write("**Meaning:** Total amount refunded to customers.")
        st.write("**Formula:** SUM(refund_amount_usd)")
with col2:
    with st.expander("🛒 Average Order Value"):
        st.write("**Meaning:** Average revenue generated per order.")
        st.write("**Formula:** Total Revenue / Total Orders")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("📊 Profit Percentage"):
        st.write("**Meaning:** Profit relative to total cost.")
        st.write("**Formula:** (Total Profit / Total Cost) * 100")
with col2:
    with st.expander("📦 Refunded Item Cost"):
        st.write("**Meaning:** Cost associated with refunded items.")
        st.write("**Formula:** SUM(order_item_refund_cost)")

col1 , col2 = st.columns(2)
with col1:
    with st.expander("📉 Refund Amount Rate %"):
        st.write("**Meaning:** Percentage of revenue lost due to refunds.")
        st.write("**Formula:** (Total Refund / Total Net Revenue) * 100")
with col2:
    with st.expander("💰 Avg Profit Per Customer"):
        st.write("**Meaning:** Average profit generated per customer.")
        st.write("**Formula:** Total Profit / Total Customers")
        
st.subheader("📖 KPI Glossary For Website Manager Dashboard")
col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🌐 Total Sessions"):
        st.write("**Meaning:** Total number of website visits.")
        st.write("**Formula:** COUNT(DISTINCT website_session_id)")

with col2:
    with st.expander("📦 Total Orders"):
        st.write("**Meaning:** Total number of orders placed.")
        st.write("**Formula:** COUNT(DISTINCT order_id)")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("👥 Total Visitors"):
        st.write("**Meaning:** Total unique users who visited the website.")
        st.write("**Formula:** COUNT(DISTINCT user_id)")

with col2:
    with st.expander("💰 Net Revenue Per Session"):
        st.write("**Meaning:** Average revenue generated per session after refunds.")
        st.write("**Formula:** (Total Revenue - Total Refund) / Total Sessions")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🆕 One Time Sessions"):
        st.write("**Meaning:** Sessions from users visiting for the first time.")
        st.write("**Formula:** COUNT(website_session_id WHERE is_repeat_session = 0)")

with col2:
    with st.expander("🔁 Repeat Session %"):
        st.write("**Meaning:** Percentage of sessions from returning users.")
        st.write("**Formula:** (Repeat Sessions / Total Sessions) * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("👥 Repeat Visitors"):
        st.write("**Meaning:** Number of users who visited more than once.")
        st.write("**Formula:** COUNT(DISTINCT user_id WHERE is_repeat_session = 1)")

with col2:
    with st.expander("🆕 One Time Visitors"):
        st.write("**Meaning:** Users who visited only once.")
        st.write("**Formula:** COUNT(DISTINCT user_id WHERE is_repeat_session = 0)")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🚪 Bounce Sessions"):
        st.write("**Meaning:** Sessions with only one pageview.")
        st.write("**Formula:** COUNT(website_session_id WHERE pageviews = 1)")

with col2:
    with st.expander("⚠️ Bounce Rate"):
        st.write("**Meaning:** Percentage of sessions with only one pageview.")
        st.write("**Formula:** (Bounce Sessions / Total Sessions) * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("📈 Conversion Rate"):
        st.write("**Meaning:** Percentage of sessions that resulted in an order.")
        st.write("**Formula:** (Converted Sessions / Total Sessions) * 100")

with col2:
    with st.expander("✅ Converted Sessions"):
        st.write("**Meaning:** Sessions that resulted in a purchase.")
        st.write("**Formula:** COUNT(DISTINCT website_session_id FROM orders)")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("📄 Avg Pages Per Session"):
        st.write("**Meaning:** Average number of pages viewed per session.")
        st.write("**Formula:** Total Pageviews / Total Sessions")

with col2:
    with st.expander("📊 Avg Session Per User"):
        st.write("**Meaning:** Average number of sessions per user.")
        st.write("**Formula:** Total Sessions / Total Users")


st.subheader("📖 KPI Glossary For Marketing Manager Dashboard")
# ================= Marketing Manager Metric Definitions ================= #

col1 , col2 = st.columns(2)

with col1: 
    with st.expander("👥 Total Visitors"):
        st.write("**Meaning:** Total unique users who visited the website.")
        st.write("**Formula:** COUNT(DISTINCT user_id)")

with col2:
    with st.expander("🆕 One Time Visitors %"):
        st.write("**Meaning:** Percentage of visitors who visited only once.")
        st.write("**Formula:** (One-time Visitors / Total Visitors) * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("📈 Conversion Rate %"):
        st.write("**Meaning:** Percentage of sessions that resulted in an order.")
        st.write("**Formula:** (Converted Sessions / Total Sessions) * 100")

with col2:
    with st.expander("🛒 Cart Abandonment Rate"):
        st.write("**Meaning:** Percentage of users who added items to cart but did not complete purchase.")
        st.write("**Formula:** (Sessions with Cart - Sessions with Orders) / Sessions with Cart * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🏆 Top Traffic Source by Session"):
        st.write("**Meaning:** Traffic source generating the highest number of sessions.")
        st.write("**Formula:** Channel with MAX(total sessions)")

with col2:
    with st.expander("🔎 Gsearch Conversion Rate"):
        st.write("**Meaning:** Conversion rate for Google Search traffic.")
        st.write("**Formula:** (Orders from gsearch / Sessions from gsearch) * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🆓 Free Channel Revenue"):
        st.write("**Meaning:** Revenue from organic and direct traffic sources.")
        st.write("**Formula:** SUM(revenue WHERE channel IN ('Direct','Organic Search','Organic Social'))")

with col2:
    with st.expander("💳 Paid Channel Revenue"):
        st.write("**Meaning:** Revenue generated from paid marketing campaigns.")
        st.write("**Formula:** SUM(revenue WHERE channel IN ('Paid Search','Paid Social'))")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("👥 Repeat Visitors"):
        st.write("**Meaning:** Users who visited more than once.")
        st.write("**Formula:** COUNT(DISTINCT user_id WHERE is_repeat_session = 1)")

with col2:
    with st.expander("🔁 Repeat Visitors %"):
        st.write("**Meaning:** Percentage of visitors who returned.")
        st.write("**Formula:** (Repeat Visitors / Total Visitors) * 100")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("🔁 Repeat Session Rate %"):
        st.write("**Meaning:** Percentage of sessions from returning users.")
        st.write("**Formula:** (Repeat Sessions / Total Sessions) * 100")

with col2:
    with st.expander("📅 Avg Days Since First Session"):
        st.write("**Meaning:** Average time gap between first visit and current session.")
        st.write("**Formula:** AVG(days_since_first_session)")


col1 , col2 = st.columns(2)

with col1: 
    with st.expander("📢 Top Campaign by Repeat Visitors"):
        st.write("**Meaning:** Campaign generating the highest number of repeat visitors.")
        st.write("**Formula:** Campaign with MAX(repeat visitors)")

with col2:
    with st.expander("🌐 Total Sessions"):
        st.write("**Meaning:** Total number of sessions on the website.")
        st.write("**Formula:** COUNT(DISTINCT website_session_id)")


        
