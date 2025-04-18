import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["txn_db"]
collection = db["fraud_alerts"]

# === Streamlit Config ===
st.set_page_config(page_title="🚨 Fraud Detection Dashboard", layout="wide")
st.title("💳 Real-Time Fraud Detection Dashboard")
st.markdown("Live insights from **CatBoost Classifier + Confluent Kafka + MongoDB**")

# === Load Data with Cache ===
@st.cache_data(ttl=30)
def load_data(limit=1000):
    data = list(collection.find().sort("trans_date_trans_time", -1).limit(limit))
    df = pd.DataFrame(data)
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)
    return df

df = load_data()

if df.empty:
    st.warning("No fraud data found.")
    st.stop()

# === Sidebar Filters ===
with st.sidebar:
    st.header("🔍 Filters")
    selected_category = st.multiselect("Category", df["category"].unique())
    selected_gender = st.multiselect("Gender", df["gender"].unique())
    selected_state = st.multiselect("State", df["state"].unique())
    refresh = st.checkbox("Auto-refresh every 30s", value=True)

# === Filter Logic ===
filtered_df = df.copy()
if selected_category:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_category)]
if selected_gender:
    filtered_df = filtered_df[filtered_df["gender"].isin(selected_gender)]
if selected_state:
    filtered_df = filtered_df[filtered_df["state"].isin(selected_state)]

# === KPI Metrics ===
st.markdown("### 📊 Key Fraud Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Fraud Cases", len(filtered_df))
col2.metric("Avg. Fraud Amount", f"${filtered_df['amt'].mean():,.2f}")
col3.metric("Max Amount", f"${filtered_df['amt'].max():,.2f}")

# === Time Processing ===
filtered_df["trans_date_trans_time"] = pd.to_datetime(filtered_df["trans_date_trans_time"])
filtered_df["hour"] = filtered_df["trans_date_trans_time"].dt.hour

# === Tabs ===
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Fraud Map", "📋 Recent Transactions"])

# === Trend Tab ===
with tab1:
    st.subheader("📈 Fraud Trend by Hour")
    hourly_counts = filtered_df.groupby("hour").size().reset_index(name="fraud_count")
    fig_line = px.line(hourly_counts, x="hour", y="fraud_count", markers=True,
                       labels={"hour": "Hour of Day", "fraud_count": "Fraud Count"})
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("👥 Gender Split")
    gender_counts = filtered_df["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]
    fig_pie = px.pie(gender_counts, values="count", names="gender", title="Gender Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

# === Map Tab ===
with tab2:
    st.subheader("🗺️ Fraud Location Map")
    if {"lat", "long"}.issubset(filtered_df.columns):
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="lat",
            lon="long",
            color="amt",
            size="amt",
            hover_data=["city", "state", "amt", "trans_date_trans_time"],
            zoom=3,
            height=500,
            color_continuous_scale="Reds"
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.error("Latitude and Longitude data missing!")

# === Transactions Tab ===
with tab3:
    st.subheader("📋 Recent Fraud Transactions")
    st.dataframe(filtered_df.sort_values(by="trans_date_trans_time", ascending=False).head(20))

# === Last Updated Time ===
st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === Auto-refresh Trigger ===
if refresh:
    st.rerun()
