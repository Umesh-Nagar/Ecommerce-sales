import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set default theme for plotly
pio.templates.default = "plotly_white"

# Title and Description
st.title("📊 E-Commerce Sales Dashboard")
st.markdown("""
This app provides interactive visualizations for Superstore e-commerce sales data.
Use the filters to explore insights like sales by category, sub-category, region, and trends over time.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='latin-1')
else:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()

# Preprocessing
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Ship Date'] = pd.to_datetime(data['Ship Date'])

# Sidebar Filters
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Select Region(s):", options=data['Region'].unique(), default=data['Region'].unique())
category = st.sidebar.multiselect("Select Category:", options=data['Category'].unique(), default=data['Category'].unique())

filtered_data = data[(data['Region'].isin(region)) & (data['Category'].isin(category))]

# Show filtered data
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_data.head())

# Sales by Category
st.subheader("💰 Total Sales by Category")
category_sales = filtered_data.groupby('Category')['Sales'].sum().reset_index()
fig1 = px.bar(category_sales, x='Category', y='Sales', color='Category', title="Total Sales by Category")
st.plotly_chart(fig1)

# Sales by Sub-Category
st.subheader("📦 Sales by Sub-Category")
subcat_sales = filtered_data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()
fig2 = px.bar(subcat_sales, x='Sales', y='Sub-Category', orientation='h', color='Sub-Category', title="Sales by Sub-Category")
st.plotly_chart(fig2)

# Monthly Sales Trend
st.subheader("📈 Monthly Sales Trend")
filtered_data['Month'] = filtered_data['Order Date'].dt.to_period('M').astype(str)
monthly_sales = filtered_data.groupby('Month')['Sales'].sum().reset_index()
fig3 = px.line(monthly_sales, x='Month', y='Sales', title="Monthly Sales Trend")
st.plotly_chart(fig3)

# Profit by Region
st.subheader("🌍 Profit by Region")
region_profit = filtered_data.groupby('Region')['Profit'].sum().reset_index()
fig4 = px.pie(region_profit, names='Region', values='Profit', title="Profit Share by Region")
st.plotly_chart(fig4)

st.markdown("---")
