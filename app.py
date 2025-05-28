# IMPORTS SECTION
# Core libraries for the Streamlit web application
import streamlit as st
from db import get_filtered_data  # Database connection and data retrieval functions
from charts import plot_strategy_heatmap  # Visualization functions
from query_logic import run_query  # Business intelligence query execution
from insert_data import insert_into_table  # Data insertion functionality
import pandas as pd  # Data manipulation and analysis

# STREAMLIT CONFIGURATION
# Set page layout to wide mode for better use of screen real estate
st.set_page_config(layout="wide")

# SESSION STATE MANAGEMENT
# Initialize session state for navigation between home page and main application
# This allows users to navigate back and forth between the welcome screen and dashboard
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    """
    Navigation helper function to return to the home page.
    Updates session state to trigger page re-render.
    """
    st.session_state.page = "home"

# HOME PAGE SECTION
# Welcome screen that introduces users to the application
if st.session_state.page == "home":
    st.title("🦈 Shark Tank Insights Explorer")
    st.markdown("""
    Welcome to the **Shark Tank Insights Explorer** — an interactive application built to explore and manage data from the Shark Tank universe.

    This database helps you:
    - Analyze trends in investments, industries, and shark behavior
    - Visualize investment strategy patterns
    - Insert new data entries like companies, entrepreneurs, or episodes
    - Share underlying Shark-Tank data used to build the GUI

    Use the navigation tabs to explore or manage data.
    """)

    # Entry button to access the main application
    if st.button("🚀 Enter App"):
        st.session_state.page = "main"
    st.stop()  # Prevent execution of main app code when on home page

# MAIN APPLICATION SECTION
# Core dashboard with all functionality organized in tabs
if st.session_state.page == "main":
    # Navigation back to home page
    if st.button("🔙 Back to Home"):
        go_home()
    
    st.title("Shark Tank Dashboard 🦈")
    st.markdown("""
    Use the **tabs below** to explore insights or add new data to the Shark Tank database.
    """)

    # GLOBAL POSSIBLE VALUES SECTION
    # These values are available across all tabs and affect data display
    st.sidebar.header("Possible Values")
    
    # Show possible values for database queries
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

    # Organize possible values into dictionary for easy passing to functions
    filters = {
        "industry": industry,
        "shark": shark,
        "season": season,
        "city": city,
        "state": state,
        "guest": guest_status
    }

    # TAB ORGANIZATION
    # Main application functionality is organized into 4 distinct tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Query Explorer", "📈 Investment Strategy", "➕ Insert Data", "📂 Browse Raw Data"])

    # TAB 1: QUERY EXPLORER
    # Business intelligence and analytical queries
    with tab1:
        st.subheader("Explore the Data")

        # PREDEFINED QUERY LIST
        # 13 pre-built analytical queries for business insights
        query_list = [
            "1. Industries with Most Appearances and Deal Rates",
            "2. Average & Range of Asks per Industry",
            "3. Valuation trends across seasons",
            "4. Shark collaboration patterns",
            "5. Top sharks by deal frequency & total investment",
            "6. Shark deal rate",
            "7. Effect of guest shark presence on deals",
            "8. Impact of pitch order on success",
            "9. Companies from a given city/state and their deal stats",
            "10. Companies by industry and their deal stats",
            "11. Companies with highest total amount invested",
            "12. Episodes with highest accepted deal count",
            "13. Average investment stats per season",
        ]

        # QUERY DESCRIPTIONS
        # Business context for each analytical query
        query_descriptions = {
            "1. Industries with Most Appearances and Deal Rates": "Industries ranked by how often they appear and how frequently they get deals.",
            "2. Average & Range of Asks per Industry": "Shows min, max, and average asks amounts and equity across industries.",
            "3. Valuation trends across seasons": "Traces average valuation trends of industries across seasons.",
            "4. Shark collaboration patterns": "Visualizes which sharks tend to invest together.",
            "5. Top sharks by deal frequency & total investment": "Ranks sharks by deal count and total amount invested.",
            "6. Shark deal rate": "Shows the number of asks and successful deals by each shark.",
            "7. Effect of guest shark presence on deals": "Analyzes if guest sharks affect deal frequency.",
            "8. Impact of pitch order on success": "Explores whether pitch order affects success rate. Lower number means an earlier slot.",
            "9. Companies from a given city/state and their deal stats": "Analyze geographic patterns in Shark Tank success rates.",
            "10. Companies by industry and their deal stats": "Compares company success across industries.",
            "11. Companies with highest total amount invested": "Shows companies that received the largest investments.",
            "12. Episodes with highest accepted deal count": "Ranks episodes by number of accepted deals.",
            "13. Average investment stats per season": "Tracks the number, total, and average of investments made per season.",
        }

        # Display available queries to user
        st.markdown("**Available Queries:**")
        for q in query_list:
            st.markdown(f"- {q}")

        st.markdown("---")
        
        # QUERY SELECTION AND EXECUTION
        selected_query = st.selectbox("Choose a query to run:", query_list)
        user_input = None  # Reserved for future user input functionality

        # FILTER CRITERIA MAPPING
        # Maps each query to its primary filter dimension for result filtering
        filter_criteria = {
            "1. Industries with Most Appearances and Deal Rates": "Industry Name",
            "2. Average & Range of Asks per Industry": "Industry Name", 
            "3. Valuation trends across seasons": "Season ID",
            "4. Shark collaboration patterns": "Shark 1",
            "5. Top sharks by deal frequency & total investment": "Shark Name",
            "6. Shark deal rate": "Shark Name",
            "7. Effect of guest shark presence on deals": "Has Guest",
            "8. Impact of pitch order on success": "Pitch Order",
            "9. Companies from a given city/state and their deal stats": "City",
            "10. Companies by industry and their deal stats": "Industry",
            "11. Companies with highest total amount invested": "Company Name",
            "12. Episodes with highest accepted deal count": "Season ID",
            "13. Average investment stats per season": "Season ID"
        }

        # SESSION STATE FOR QUERY RESULTS
        # Maintain query results across user interactions for filtering and export
        if "query_results" not in st.session_state:
            st.session_state.query_results = None
        if "last_query" not in st.session_state:
            st.session_state.last_query = None

        # QUERY EXECUTION
        if st.button("Run Query"):
            df = run_query(selected_query, user_input)
            st.session_state.query_results = df
            st.session_state.last_query = selected_query

        # RESULTS DISPLAY AND FILTERING SECTION
        if st.session_state.query_results is not None and not st.session_state.query_results.empty:
            df = st.session_state.query_results.copy()
            
            # Display query description for context
            description = query_descriptions.get(st.session_state.last_query)
            if description:
                st.markdown(f"**Query Summary:** {description}")

            # DYNAMIC RESULT FILTERING
            # Add filter dropdown based on the query type
            filter_type = filter_criteria.get(st.session_state.last_query)
            if filter_type:
                st.markdown("---")
                st.markdown(f"### 🔍 Filter Results by {filter_type}")
                
                # COLUMN MAPPING LOGIC
                # Map filter types to actual DataFrame column names
                filter_column = None
                filter_options = ["All"]
                
                # Industry-related filters
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
                
                # Numeric filters
                elif filter_type == "Season ID":
                    if "season_id" in df.columns:
                        filter_column = "season_id"
                
                # Shark-related filters
                elif filter_type == "Shark Name":
                    if "shark_name" in df.columns:
                        filter_column = "shark_name"
                elif filter_type == "Shark 1":
                    if "Shark1" in df.columns:
                        filter_column = "Shark1"
                
                # Boolean and other filters
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
                
                # FILTER APPLICATION
                if filter_column and filter_column in df.columns:
                    unique_values = sorted(df[filter_column].unique())
                    filter_options.extend([str(val) for val in unique_values])
                    
                    selected_filter = st.selectbox(f"Filter by {filter_type}:", filter_options)
                    
                    # Apply filter if not "All"
                    if selected_filter != "All":
                        if filter_type in ["Season ID", "Pitch Order"]:
                            # Numeric filters require integer conversion
                            df = df[df[filter_column] == int(selected_filter)]
                        else:
                            # String filters use direct comparison
                            df = df[df[filter_column] == selected_filter]
                    
                    # Handle empty results
                    if df.empty:
                        st.warning(f"No results found for {filter_type}: {selected_filter}")
                        df = st.session_state.query_results.copy()  # Reset to original data

            # DATA FORMATTING FOR DISPLAY
            # Format numeric columns for better readability
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
            
            # RESULTS DISPLAY AND EXPORT
            st.dataframe(df)  # Interactive data table
            st.download_button("Export CSV", df.to_csv(index=False), "results.csv")  # CSV export functionality
            
        elif st.session_state.query_results is not None:
            st.warning("No results found.")

    # TAB 2: INVESTMENT STRATEGY VISUALIZATIONS
    # Interactive charts and graphs for visual analysis
    with tab2:
        st.subheader("📈 Investment Strategy Visuals")
        
        # STRATEGY HEATMAP SECTION
        st.markdown("### 🔎 Strategy Overview")
        strategy_df = get_filtered_data("strategy", filters)
        if not strategy_df.empty:
            st.plotly_chart(plot_strategy_heatmap(strategy_df), use_container_width=True)
        else:
            st.warning("No investment strategy data found.")



    # TAB 3: DATA INSERTION
    # Forms for adding new records to the database
    with tab3:
        st.subheader("Insert Data into Tables")

        st.markdown("---")
        
        # DATA ENTRY GUIDANCE
        # Help users understand foreign key dependencies and proper insertion order
        st.markdown("### 💡 Tips for Data Entry")
        st.markdown("""
        - **Required fields** are marked with an asterisk (*)
        - **Foreign Key Dependencies**: Make sure referenced records exist first:
        - Companies need Industries to exist first
        - Episodes need Seasons to exist first  
        - Asks need Episodes, Seasons, and Companies to exist first
        - Investments need Episodes, Seasons, and Companies to exist first
        - Contributions need Investments and Sharks to exist first
        - Ownership needs Companies and Entrepreneurs to exist first
        - Judge assignments need Episodes, Seasons, and Sharks to exist first
        - **Recommended insertion order**: Industry → Season → Shark → Entrepreneur → Episode → Company → Own → Ask → Investment → Contribute → Judge
        """)

        # TABLE SELECTION FOR DATA INSERTION
        tables = [
            "Ask", "Company", "Contribute", "Entrepreneur", "Episode", "Industry",  
            "Investment", "Judge", "Own", "Season", "Shark"
        ]
        selected_table = st.selectbox("Select a table to insert into:", tables)
        
        # Call the insertion function from insert_data.py
        insert_into_table(selected_table)

    # TAB 4: RAW DATA BROWSING
    # View and export complete table contents
    with tab4:
        st.subheader("📁 Browse Raw Data")

        # TABLE SELECTION FOR BROWSING
        table_options = [
            "Company", "Investment", "Industry", "Entrepreneur",
            "Episode", "Season", "Shark", "Ask", "Contribute", "Own", "Judge"
        ]
        selected_table = st.selectbox("Select a table to view:", table_options)

        # DATA RETRIEVAL AND DISPLAY
        if selected_table:
            df = get_filtered_data("raw_table", {"table": selected_table})
            df = pd.DataFrame(df)
            if not df.empty:
                st.dataframe(df)  # Interactive data table
                # CSV export with descriptive filename
                st.download_button("Download CSV", df.to_csv(index=False), f"{selected_table.lower()}_data.csv")
            else:
                st.info("No data found in selected table.")

