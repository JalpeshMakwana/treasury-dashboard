import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Treasury Dashboard", layout="wide")

ADDRESS = "0x5ad05c158151248064a9db38624000ddba0eb6a1"

# Railway / Streamlit Secrets
API_KEY = st.secrets["ETHERSCAN_API_KEY"]

st.title("🚀 Treasury Dashboard (Live)")

# -----------------------------
# FETCH DATA
# -----------------------------
url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={ADDRESS}&page=1&offset=100&sort=desc&apikey={API_KEY}"

response = requests.get(url).json()

txs = response.get("result", [])

df = pd.DataFrame(txs)

# -----------------------------
# DASHBOARD UI
# -----------------------------
if not df.empty:

    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", len(df))
    col2.metric("Unique Tokens", df["tokenSymbol"].nunique())
    col3.metric("Wallet", ADDRESS[:10] + "...")

    st.divider()

    st.subheader("📋 Latest ERC20 Transfers")

    st.dataframe(
        df[[
            "tokenSymbol",
            "from",
            "to",
            "value",
            "timeStamp"
        ]],
        use_container_width=True
    )

    st.subheader("📊 Token Activity Chart")

    chart = px.histogram(
        df,
        x="tokenSymbol",
        title="Token Distribution"
    )

    st.plotly_chart(chart, use_container_width=True)

else:
    st.warning("No data found from Etherscan API")
