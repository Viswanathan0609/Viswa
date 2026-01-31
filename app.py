import streamlit as st
import pandas as pd

st.title("📊 One-Click Data Summarizer")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head())

    # Rows & Columns
    st.subheader("📐 Dataset Shape")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Missing values
    st.subheader("❓ Missing Values Count")
    st.write(df.isnull().sum())

    # Basic statistics
    st.subheader("📈 Basic Statistics")
    st.write(df.describe())

    # Select numeric column for chart
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select a numeric column for histogram", numeric_cols)

        fig, ax = plt.subplots()
        ax.hist(df[col].dropna())
        ax.set_title(f"Histogram of {col}")

        st.pyplot(fig)
    else:
        st.warning("No numeric columns found for visualization.")
