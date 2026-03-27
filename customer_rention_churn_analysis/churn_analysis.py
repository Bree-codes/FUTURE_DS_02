import pandas as pd

def load_data(path):
    df = pd.read_csv(path)

    # Fix TotalCharges
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Drop missing
    df.dropna(inplace=True)

    return df


def add_features(df):
    # Convert churn to numeric
    df['ChurnFlag'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # Tenure groups
    bins = [0, 6, 12, 24, 60, 100]
    labels = ['0-6m', '6-12m', '1-2y', '2-5y', '5y+']
    df['TenureGroup'] = pd.cut(df['tenure'], bins=bins, labels=labels)

    return df


def churn_rate(df):
    return df['ChurnFlag'].mean()


def churn_by_contract(df):
    return df.groupby('Contract')['ChurnFlag'].mean().reset_index()


def churn_by_tenure(df):
    return df.groupby('TenureGroup')['ChurnFlag'].mean().reset_index()


def churn_by_payment(df):
    return df.groupby('PaymentMethod')['ChurnFlag'].mean().reset_index()


def kpis(df):
    total_customers = len(df)
    churn = df['ChurnFlag'].mean() * 100
    avg_tenure = df['tenure'].mean()
    avg_monthly = df['MonthlyCharges'].mean()

    return total_customers, churn, avg_tenure, avg_monthly