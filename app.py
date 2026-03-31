import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Data Cleaning and EDA Tool", layout="wide")

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f5f7fa, #e4ecf7);
}

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #2E7D32);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

h2 {
    color: #2C3E50;
}

.insight-box {
    background-color: #ffffff;
    padding: 12px;
    border-radius: 10px;
    border-left: 6px solid #4CAF50;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Advanced Data Cleaning & EDA")

# -------------------------------
# SIDEBAR
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

with st.spinner("Loading dataset..."):
    df = load_data(uploaded_file)

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()


st.sidebar.header("⚙️ Controls")

show_raw = st.sidebar.toggle("Show Raw Data")
enable_filters = st.sidebar.toggle("Enable Filters")
auto_mode = st.sidebar.button("⚡ Auto Analyze")

df_clean = df.copy()


if enable_filters:
    st.sidebar.subheader("🔎 Filters")
    for col in categorical_cols:
        selected = st.sidebar.multiselect(
            f"{col}",
            df[col].dropna().unique(),
            default=df[col].dropna().unique()
        )
        df_clean = df_clean[df_clean[col].isin(selected)]


tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🧼 Cleaning",
    "📈 Visualizations",
    "🧠 Insights"
])

with tab1:
    st.subheader("Dataset Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", df_clean.shape[0])
    c2.metric("Columns", df_clean.shape[1])
    c3.metric("Missing Cells", df_clean.isnull().sum().sum())

    with st.expander("Preview Data"):
        st.dataframe(df_clean.head())

    st.subheader("📦 Column Summary")

    summary = pd.DataFrame({
        "Type": df_clean.dtypes,
        "Unique Values": df_clean.nunique(),
        "Missing": df_clean.isnull().sum()
    })

    st.dataframe(summary)

    if show_raw:
        st.subheader("📄 Full Dataset")
        st.dataframe(df_clean)


with tab2:
    st.subheader("Missing Value Handling")

    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:

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

    st.success("Cleaning Applied ✅")

    st.download_button(
        "⬇️ Download Cleaned Dataset",
        df_clean.to_csv(index=False),
        "cleaned_data.csv"
    )


with tab3:
    st.subheader("Smart Visualizations")

    if len(numeric_cols) > 1:
        st.write("### 🔗 Correlation Heatmap")
        fig_corr = px.imshow(df_clean[numeric_cols].corr(), text_auto=True)
        st.plotly_chart(fig_corr, use_container_width=True)

    if numeric_cols:
        st.write("### 📊 Numeric Distribution")
        num_col = st.selectbox("Select Numeric Column", numeric_cols)

        fig = px.histogram(
            df_clean,
            x=num_col,
            color_discrete_sequence=["#4CAF50"]
        )

        fig.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    if categorical_cols:
        st.write("### 📊 Categorical Distribution")
        cat_col = st.selectbox("Select Categorical Column", categorical_cols)

        fig = px.histogram(
            df_clean,
            x=cat_col,
            color=cat_col
        )

        st.plotly_chart(fig, use_container_width=True)

    if len(numeric_cols) >= 2:
        st.write("### 🔍 Relationship Explorer")
        x_col = st.selectbox("X-axis", numeric_cols, key="x")
        y_col = st.selectbox("Y-axis", numeric_cols, key="y")

        fig = px.scatter(df_clean, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

    if categorical_cols and numeric_cols:
        st.write("### 📦 Category vs Numeric")
        cat = st.selectbox("Category", categorical_cols, key="cat")
        num = st.selectbox("Numeric", numeric_cols, key="num")

        fig = px.box(df_clean, x=cat, y=num)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top Categories")

    if categorical_cols:
        col = st.selectbox("Select Column", categorical_cols, key="topcat")
        top_n = st.slider("Top N", 3, 20, 10)

        top_data = df_clean[col].value_counts().head(top_n)

        fig = px.bar(
            x=top_data.index,
            y=top_data.values,
            color=top_data.values,
            color_continuous_scale="greens"
        )

        st.plotly_chart(fig, use_container_width=True)


with tab4:
    st.subheader("Automated Insights")

    insights = []

    missing_percent = (df_clean.isnull().sum() / len(df_clean)) * 100
    high_missing = missing_percent[missing_percent > 30]

    if not high_missing.empty:
        insights.append(f"⚠️ High missing values in: {list(high_missing.index)}")

    for col in numeric_cols:
        skew = df_clean[col].skew()
        if abs(skew) > 1:
            insights.append(f"📉 {col} is highly skewed (skew={skew:.2f})")

    if len(numeric_cols) > 1:
        corr = df_clean[numeric_cols].corr()
        for i in corr.columns:
            for j in corr.columns:
                if i != j and abs(corr.loc[i, j]) > 0.8:
                    insights.append(f"🔗 Strong correlation between {i} and {j}")

    for col in numeric_cols:
        q1 = df_clean[col].quantile(0.25)
        q3 = df_clean[col].quantile(0.75)
        iqr = q3 - q1

        outliers = df_clean[
            (df_clean[col] < q1 - 1.5 * iqr) |
            (df_clean[col] > q3 + 1.5 * iqr)
        ]

        if len(outliers) > 0:
            insights.append(f"🚨 {col} has {len(outliers)} outliers")

    if auto_mode:
        st.subheader("⚡ Auto Analysis Report")

        st.write(f"- {len(numeric_cols)} numeric features detected")
        st.write(f"- {len(categorical_cols)} categorical features detected")

        if len(df_clean) > 10000:
            st.warning("Large dataset detected — consider sampling")

        st.success("Auto analysis complete ✅")

    if insights:
        for ins in insights:
            st.markdown(
                f'<div class="insight-box">{ins}</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("No major issues detected 🎉")
