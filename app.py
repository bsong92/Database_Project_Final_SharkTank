import streamlit as st
from db import get_filtered_data
from charts import plot_valuation_chart, plot_network_graph, plot_strategy_heatmap
from query_logic import run_query
from insert_data import insert_into_table
import pandas as pd

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
    st.sidebar.header("Possible Values")
    industry_data = get_filtered_data("industry") or []
    industry = st.sidebar.selectbox("Industry", options=["All"] + industry_data)
    season_data = get_filtered_data("season") or []
    season = st.sidebar.selectbox("Season", options=["All"] + season_data)
    city_data = get_filtered_data("city") or []
    city = st.sidebar.selectbox("City", options=["All"] + city_data)
    state_data = get_filtered_data("state") or []
    state = st.sidebar.selectbox("State", options=["All"] + state_data)
    shark_data = get_filtered_data("shark") or []
    shark = st.sidebar.selectbox("Shark", options=["All"] + shark_data)
    guest_status = st.sidebar.selectbox("Guest Status", options=["All", "Guest", "Main Shark"])

    filters = {
        "industry": industry,
        "shark": shark,
        "season": season,
        "city": city,
        "state": state,
        "guest": guest_status
    }

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Query Explorer", "📈 Strategy & Networking", "➕ Insert Data", "📂 Browse Raw Data"])

    with tab1:
        st.subheader("Explore the Data")

        # Add query list and description mapping
        query_list = [
            "1. Industries with Most Appearances and Deal Rates",
            "2. Average & Range of Offers per Industry",
            "3. Valuation trends across seasons",
            "4. Shark collaboration patterns",
            "5. Top sharks by deal frequency & total investment",
            "6. Shark deal rate",
            "7. Effect of guest shark presence on deals",
            "8. Impact of pitch order on success",
            "9. Entrepreneurs from a given city/state and their deal stats",
            "10. Entrepreneurs by industry and their deal stats",
            "11. Companies with highest total amount offered",
            "12. Episodes with highest accepted deal count",
            "13. Average investment stats per season",
        ]

        # 🔹 Add description dictionary
        query_descriptions = {
            "1. Industries with Most Appearances and Deal Rates": "Industries ranked by how often they appear and how frequently they get deals.",
            "2. Average & Range of Offers per Industry": "Shows min, max, and average offer amounts and equity across industries.",
            "3. Valuation trends across seasons": "Traces average valuation trends of industries across seasons.",
            "4. Shark collaboration patterns": "Visualizes which sharks tend to invest together.",
            "5. Top sharks by deal frequency & total investment": "Ranks sharks by deal count and total amount invested.",
            "6. Shark deal rate": "Shows the number of asks and successful deals by each shark.",
            "7. Effect of guest shark presence on deals": "Analyzes if guest sharks affect deal frequency.",
            "8. Impact of pitch order on success": "Explores whether pitch order affects success rate. Lower number means an earlier slot.",
            "9. Entrepreneurs from a given city/state and their deal stats": "Analyze geographic patterns in Shark Tank success rates.",
            "10. Entrepreneurs by industry and their deal stats": "Compares entrepreneur success across industries.",
            "11. Companies with highest total amount offered": "Shows companies that received the largest offers.",
            "12. Episodes with highest accepted deal count": "Ranks episodes by number of accepted deals.",
            "13. Average investment stats per season": "Tracks the number, total, and average of investments made per season.",
        }

        st.markdown("**Available Queries:**")
        for q in query_list:
            st.markdown(f"- {q}")

        st.markdown("---")
        
        # 🔹 Select and run query
        selected_query = st.selectbox("Choose a query to run:", query_list)
        user_input = None

        # Define filter criteria for each query
        filter_criteria = {
            "1. Industries with Most Appearances and Deal Rates": "Industry Name",
            "2. Average & Range of Offers per Industry": "Industry Name", 
            "3. Valuation trends across seasons": "Season ID",
            "4. Shark collaboration patterns": "Shark 1",
            "5. Top sharks by deal frequency & total investment": "Shark Name",
            "6. Shark deal rate": "Shark Name",
            "7. Effect of guest shark presence on deals": "Has Guest",
            "8. Impact of pitch order on success": "Pitch Order",
            "9. Entrepreneurs from a given city/state and their deal stats": "City",
            "10. Entrepreneurs by industry and their deal stats": "Industry",
            "11. Companies with highest total amount offered": "Company Name",
            "12. Episodes with highest accepted deal count": "Season ID",
            "13. Average investment stats per season": "Season ID"
        }

        # Initialize session state for storing query results
        if "query_results" not in st.session_state:
            st.session_state.query_results = None
        if "last_query" not in st.session_state:
            st.session_state.last_query = None

        if st.button("Run Query"):
            df = run_query(selected_query, user_input)
            st.session_state.query_results = df
            st.session_state.last_query = selected_query

        # Show results and filtering options if we have data
        if st.session_state.query_results is not None and not st.session_state.query_results.empty:
            df = st.session_state.query_results.copy()
            
            # 🔹 Show query description before results
            description = query_descriptions.get(st.session_state.last_query)
            if description:
                st.markdown(f"**Query Summary:** {description}")

            # Add filter dropdown based on the query type
            filter_type = filter_criteria.get(st.session_state.last_query)
            if filter_type:
                st.markdown("---")
                st.markdown(f"### 🔍 Filter Results by {filter_type}")
                
                # Get unique values for the filter column
                filter_column = None
                filter_options = ["All"]
                
                if filter_type == "Industry Name":
                    if "industry_name" in df.columns:
                        filter_column = "industry_name"
                    elif "industry" in df.columns:
                        filter_column = "industry"
                elif filter_type == "Industry":
                    if "industry" in df.columns:
                        filter_column = "industry"
                    elif "industry_name" in df.columns:
                        filter_column = "industry_name"
                elif filter_type == "Season ID":
                    if "season_id" in df.columns:
                        filter_column = "season_id"
                elif filter_type == "Shark Name":
                    if "shark_name" in df.columns:
                        filter_column = "shark_name"
                elif filter_type == "Shark 1":
                    if "Shark1" in df.columns:
                        filter_column = "Shark1"
                elif filter_type == "Has Guest":
                    if "has_guest" in df.columns:
                        filter_column = "has_guest"
                elif filter_type == "Pitch Order":
                    if "pitch_order" in df.columns:
                        filter_column = "pitch_order"
                elif filter_type == "City":
                    if "city" in df.columns:
                        filter_column = "city"
                elif filter_type == "Company Name":
                    if "company_name" in df.columns:
                        filter_column = "company_name"
                
                if filter_column and filter_column in df.columns:
                    unique_values = sorted(df[filter_column].unique())
                    filter_options.extend([str(val) for val in unique_values])
                    
                    selected_filter = st.selectbox(f"Filter by {filter_type}:", filter_options)
                    
                    # Apply filter if not "All"
                    if selected_filter != "All":
                        if filter_type in ["Season ID", "Pitch Order"]:
                            # For numeric filters
                            df = df[df[filter_column] == int(selected_filter)]
                        else:
                            # For string filters
                            df = df[df[filter_column] == selected_filter]
                    
                    if df.empty:
                        st.warning(f"No results found for {filter_type}: {selected_filter}")
                        df = st.session_state.query_results.copy()  # Reset to original data

            # Format numeric columns for display
            if "average_amount_raised" in df.columns:
                df["average_amount_raised"] = df["average_amount_raised"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")  
            if "total_offered" in df.columns:
                df["total_offered"] = df["total_offered"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")
            if "avg_deal_rate" in df.columns:
                df["avg_deal_rate"] = df["avg_deal_rate"].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
            if "avg_investment" in df.columns:
                df["avg_investment"] = df["avg_investment"].apply(lambda x: f"${int(x):,}" if pd.notna(x) else "")
            if "total_invested" in df.columns:
                df["total_invested"] = df["total_invested"].apply(lambda x: f"${int(x):,}" if pd.notna(x) else "")    
            
            st.dataframe(df)
            st.download_button("Export CSV", df.to_csv(index=False), "results.csv")
        elif st.session_state.query_results is not None:
            st.warning("No results found.")

    with tab2:
        st.subheader("📈 Strategy and 🔗 Networking Visuals")
        
        st.markdown("### 🔎 Strategy Overview")
        strategy_df = get_filtered_data("strategy", filters)
        if not strategy_df.empty:
            st.plotly_chart(plot_strategy_heatmap(strategy_df), use_container_width=True)
        else:
            st.warning("No investment strategy data found.")

        # st.info("This section will show strategy visuals by shark, episode, and industry.")

        # st.markdown("### 🔗 Shark Co-Investment Network")
        # net_df = get_filtered_data("network", filters)
        # st.plotly_chart(plot_network_graph(net_df))

        # st.markdown("### 💰 Top 10 Valuations by Company")
        # valuation_df = get_filtered_data("valuation", filters)
        # if not valuation_df.empty:
        #     st.plotly_chart(plot_valuation_chart(valuation_df), use_container_width=True)
        # else:
        #     st.warning("No valuation data available.")

    with tab3:
        st.subheader("Insert Data into Tables")

        st.markdown("Entities should be inserted before relationships.")

        tables = [
            "Ask", "Company", "Contribute", "Entrepreneur", "Episode", "Industry",  
            "Investment", "Judge", "Own", "Season", "Shark"
        ]
        selected_table = st.selectbox("Select a table to insert into:", tables)
        insert_into_table(selected_table)

    with tab4:
        st.subheader("📁 Browse Raw Data")

        # List of all core tables
        table_options = [
            "Company", "Investment", "Industry", "Entrepreneur",
            "Episode", "Season", "Shark", "Ask", "Contribute", "Own", "Judge"
        ]
        selected_table = st.selectbox("Select a table to view:", table_options)

        if selected_table:
            df = get_filtered_data("raw_table", {"table": selected_table})
            df = pd.DataFrame(df)
            if not df.empty:
                st.dataframe(df)
                st.download_button("Download CSV", df.to_csv(index=False), f"{selected_table.lower()}_data.csv")
            else:
                st.info("No data found in selected table.")
    
    # with tab4:
    #     st.subheader("📂 Browse Raw Data")
    #     st.markdown("Select a table and use the global filters on the left to browse the data.")
        
    #     raw_tables = [
    #         "Company", "Entrepreneur", "Episode", "Industry", "Season", 
    #         "Shark", "Investment", "Ask", "Own", "Judge", "Contribute"
    #     ]
        
    #     selected_table = st.selectbox("Select a table to view:", raw_tables, key="raw_table_select")

    #     df = get_filtered_data(selected_table.lower(), filters)

    #     if df is not None and not df.empty:
    #         st.dataframe(df)
    #         st.download_button("Download CSV", df.to_csv(index=False), "raw_data.csv")
    #     else:
    #         st.info("No data found for selected table and filters.")
