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
date_range = st.sidebar.date_input("Select Order Date Range:", [data['Order Date'].min(), data['Order Date'].max()])

filtered_data = data[
    (data['Region'].isin(region)) &
    (data['Category'].isin(category)) &
    (data['Order Date'] >= pd.to_datetime(date_range[0])) &
    (data['Order Date'] <= pd.to_datetime(date_range[1]))
]

# KPI Metrics
st.subheader("📌 Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${filtered_data['Sales'].sum():,.2f}")
kpi2.metric("Total Profit", f"${filtered_data['Profit'].sum():,.2f}")
kpi3.metric("Total Orders", filtered_data['Order ID'].nunique())

# Show filtered data
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_data.head())

# Download filtered data
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

# Sales by Category
st.subheader("💰 Total Sales by Category")
category_sales = filtered_data.groupby('Category')['Sales'].sum().reset_index()
fig1 = px.bar(category_sales, x='Category', y='Sales', color='Category', title="Total Sales by Category")
st.plotly_chart(fig1)

# Profit by Category
st.subheader("📈 Total Profit by Category")
category_profit = filtered_data.groupby('Category')['Profit'].sum().reset_index()
fig1p = px.bar(category_profit, x='Category', y='Profit', color='Category', title="Total Profit by Category")
st.plotly_chart(fig1p)

# Sales by Sub-Category
st.subheader("📦 Sales by Sub-Category")
subcat_sales = filtered_data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()
fig2 = px.bar(subcat_sales, x='Sales', y='Sub-Category', orientation='h', color='Sub-Category', title="Sales by Sub-Category")
st.plotly_chart(fig2)

# Profit by Sub-Category
st.subheader("💹 Profit by Sub-Category")
subcat_profit = filtered_data.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).reset_index()
fig2p = px.bar(subcat_profit, x='Profit', y='Sub-Category', orientation='h', color='Sub-Category', title="Profit by Sub-Category")
st.plotly_chart(fig2p)

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

# Sales and Profit by Segment
st.subheader("👥 Sales and Profit by Customer Segment")
segment_data = filtered_data.groupby('Segment')[['Sales', 'Profit']].sum().reset_index()
fig5 = px.bar(segment_data, x='Segment', y=['Sales', 'Profit'], barmode='group', title="Sales and Profit by Segment")
st.plotly_chart(fig5)

# Ending Section
st.markdown("## Thank You for Exploring the Dashboard!")
st.success("We hope this dashboard helped you uncover valuable insights from the data.")

# Feedback Section
st.markdown("### Your Feedback Matters!")
rating = st.slider("Rate this dashboard experience", 1, 5, 4)
feedback = st.text_area("Any suggestions or comments?")

if st.button("Submit Feedback"):
    st.balloons()
    st.success("Thanks for your feedback! 🚀")

# Developer Info or Footer
st.markdown("---")
st.markdown("**Developed by [Umesh Nagar]**")
st.markdown("🌐 [Visit My GitHub](https://github.com/Umesh-Nagar))
