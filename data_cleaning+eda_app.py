import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Generic Data Cleaning & EDA App",
    layout="wide"
)

st.title("📊 Generic Data Cleaning & EDA Dashboard")

st.sidebar.header("📁 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("Upload a dataset to begin EDA.")
    st.stop()

st.subheader("🔍 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Cells", df.isnull().sum().sum())

with st.expander("Preview Data"):
    st.dataframe(df.head())

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

st.subheader("🧼 Missing Value Summary")

missing_df = df.isnull().sum()
missing_df = missing_df[missing_df > 0]

if missing_df.empty:
    st.success("No missing values detected 🎉")
else:
    st.dataframe(missing_df)


st.sidebar.header("🔎 Filters")

filtered_df = df.copy()

for col in categorical_cols:
    options = st.sidebar.multiselect(
        f"{col}",
        df[col].dropna().unique(),
        default=df[col].dropna().unique()
    )
    filtered_df = filtered_df[filtered_df[col].isin(options)]


st.subheader("📈 Automatic EDA Visualizations")

if categorical_cols:
    cat_col = st.selectbox("Select Categorical Column", categorical_cols)
    fig_cat = px.histogram(filtered_df, x=cat_col, color=cat_col)
    st.plotly_chart(fig_cat, use_container_width=True)

if numeric_cols:
    num_col = st.selectbox("Select Numeric Column", numeric_cols)
    fig_num = px.histogram(filtered_df, x=num_col)
    st.plotly_chart(fig_num, use_container_width=True)


st.subheader("📌 Project-Specific KPIs")

if "Purchased Bike" in df.columns:
    total_customers = df.shape[0]
    bike_buyers = df[df["Purchased Bike"] == "Yes"].shape[0]
    purchase_rate = bike_buyers / total_customers

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Customers", total_customers)
    c2.metric("Bike Buyers", bike_buyers)
    c3.metric("Purchase Rate", f"{purchase_rate:.2%}")

else:
    st.info("No project-specific KPIs detected for this dataset.")
