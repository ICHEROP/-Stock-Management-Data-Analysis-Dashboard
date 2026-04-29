import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Management Dashboard", layout="wide")

st.title("📦 Stock Management & Data Analysis Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload your stock CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # Data Cleaning
    df.dropna(inplace=True)

    # Convert Date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Data")

    if 'Category' in df.columns:
        category = st.sidebar.multiselect(
            "Select Category", options=df['Category'].unique(), default=df['Category'].unique()
        )
        df = df[df['Category'].isin(category)]

    if 'Product' in df.columns:
        product = st.sidebar.multiselect(
            "Select Product", options=df['Product'].unique(), default=df['Product'].unique()
        )
        df = df[df['Product'].isin(product)]

    st.subheader("📊 Filtered Data")
    st.dataframe(df)

    # Key Metrics
    st.subheader("📈 Key Metrics")

    total_stock = df['Quantity'].sum()
    total_value = (df['Quantity'] * df['Price']).sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Stock Quantity", total_stock)
    col2.metric("Total Stock Value", f"${total_value:,.2f}")

    # Grouping
    st.subheader("📦 Stock by Category")

    if 'Category' in df.columns:
        category_summary = df.groupby('Category')['Quantity'].sum()

        fig, ax = plt.subplots()
        category_summary.plot(kind='bar', ax=ax)
        ax.set_ylabel("Quantity")
        st.pyplot(fig)

    # Time Series Analysis
    if 'Date' in df.columns:
        st.subheader("📅 Stock Trends Over Time")

        time_series = df.groupby('Date')['Quantity'].sum()

        fig2, ax2 = plt.subplots()
        time_series.plot(ax=ax2)
        ax2.set_ylabel("Quantity")
        st.pyplot(fig2)

    # Low Stock Alert
    st.subheader("⚠️ Low Stock Alert")

    threshold = st.slider("Set Low Stock Threshold", 1, 100, 10)

    low_stock = df[df['Quantity'] < threshold]

    st.write(f"Items below {threshold}:")
    st.dataframe(low_stock)

else:
    st.info("Please upload a CSV file to begin.")