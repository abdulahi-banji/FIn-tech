"""Session-one Money Brain dashboard, using only fictional data."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Money Brain", page_icon="💸", layout="wide")
data = json.loads((Path(__file__).parent / "data" / "demo.json").read_text())
transactions = pd.DataFrame(data["transactions"])
transactions["date"] = pd.to_datetime(transactions["date"])
dashboard, controls = st.columns([4, 1], gap="large")

with controls:
    st.header("Explore spending")
    months = sorted(transactions["date"].dt.strftime("%Y-%m").unique(), reverse=True)
    month = st.selectbox("Month", months, key="month")
    categories = st.multiselect(
        "Categories (empty means all)", sorted(transactions["category"].unique())
    )
    threshold = st.number_input("Large purchase alert ($)", min_value=1, value=250)

monthly = transactions[transactions["date"].dt.strftime("%Y-%m") == month]
visible = monthly[monthly["category"].isin(categories)] if categories else monthly
with dashboard:
    st.title("Your money, in one place")
    st.caption("Money Brain · Fintech Club · Fictional demo data")
    st.info("Session-one prototype. Bank connections and AI arrive in later sessions.")

    st.subheader("Accounts")
    for column, account in zip(st.columns(len(data["accounts"])), data["accounts"]):
        column.metric(account["name"], f"${account['balance']:,.2f}")
    st.caption("Negative credit card balances represent money owed.")

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Spending")
        st.metric("Selected spending", f"${visible['amount'].sum():,.2f}")
        if visible.empty:
            st.info("No purchases match these filters.")
        else:
            st.bar_chart(visible.groupby("category")["amount"].sum())
        st.subheader("Transactions")
        table = visible.sort_values("date", ascending=False).copy()
        table["date"] = table["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(table, hide_index=True, width="stretch")

    with right:
        st.subheader("Purchase alerts")
        st.caption("Uses spending filters. Large purchases are not proof of fraud.")
        alerts = visible[visible["amount"] >= threshold]
        if alerts.empty:
            st.success("No purchases meet your alert threshold.")
        for row in alerts.itertuples():
            st.warning(f"{row.merchant}: ${row.amount:,.2f}")

        st.subheader("Ask about your money")
        st.caption("Calculated demo answers; AI is planned for November 6.")
        question = st.selectbox("Question", [
            "How much did I spend?",
            "What is my biggest spending category?",
            "What was my largest purchase?",
            "How much did I spend on dining?",
            "What is my total account balance?",
        ], key="question")
        st.caption("Spending answers use your filters. Balances use all demo accounts.")
        if question == "What is my total account balance?":
            total = sum(account["balance"] for account in data["accounts"])
            st.write(f"Your demo net account balance is ${total:,.2f}.")
        elif visible.empty:
            st.write("No purchases match your filters.")
        elif question == "How much did I spend?":
            st.write(f"You spent ${visible['amount'].sum():,.2f}.")
        elif question == "What is my biggest spending category?":
            totals = visible.groupby("category")["amount"].sum()
            st.write(f"{totals.idxmax()} leads at ${totals.max():,.2f}.")
        elif question == "What was my largest purchase?":
            largest = visible.loc[visible["amount"].idxmax()]
            st.write(f"{largest['merchant']}: ${largest['amount']:,.2f}.")
        else:
            dining = visible.loc[visible["category"] == "Dining", "amount"].sum()
            st.write(f"You spent ${dining:,.2f} on dining.")
