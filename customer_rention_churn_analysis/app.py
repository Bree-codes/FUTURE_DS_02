import streamlit as st
import plotly.express as px
from churn_analysis import *

# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")
st.title("📊 Customer Churn Analysis Dashboard")

# ------------------------
# Load & Preprocess Data
# ------------------------
df = load_data("customer_rention_churn_analysis/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df = add_features(df)

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filters")

# Contract filter
contract_filter = st.sidebar.multiselect(
    "Select Contract Type",
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)

# Payment Method filter
payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=df['PaymentMethod'].unique(),
    default=df['PaymentMethod'].unique()
)

# Tenure slider
min_tenure, max_tenure = int(df['tenure'].min()), int(df['tenure'].max())
selected_tenure = st.sidebar.slider(
    "Select Tenure Range (months)",
    min_value=min_tenure,
    max_value=max_tenure,
    value=(min_tenure, max_tenure)
)

# Apply filters
filtered_df = df[
    (df['Contract'].isin(contract_filter)) &
    (df['PaymentMethod'].isin(payment_filter)) &
    (df['tenure'] >= selected_tenure[0]) &
    (df['tenure'] <= selected_tenure[1])
]

# ------------------------
# KPIs
# ------------------------
total, churn, tenure, monthly = kpis(filtered_df)

cols = st.columns(4)
kpis_list = [
    ("Total Customers", f"{total:,}", "#1f77b4"),
    ("Churn Rate (%)", f"{churn:.2f}%", "#d62728"),
    ("Avg Tenure (months)", f"{tenure:.1f}", "#ff7f0e"),
    ("Avg Monthly Charges", f"${monthly:.2f}", "#2ca02c")
]

for col, (label, value, color) in zip(cols, kpis_list):
    with col:
        st.markdown(f"""
        <div style="
            background-color:#181818;
            padding:2px;
            border-radius:10px;
            text-align:center;
            box-shadow: 3px 3px 8px #111;
            margin-bottom:10px;">
            <h4 style="margin:0">{label}</h4>
            <h2 style="color:{color}; margin:5px 0">{value}</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ------------------------
# Charts
# ------------------------
st.subheader("Churn by Contract Type")
contract_df = churn_by_contract(filtered_df)
fig1 = px.bar(contract_df, x="Contract", y="ChurnFlag", color="Contract")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Churn by Tenure Group")
tenure_df = churn_by_tenure(filtered_df)
fig2 = px.bar(tenure_df, x="TenureGroup", y="ChurnFlag", color="TenureGroup")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Churn by Payment Method")
payment_df = churn_by_payment(filtered_df)
fig3 = px.bar(payment_df, x="PaymentMethod", y="ChurnFlag", color="PaymentMethod")
st.plotly_chart(fig3, use_container_width=True)

# ------------------------
# Insights
# ------------------------
st.markdown("## Key Insights")
if not contract_df.empty and not tenure_df.empty and not payment_df.empty:

    highest_contract = contract_df.sort_values(by="ChurnFlag", ascending=False).iloc[0]
    highest_tenure = tenure_df.sort_values(by="ChurnFlag", ascending=False).iloc[0]
    highest_payment = payment_df.sort_values(by="ChurnFlag", ascending=False).iloc[0]

    st.write(f"""
- Customers on **{highest_contract['Contract']} contracts** have the highest churn rate.

- Customers in the **{highest_tenure['TenureGroup']} stage** are most likely to leave the service.

- Customers using **{highest_payment['PaymentMethod']}** tend to churn more than others.

N/B -> This suggests that **contract flexibility, early customer experience, and payment convenience** play a major role in customer retention.
""")
else:
    st.warning("Not enough data to generate insights.")

# ------------------------
# Recommendations
# ------------------------
st.markdown("## Recommendations")
st.write("""
- Encourage long-term contracts with discounts.
- Improve onboarding experience for new users.
- Incentivize automatic payment methods.
""")

# ------------------------
# Raw Data
# ------------------------
with st.expander("View Raw Data"):
    st.dataframe(filtered_df)