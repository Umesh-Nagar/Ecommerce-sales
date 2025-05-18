{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4b0df453-6265-44e4-b1db-20a3ffcb7ef9",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-05-18 14:28:54.415 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\91911\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import plotly.io as pio\n",
    "\n",
    "# Set default theme for plotly\n",
    "pio.templates.default = \"plotly_white\"\n",
    "\n",
    "# Title and Description\n",
    "st.title(\"📊 E-Commerce Sales Dashboard\")\n",
    "st.markdown(\"\"\"\n",
    "This app provides interactive visualizations for Superstore e-commerce sales data.\n",
    "Use the filters to explore insights like sales by category, sub-category, region, and trends over time.\n",
    "\"\"\")\n",
    "\n",
    "# Load Data\n",
    "data = pd.read_csv(\"Sample - Superstore.csv\", encoding='latin-1')\n",
    "\n",
    "# Preprocessing\n",
    "data['Order Date'] = pd.to_datetime(data['Order Date'])\n",
    "data['Ship Date'] = pd.to_datetime(data['Ship Date'])\n",
    "\n",
    "# Sidebar Filters\n",
    "st.sidebar.header(\"Filter Options\")\n",
    "region = st.sidebar.multiselect(\"Select Region(s):\", options=data['Region'].unique(), default=data['Region'].unique())\n",
    "category = st.sidebar.multiselect(\"Select Category:\", options=data['Category'].unique(), default=data['Category'].unique())\n",
    "\n",
    "filtered_data = data[(data['Region'].isin(region)) & (data['Category'].isin(category))]\n",
    "\n",
    "# Show filtered data\n",
    "st.subheader(\"📄 Filtered Data Preview\")\n",
    "st.dataframe(filtered_data.head())\n",
    "\n",
    "# Sales by Category\n",
    "st.subheader(\"💰 Total Sales by Category\")\n",
    "category_sales = filtered_data.groupby('Category')['Sales'].sum().reset_index()\n",
    "fig1 = px.bar(category_sales, x='Category', y='Sales', color='Category', title=\"Total Sales by Category\")\n",
    "st.plotly_chart(fig1)\n",
    "\n",
    "# Sales by Sub-Category\n",
    "st.subheader(\"📦 Sales by Sub-Category\")\n",
    "subcat_sales = filtered_data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()\n",
    "fig2 = px.bar(subcat_sales, x='Sales', y='Sub-Category', orientation='h', color='Sub-Category', title=\"Sales by Sub-Category\")\n",
    "st.plotly_chart(fig2)\n",
    "\n",
    "# Monthly Sales Trend\n",
    "st.subheader(\"📈 Monthly Sales Trend\")\n",
    "filtered_data['Month'] = filtered_data['Order Date'].dt.to_period('M').astype(str)\n",
    "monthly_sales = filtered_data.groupby('Month')['Sales'].sum().reset_index()\n",
    "fig3 = px.line(monthly_sales, x='Month', y='Sales', title=\"Monthly Sales Trend\")\n",
    "st.plotly_chart(fig3)\n",
    "\n",
    "# Profit by Region\n",
    "st.subheader(\"🌍 Profit by Region\")\n",
    "region_profit = filtered_data.groupby('Region')['Profit'].sum().reset_index()\n",
    "fig4 = px.pie(region_profit, names='Region', values='Profit', title=\"Profit Share by Region\")\n",
    "st.plotly_chart(fig4)\n",
    "\n",
    "st.markdown(\"---\")\n",
    "st.markdown(\"Made with ❤️ using Streamlit\")\n"
   ]
  },
  {
   "cell_type": "code",
   "id": "c458ac3a-9ede-488b-84f2-0c3c1c319743",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
