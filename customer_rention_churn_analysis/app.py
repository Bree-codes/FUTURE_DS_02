import streamlit as st
import plotly.express as px
from churn_analysis import *

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("📊 Customer Churn Analysis Dashboard")

# Load data
df = load_data("/home/bree/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.xls")
df = add_features(df)

# KPIs
total, churn, tenure, monthly = kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total)
col2.metric("Churn Rate (%)", f"{churn:.2f}")
col3.metric("Avg Tenure (months)", f"{tenure:.1f}")
col4.metric("Avg Monthly Charges", f"${monthly:.2f}")

st.markdown("---")

# Churn by Contract
st.subheader("Churn by Contract Type")
contract_df = churn_by_contract(df)
fig1 = px.bar(contract_df, x="Contract", y="ChurnFlag", color="Contract")
st.plotly_chart(fig1, use_container_width=True)

# Churn by Tenure
st.subheader("Churn by Tenure Group")
tenure_df = churn_by_tenure(df)
fig2 = px.bar(tenure_df, x="TenureGroup", y="ChurnFlag", color="TenureGroup")
st.plotly_chart(fig2, use_container_width=True)

# Payment Method
st.subheader("Churn by Payment Method")
payment_df = churn_by_payment(df)
fig3 = px.bar(payment_df, x="PaymentMethod", y="ChurnFlag", color="PaymentMethod")
st.plotly_chart(fig3, use_container_width=True)

# Raw data
with st.expander("View Raw Data"):
    st.dataframe(df)

# Filters
st.sidebar.header("Filters")

contract_filter = st.sidebar.multiselect(
    "Select Contract Type",
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)

df = df[df['Contract'].isin(contract_filter)]

# Insights
st.markdown("## 🔍 Key Insights")

st.write("""
- Customers on month-to-month contracts show significantly higher churn.
- Early-stage customers (0–6 months) are most likely to leave.
- Certain payment methods correlate with higher churn rates.
""")

# Recommendations
st.markdown("## 💡 Recommendations")

st.write("""
- Encourage long-term contracts with discounts.
- Improve onboarding experience for new users.
- Incentivize automatic payment methods.
""")