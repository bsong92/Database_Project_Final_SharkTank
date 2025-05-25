# insert_data.py
import streamlit as st
from db import connect_db

def insert_into_table(table):
    conn = connect_db()
    cursor = conn.cursor()

    if table == "Industry":
        industry_name = st.text_input("Industry Name")
        market_size = st.text_input("Market Size")
        growth_rate = st.text_input("Growth Rate")
        if st.button("Insert Industry"):
            cursor.execute("INSERT INTO Industry VALUES (%s, %s, %s)", (industry_name, market_size, growth_rate))
            conn.commit()
            st.success("Inserted into Industry")

    elif table == "Ask":
        episode_id = st.number_input("Episode ID", step=1)
        season_id = st.number_input("Season ID", step=1)
        company_id = st.number_input("Company ID", step=1)
        equity_amount = st.number_input("Equity Amount", step=1000)
        equity_share = st.number_input("Equity Share (%)", step=1)
        if st.button("Insert Ask"):
            cursor.execute(
                "INSERT INTO Ask (episode_id, season_id, company_id, equity_amount, equity_share) VALUES (%s, %s, %s, %s, %s)",
                (episode_id, season_id, company_id, equity_amount, equity_share))
            conn.commit()
            st.success("Inserted into Ask")

    elif table == "Investment":
        investment_id = st.number_input("Investment ID", step=1)
        episode_id = st.number_input("Episode ID", step=1)
        season_id = st.number_input("Season ID", step=1)
        company_id = st.number_input("Company ID", step=1)
        equity_amount = st.number_input("Equity Amount", step=1000)
        equity_share = st.number_input("Equity Share (%)", step=1)
        loan = st.number_input("Loan", step=1000)
        advisory_shares_equity = st.number_input("Advisory Shares Equity", step=0.1)
        has_conditions = st.checkbox("Has Conditions")
        involve_royalty = st.checkbox("Involve Royalty")
        if st.button("Insert Investment"):
            cursor.execute(
                "INSERT INTO Investment VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (investment_id, episode_id, season_id, company_id, equity_amount, equity_share,
                 loan, advisory_shares_equity, has_conditions, involve_royalty))
            conn.commit()
            st.success("Inserted into Investment")

    elif table == "Contribute":
        investment_id = st.number_input("Investment ID", step=1)
        shark_id = st.number_input("Shark ID", step=1)
        equity_amount = st.number_input("Equity Amount", step=1000)
        equity_share = st.number_input("Equity Share (%)", step=1)
        if st.button("Insert Contribute"):
            cursor.execute(
                "INSERT INTO Contribute VALUES (%s, %s, %s, %s)",
                (investment_id, shark_id, equity_amount, equity_share))
            conn.commit()
            st.success("Inserted into Contribute")

# elif table == "Pitch":
    #     ep = st.text_input("Episode ID")
    #     company = st.text_input("Company Name")
    #     if st.button("Insert Pitch"):
    #         cursor.execute("INSERT INTO Pitch VALUES (%s, %s)", (ep, company))
    #         conn.commit()
    #         st.success("Inserted into Pitch")

    # elif table == "Offer":
    #     season = st.text_input("Season ID")
    #     ep = st.text_input("Episode ID")
    #     company = st.text_input("Company Name")
    #     amount = st.number_input("Amount", min_value=0.0)
    #     equity = st.number_input("Equity", min_value=0.0)
    #     if st.button("Insert Offer"):
    #         cursor.execute("INSERT INTO Offer VALUES (%s, %s, %s, %s, %s)", (season, ep, company, amount, equity))
    #         conn.commit()
    #         st.success("Inserted into Offer")

    # elif table == "Deal":
    #     season = st.text_input("Season ID")
    #     ep = st.text_input("Episode ID")
    #     company = st.text_input("Company Name")
    #     amount = st.number_input("Total Amount", min_value=0.0)
    #     equity = st.number_input("Total Equity", min_value=0.0)
    #     shark = st.text_input("Shark Name")
    #     royalty = st.selectbox("Royalty Component?", ["True", "False"])
    #     accepted = st.selectbox("Was Accepted?", ["True", "False"])
    #     if st.button("Insert Deal"):
    #         cursor.execute("INSERT INTO Deal VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (season, ep, company, amount, equity, shark, royalty == "True", accepted == "True"))
    #         conn.commit()
    #         st.success("Inserted into Deal")

    conn.close()
