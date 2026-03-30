# eda_pro_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Advanced EDA Tool",
    layout="wide"
)

st.title("🚀 Advanced Data Cleaning & EDA Platform")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.sidebar.header("📁 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if not uploaded_file:
    st.info("Upload a dataset to begin")
    st.stop()

df = load_data(uploaded_file)

# -------------------------------
# BASIC INFO
# -------------------------------
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🧼 Data Cleaning",
    "📈 Visualizations",
    "🧠 Insights"
])

# ===============================
# 📊 OVERVIEW
# ===============================
with tab1:
    st.subheader("Dataset Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Cells", df.isnull().sum().sum())

    with st.expander("Preview Data"):
        st.dataframe(df.head())

    st.subheader("📦 Column Summary")

    summary = pd.DataFrame({
        "Type": df.dtypes,
        "Unique Values": df.nunique(),
        "Missing": df.isnull().sum()
    })

    st.dataframe(summary)

# ===============================
# 🧼 DATA CLEANING
# ===============================
with tab2:
    st.subheader("Missing Value Handling")

    df_clean = df.copy()

    for col in df.columns:
        if df[col].isnull().sum() > 0:

            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**{col}**")

            with col2:
                action = st.selectbox(
                    f"{col}",
                    ["None", "Drop Rows", "Fill Mean", "Fill Median", "Fill Mode"],
                    key=col
                )

            if action == "Drop Rows":
                df_clean = df_clean.dropna(subset=[col])

            elif action == "Fill Mean" and col in numeric_cols:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

            elif action == "Fill Median" and col in numeric_cols:
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())

            elif action == "Fill Mode":
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

    st.success("Cleaning Applied")

    # Download cleaned data
    st.download_button(
        "⬇️ Download Cleaned Dataset",
        df_clean.to_csv(index=False),
        "cleaned_data.csv"
    )

# ===============================
# 📈 VISUALIZATIONS
# ===============================
with tab3:
    st.subheader("Smart Visualizations")

    # Correlation Heatmap
    if len(numeric_cols) > 1:
        st.write("### 🔗 Correlation Heatmap")
        fig_corr = px.imshow(df_clean[numeric_cols].corr(), text_auto=True)
        st.plotly_chart(fig_corr, use_container_width=True)

    # Numeric Distribution
    if numeric_cols:
        st.write("### 📊 Numeric Distribution")
        num_col = st.selectbox("Select Numeric Column", numeric_cols)
        fig = px.histogram(df_clean, x=num_col)
        st.plotly_chart(fig, use_container_width=True)

    # Categorical Distribution
    if categorical_cols:
        st.write("### 📊 Categorical Distribution")
        cat_col = st.selectbox("Select Categorical Column", categorical_cols)
        fig = px.histogram(df_clean, x=cat_col, color=cat_col)
        st.plotly_chart(fig, use_container_width=True)

    # Scatter Plot
    if len(numeric_cols) >= 2:
        st.write("### 🔍 Relationship Explorer")
        x_col = st.selectbox("X-axis", numeric_cols, key="x")
        y_col = st.selectbox("Y-axis", numeric_cols, key="y")

        fig = px.scatter(df_clean, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

    # Box Plot
    if categorical_cols and numeric_cols:
        st.write("### 📦 Category vs Numeric")
        cat = st.selectbox("Category", categorical_cols, key="cat")
        num = st.selectbox("Numeric", numeric_cols, key="num")

        fig = px.box(df_clean, x=cat, y=num)
        st.plotly_chart(fig, use_container_width=True)

# ===============================
# 🧠 INSIGHTS
# ===============================
with tab4:
    st.subheader("Automated Insights")

    insights = []

    # Missing values
    missing_percent = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_percent[missing_percent > 30]

    if not high_missing.empty:
        insights.append(f"⚠️ High missing values in: {list(high_missing.index)}")

    # Skewness
    for col in numeric_cols:
        skew = df[col].skew()
        if abs(skew) > 1:
            insights.append(f"📉 {col} is highly skewed (skew={skew:.2f})")

    # Correlation
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        for i in corr.columns:
            for j in corr.columns:
                if i != j and abs(corr.loc[i, j]) > 0.8:
                    insights.append(f"🔗 Strong correlation between {i} and {j}")

    # Outliers
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]

        if len(outliers) > 0:
            insights.append(f"🚨 {col} has {len(outliers)} outliers")

    # Display
    if insights:
        for ins in insights:
            st.write(ins)
    else:
        st.success("No major issues detected 🎉")
