from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Loan & Credit Data Analysis", page_icon="📊", layout="wide")

ROOT = Path(__file__).parent
DEFAULT_DATA = ROOT / "data" / "loan_credit_data.csv"

st.title("📊 Loan & Credit Data Analysis")
st.caption("Explore loan applications, applicant profiles, and credit-risk patterns using a synthetic demonstration dataset.")
st.info("Demo only: this dataset is synthetic and the dashboard is for learning and exploratory analysis, not for making real lending decisions.")

@st.cache_data
def load_csv(file_bytes=None):
    if file_bytes is not None:
        from io import BytesIO
        return pd.read_csv(BytesIO(file_bytes))
    return pd.read_csv(DEFAULT_DATA)

with st.sidebar:
    st.header("Data & filters")
    uploaded = st.file_uploader("Upload a CSV (optional)", type=["csv"])
    try:
        df = load_csv(uploaded.getvalue() if uploaded else None)
    except Exception as e:
        st.error(f"Could not read the CSV: {e}")
        st.stop()

    required = {"applicant_id", "age", "annual_income", "loan_amount", "credit_score", "employment_type", "loan_purpose", "loan_status"}
    missing = required - set(df.columns)
    if missing:
        st.error("CSV is missing required columns: " + ", ".join(sorted(missing)))
        st.stop()

    status_values = sorted(df["loan_status"].dropna().astype(str).unique().tolist())
    purpose_values = sorted(df["loan_purpose"].dropna().astype(str).unique().tolist())
    employment_values = sorted(df["employment_type"].dropna().astype(str).unique().tolist())
    selected_status = st.multiselect("Loan status", status_values, default=status_values)
    selected_purpose = st.multiselect("Loan purpose", purpose_values, default=purpose_values)
    selected_employment = st.multiselect("Employment type", employment_values, default=employment_values)
    score_range = st.slider("Credit score range", 300, 850, (300, 850))

filtered = df[
    df["loan_status"].astype(str).isin(selected_status)
    & df["loan_purpose"].astype(str).isin(selected_purpose)
    & df["employment_type"].astype(str).isin(selected_employment)
    & df["credit_score"].between(score_range[0], score_range[1])
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

total_apps = len(filtered)
approval_rate = (filtered["loan_status"].eq("Approved").mean() * 100) if total_apps else 0
avg_income = filtered["annual_income"].mean()
avg_loan = filtered["loan_amount"].mean()
avg_score = filtered["credit_score"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Applications", f"{total_apps:,}")
c2.metric("Approval share", f"{approval_rate:.1f}%")
c3.metric("Average annual income", f"₹{avg_income:,.0f}")
c4.metric("Average credit score", f"{avg_score:.0f}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Applications by loan status")
    status_counts = filtered["loan_status"].value_counts().rename_axis("Status").reset_index(name="Applications")
    st.plotly_chart(px.bar(status_counts, x="Status", y="Applications", color="Status", title="Status distribution"), use_container_width=True)
with right:
    st.subheader("Loan purpose breakdown")
    purpose_counts = filtered.groupby("loan_purpose", as_index=False)["loan_amount"].sum().sort_values("loan_amount", ascending=False)
    st.plotly_chart(px.bar(purpose_counts, x="loan_purpose", y="loan_amount", title="Total loan amount by purpose", labels={"loan_purpose":"Loan purpose", "loan_amount":"Total loan amount (₹)"}), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Income vs. loan amount")
    st.plotly_chart(px.scatter(filtered, x="annual_income", y="loan_amount", color="loan_status", hover_data=["applicant_id", "credit_score", "loan_purpose"], labels={"annual_income":"Annual income (₹)", "loan_amount":"Loan amount (₹)"}, title="Applicant income and requested loan"), use_container_width=True)
with right:
    st.subheader("Credit score distribution")
    st.plotly_chart(px.histogram(filtered, x="credit_score", color="loan_status", nbins=20, title="Credit score by loan status"), use_container_width=True)

st.subheader("Summary by employment type")
summary = filtered.groupby("employment_type", as_index=False).agg(
    applicants=("applicant_id", "count"),
    average_income=("annual_income", "mean"),
    average_loan=("loan_amount", "mean"),
    average_credit_score=("credit_score", "mean"),
    approval_share=("loan_status", lambda s: (s == "Approved").mean() * 100)
).round(1)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("Filtered records")
st.caption("Applicant IDs are synthetic. Avoid uploading real personal or financial data to a public repository.")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered data as CSV", data=csv_bytes, file_name="filtered_loan_credit_data.csv", mime="text/csv")

st.subheader("Data quality checks")
quality = pd.DataFrame({
    "Check": ["Rows", "Duplicate applicant IDs", "Missing values (all columns)", "Credit scores outside 300–850"],
    "Result": [len(df), int(df["applicant_id"].duplicated().sum()), int(df.isna().sum().sum()), int((~df["credit_score"].between(300, 850)).sum())]
})
st.dataframe(quality, use_container_width=True, hide_index=True)
