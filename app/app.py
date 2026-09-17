import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Advanced Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Advanced Sales Analytics Dashboard")
st.markdown("### Analyze Sales, Profit and Business Performance")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("../dataset/final_sales_data.csv")

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Year"].isin(year))
]

# -----------------------------
# KPI Cards
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_discount = filtered_df["Discount"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.2f}")
col2.metric("📈 Total Profit", f"₹ {total_profit:,.2f}")
col3.metric("📦 Orders", total_orders)
col4.metric("🏷 Avg Discount", f"{avg_discount:.2%}")

st.markdown("---")
# -----------------------------
# Category Wise Sales
# -----------------------------
st.subheader("📊 Category Wise Sales")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=True,
    title="Category Wise Sales"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Region Wise Sales
# -----------------------------
st.subheader("🌍 Region Wise Sales")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    hole=0.4,
    title="Region Wise Sales"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Category Wise Profit
# -----------------------------
st.subheader("💰 Category Wise Profit")

category_profit = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Category",
    text_auto=True,
    title="Category Wise Profit"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Monthly Sales Trend
# -----------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# -----------------------------
# Top 10 Customers
# -----------------------------
st.subheader("👤 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_customers, use_container_width=True)

# -----------------------------
# Top 10 Products
# -----------------------------
st.subheader("🛍️ Top 10 Products")

top_products = (
    filtered_df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_products, use_container_width=True)

# -----------------------------
# Sales vs Profit Scatter Plot
# -----------------------------
st.subheader("📉 Sales vs Profit")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_name="Customer Name",
    title="Sales vs Profit Analysis"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# Download CSV
# -----------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.write("---")

st.markdown(
    """
### 👨‍💻 Developed By

**Soaib Akhtar**

B.Tech CSE

Advanced Sales Data Analytics Dashboard

Python | Pandas | NumPy | Matplotlib | Streamlit
"""
)