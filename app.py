import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Advanced Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("../dataset/final_sales_data.csv")

df = load_data()

st.title("📊 Advanced Sales Analytics Dashboard")
st.markdown("### Python + Pandas + Plotly + Streamlit")

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

filtered = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Year"].isin(year))
]

st.subheader("Business Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹ {filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"₹ {filtered['Profit'].sum():,.2f}")
col3.metric("Orders", filtered.shape[0])
col4.metric("Average Discount", round(filtered["Discount"].mean(),2))

st.write("---")

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        filtered.groupby("Category")["Sales"].sum().reset_index(),
        x="Category",
        y="Sales",
        title="Category Wise Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.pie(
        filtered,
        names="Region",
        values="Sales",
        title="Region Wise Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

st.write("---")

fig = px.line(
    filtered.groupby("Month")["Sales"].sum().reset_index(),
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")

fig = px.scatter(
    filtered,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_name="Customer Name",
    title="Sales vs Profit"
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")

st.subheader("Dataset Preview")
st.dataframe(filtered)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "Filtered_Sales.csv",
    "text/csv"
)

st.caption("Developed by Soaib Akhtar | Advanced Sales Analytics Dashboard")