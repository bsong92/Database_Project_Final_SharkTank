import streamlit as st
from db import get_filtered_data
from charts import plot_valuation_chart, plot_network_graph, plot_strategy_heatmap
from query_logic import run_query
from insert_data import insert_into_table

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("🦈 Shark Tank Insights Explorer")
    st.markdown("""
    Welcome to the **Shark Tank Insights Explorer** — an interactive application built to explore and manage data from the Shark Tank universe.

    This database helps you:
    - Analyze trends in investments, industries, and shark behavior
    - Visualize co-investment networks and strategic patterns
    - Insert new data entries like companies, entrepreneurs, or episodes

    Use the navigation tabs to explore or manage data.
    """)

    if st.button("🚀 Enter App"):
        st.session_state.page = "main"
    st.stop()

if st.session_state.page == "main":
    if st.button("🔙 Back to Home"):
        go_home()
    st.title("Shark Tank Dashboard 🦈")
    st.markdown("""
    Use the **tabs below** to explore insights or add new data to the Shark Tank database.
    """)

    # Global sidebar filters (visible to all tabs)
    st.sidebar.header("Global Filters")
    industry_data = get_filtered_data("industry") or []
    industry = st.sidebar.selectbox("Industry", options=["All"] + industry_data)
    season_data = get_filtered_data("season") or []
    season = st.sidebar.selectbox("Season", options=["All"] + season_data)
    city_data = get_filtered_data("city") or []
    city = st.sidebar.selectbox("City", options=["All"] + city_data)
    shark_data = get_filtered_data("shark") or []
    shark = st.sidebar.selectbox("Shark", options=["All"] + shark_data)
    guest_status = st.sidebar.selectbox("Guest Status", options=["All", "Guest", "Main Shark"])

    filters = {
        "industry": industry,
        "shark": shark,
        "season": season,
        "city": city,
        "guest": guest_status
    }

    tab1, tab2, tab3 = st.tabs(["📊 Query Explorer", "📈 Strategy & Networking", "➕ Insert Data"])

    with tab1:
        st.subheader("Explore the Data")

        query_list = [
            "1. Industries with most appearances and deal rates",
            "2. Avg & range of offers per industry",
            "3. Valuation trends across seasons",
            "4. Shark collaboration patterns",
            "5. Top sharks by deal frequency & total investment",
            "6. Shark deal rate by episode and industry",
            "7. Effect of guest shark presence on deals",
            "8. Impact of pitch order on success",
            "9. Entrepreneurs from a given city/state and their deal stats",
            "10. Entrepreneurs by industry and their deal stats",
            "11. Companies with highest total amount offered",
            "12. Episodes with highest accepted deal count"
        ]

        selected_query = st.selectbox("Choose a query to run:", query_list)
        user_input = None

        if "industry" in selected_query.lower():
            user_input = st.text_input("Enter Industry (optional):")
        elif "city" in selected_query.lower() or "state" in selected_query.lower():
            user_input = st.text_input("Enter City or State (optional):")

        if st.button("Run Query"):
            df = run_query(selected_query, user_input)
            if df is not None and not df.empty:
                st.dataframe(df)
                st.download_button("Export CSV", df.to_csv(index=False), "results.csv")
            else:
                st.warning("No results found.")

    with tab2:
        st.subheader("📈 Strategy and 🔗 Networking Visuals")
        st.markdown("### 🔎 Strategy Overview")
        strategy_df = get_filtered_data("strategy", filters)
        if not strategy_df.empty:
            st.plotly_chart(plot_strategy_heatmap(strategy_df), use_container_width=True)
        else:
            st.warning("No investment strategy data found.")

        st.info("This section will show strategy visuals by shark, episode, and industry.")

        st.markdown("### 🔗 Shark Co-Investment Network")
        net_df = get_filtered_data("network", filters)
        st.plotly_chart(plot_network_graph(net_df))

    with tab3:
        st.subheader("Insert Data into Tables")
        tables = [
            "Ask", "Company", "Contribute", "Entrepreneur", "Episode", "Industry",  
            "Investment", "Judge", "Own", "Season", "Shark"
        ]
        selected_table = st.selectbox("Select a table to insert into:", tables)
        insert_into_table(selected_table)