# QUERY LOGIC MODULE
# ==================
# This module contains the business intelligence engine for the Shark Tank Insights Explorer.
# It provides 13 pre-built analytical queries that answer key business questions about:
# - Investment patterns and trends
# - Shark behavior and collaboration
# - Industry performance and success rates
# - Geographic and temporal analysis
# - Deal structures and valuations
#
# Each query is extensively documented with:
# - Business purpose and context
# - Technical implementation details
# - SQL optimization strategies
# - Expected output format

import pandas as pd
from db import connect_db

def run_query(query_name, user_input=None):
    """
    Execute SQL queries based on the selected query name from the Streamlit interface.
    
    This function serves as the main query dispatcher, routing query requests to the appropriate
    SQL implementation. Each query is designed to answer specific business questions and
    provide actionable insights for different stakeholders.
    
    Args:
        query_name (str): The name of the query to execute (from predefined list)
        user_input (str, optional): User input for filtering certain queries (reserved for future use)
    
    Returns:
        pandas.DataFrame: Query results formatted for display and analysis
        
    Query Categories:
        - Industry Analysis (Queries 1-3, 10): Market trends and sector performance
        - Shark Behavior (Queries 4-7): Investment patterns and collaboration
        - Success Factors (Queries 8-9): Geographic and temporal influences
        - Performance Metrics (Queries 11-13): Financial and episode analysis
    """
    # DATABASE CONNECTION
    # Establish connection for query execution
    conn = connect_db()

    # QUERY ROUTING SECTION
    # Each query is implemented as a separate conditional block with comprehensive documentation
    
    if "Industries with Most Appearances and Deal Rates" in query_name:
        # QUERY 1: Industries with Most Appearances and Deal Rates
        # PURPOSE: Identify which industries are most represented and how often they land deals
        # BUSINESS LOGIC: Measures deal-making success by comparing appearance frequency vs. deal frequency
        # STAKEHOLDERS: Entrepreneurs (market assessment), Investors (sector analysis)
        # TECHNICAL APPROACH:
        # - COUNT(*) counts how many companies appear per industry
        # - SUM(CASE...) counts how many got a deal (investment_id not null)
        # - Calculates deal rate = deal_count / total_appearances
        # - Uses ROUND and CONCAT to present as percentage string
        # - GROUP BY industry for aggregation
        # - LEFT JOIN ensures all companies are counted, even without deals
        sql = """
            SELECT 
                C.industry_name,
                COUNT(*) AS Company_Count,
                SUM(CASE WHEN I.investment_id IS NOT NULL THEN 1 ELSE 0 END) AS Deal_Count,
                CONCAT(ROUND(SUM(CASE WHEN I.investment_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) * 100, 2), '%') AS Deal_Rate
            FROM Company C
            LEFT JOIN Investment I ON C.company_id = I.company_id
            GROUP BY C.industry_name
            ORDER BY company_count DESC;
        """

    elif "Average & Range of Asks per Industry" in query_name:
        # QUERY 2: Average & Range of Asks per Industry
        # PURPOSE: Summarize investment behavior by showing ask ranges and equity per industry
        # BUSINESS LOGIC: Provides insight into typical deal structures and how aggressive asks are
        # STAKEHOLDERS: Entrepreneurs (pricing strategy), Investors (market benchmarks)
        # TECHNICAL APPROACH:
        # - MIN, MAX, and AVG functions calculate range and average of equity_amount
        # - AVG equity_share converted to percentage
        # - FORMAT for rounding and thousands separators
        # - GROUP BY industry to aggregate metrics
        # - INNER JOIN Ask with Company to get industry context
        sql = """
        SELECT 
            C.industry_name,
            FORMAT(MIN(A.equity_amount), 0) AS Min_Amount,
            FORMAT(MAX(A.equity_amount), 0) AS Max_Amount,
            FORMAT(AVG(A.equity_amount), 0) AS Avg_Amount,
            CONCAT(FORMAT(AVG(A.equity_share), 2), '%') AS Avg_Equity
        FROM Ask A
        JOIN Company C ON A.company_id = C.company_id
        GROUP BY C.industry_name;
        """

    elif "Valuation trends across seasons" in query_name:
        # QUERY 3: Valuation trends across seasons
        # PURPOSE: Track how company valuations change over time by industry and season
        # BUSINESS LOGIC: Calculates implied valuations from investment deals to show market trends
        # STAKEHOLDERS: Market analysts, Investors (timing strategies)
        # TECHNICAL APPROACH:
        # - Calculates valuation using formula: (equity_amount / equity_share) * 100
        # - INNER JOINs to only include actual investments with valid equity shares
        # - WHERE clause filters out zero equity shares to avoid division errors
        # - GROUP BY season and industry for trend analysis
        # - ROUND function for readable decimal places
        # - ORDER BY season and valuation for chronological and value-based sorting
        sql = """
        SELECT 
            S.season_id, 
            C.industry_name,
            FORMAT(AVG(I.equity_amount / I.equity_share * 100), 2) AS avg_valuation
        FROM Investment I
        JOIN Company C ON I.company_id = C.company_id
        JOIN Season S ON I.season_id = S.season_id
        WHERE I.equity_share > 0
        GROUP BY S.season_id, C.industry_name
        ORDER BY S.season_id, AVG(I.equity_amount / I.equity_share * 100) DESC;
        """

    elif "Shark collaboration patterns" in query_name:
        # QUERY 4: Shark collaboration patterns
        # PURPOSE: Identify which sharks frequently invest together in deals
        # BUSINESS LOGIC: Reveals partnership preferences and strategic alliances between sharks
        # STAKEHOLDERS: Sharks (partnership strategies), Researchers (network analysis)
        # TECHNICAL APPROACH:
        # - Self-join on Contribute table to find pairs of sharks in same investment
        # - C1.shark_id < C2.shark_id prevents duplicate pairs (A,B) and (B,A)
        # - Multiple JOINs to get shark names for both partners
        # - COUNT(*) to quantify collaboration frequency
        # - Results show strongest partnerships first
        sql = """
        SELECT S1.shark_name AS Shark1, S2.shark_name AS Shark2, COUNT(*) AS Number_of_collaborations
        FROM Contribute C1
        JOIN Contribute C2 ON C1.investment_id = C2.investment_id AND C1.shark_id < C2.shark_id
        JOIN Shark S1 ON C1.shark_id = S1.shark_id
        JOIN Shark S2 ON C2.shark_id = S2.shark_id
        GROUP BY S1.shark_name, S2.shark_name
        ORDER BY Number_of_collaborations DESC
        """

    elif "Top sharks by deal frequency" in query_name:
        # QUERY 5: Top sharks by deal frequency and total investment
        # PURPOSE: Rank sharks by their investment activity and financial commitment
        # BUSINESS LOGIC: Identifies most active investors and their investment patterns
        # STAKEHOLDERS: Entrepreneurs (target identification), Media (shark profiles)
        # TECHNICAL APPROACH:
        # - INNER JOINs through Investment -> Contribute -> Shark to link investments to sharks
        # - COUNT(*) for total number of deals per shark
        # - MAX(I.equity_amount) for largest single investment per shark
        # - SUM(I.equity_amount) for total investment amount per shark
        # - FORMAT functions for readable currency display
        # - ORDER BY total_investment to rank by financial commitment
        sql = """
        SELECT S.shark_name,
            COUNT(*) AS total_deals,
            FORMAT(MAX(I.equity_amount), 0) AS max_single_investment,
            FORMAT(SUM(I.equity_amount), 0) AS total_investment
        FROM Investment I
        JOIN Contribute C ON I.investment_id = C.investment_id
        JOIN Shark S ON C.shark_id = S.shark_id
        GROUP BY S.shark_name
        ORDER BY SUM(I.equity_amount) DESC;
        """

    elif "Shark deal rate" in query_name:
        # QUERY 6: Shark deal rate by episode and industry
        # PURPOSE: Calculate each shark's success rate (deals made vs opportunities available)
        # BUSINESS LOGIC: Shows which sharks are most selective vs most active in making deals
        # STAKEHOLDERS: Entrepreneurs (pitch targeting), Sharks (performance analysis)
        # TECHNICAL APPROACH:
        # - Complex JOIN chain: Ask -> Episode -> Judge -> Shark to link asks to judging sharks
        # - LEFT JOIN to Investment to identify successful deals
        # - CASE WHEN with COUNT DISTINCT for conditional counting of successful deals
        # - NULLIF prevents division by zero in deal rate calculation
        # - HAVING clause filters out sharks with no judging opportunities
        # - Deal rate = successful_deals / total_asks_judged
        # - Results show most selective sharks first
        sql = """
        SELECT S.shark_name, 
               COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN A.company_id END) AS successful_deals,
               COUNT(DISTINCT A.company_id) AS total_asks,
               ROUND(
                   COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN A.company_id END) * 1.0 / 
                   NULLIF(COUNT(DISTINCT A.company_id), 0), 3
               ) AS deal_rate
        FROM Ask A
        JOIN Episode E ON A.episode_id = E.episode_id AND A.season_id = E.season_id
        JOIN Judge J ON E.episode_id = J.episode_id AND E.season_id = J.season_id
        JOIN Shark S ON J.shark_id = S.shark_id
        LEFT JOIN Investment I ON A.company_id = I.company_id AND A.season_id = I.season_id AND A.episode_id = I.episode_id
        LEFT JOIN Contribute C ON I.investment_id = C.investment_id AND C.shark_id = S.shark_id
        GROUP BY S.shark_name
        HAVING COUNT(DISTINCT A.company_id) > 0
        ORDER BY deal_rate DESC;
        """

    elif "guest shark presence on deals" in query_name:
        # QUERY 7: Effect of guest shark presence on deals
        # PURPOSE: Compare deal-making activity in episodes with vs without guest sharks
        # BUSINESS LOGIC: Tests hypothesis that guest sharks affect investment behavior
        # STAKEHOLDERS: Show producers (casting decisions), Researchers (behavioral analysis)
        # TECHNICAL APPROACH:
        # - Subquery (episode_stats) calculates per-episode statistics
        # - MAX(S.is_guest) determines if episode has any guest sharks (1=yes, 0=no)
        # - COUNT(DISTINCT I.investment_id) counts deals per episode
        # - Outer query groups episodes by guest presence and calculates averages
        # - CASE WHEN converts binary to readable Yes/No format
        # - Result shows average deals per episode for each scenario
        sql = """
        SELECT 
            CASE WHEN has_guest = 1 THEN 'Yes' ELSE 'No' END AS has_guest,
            ROUND(AVG(deal_count), 2) AS average_deal_count
        FROM (
            SELECT 
                E.episode_id,
                E.season_id,
                MAX(S.is_guest) AS has_guest,
                COUNT(DISTINCT I.investment_id) AS deal_count
            FROM Episode E
            JOIN Judge J ON E.episode_id = J.episode_id AND E.season_id = J.season_id
            JOIN Shark S ON J.shark_id = S.shark_id
            LEFT JOIN Investment I ON E.episode_id = I.episode_id AND E.season_id = I.season_id
            GROUP BY E.episode_id, E.season_id
        ) AS episode_stats
        GROUP BY has_guest
        ORDER BY has_guest DESC;
        """

    elif "pitch order on success" in query_name:
        # QUERY 8: Impact of pitch order on success
        # PURPOSE: Analyze if presentation order within episodes affects deal success rates
        # BUSINESS LOGIC: Tests if going first, last, or middle affects entrepreneur success
        # STAKEHOLDERS: Entrepreneurs (strategy), Show producers (episode structure)
        # TECHNICAL APPROACH:
        # - Subquery (pitch_data) assigns pitch order using ROW_NUMBER() window function
        # - PARTITION BY episode ensures ordering resets for each episode
        # - ORDER BY company_id provides consistent ordering (proxy for pitch sequence)
        # - CASE WHEN converts investment status to binary (1=deal, 0=no deal)
        # - Outer query groups by pitch position and calculates success rates
        # - AVG of binary values gives success rate (0.0 to 1.0)
        # - WHERE pitch_order <= 5 focuses on first 5 positions for statistical significance
        sql = """
        SELECT 
            pitch_order,
            COUNT(*) AS total_pitches,
            AVG(CASE WHEN deal_status = 'Got Deal' THEN 1.0 ELSE 0.0 END) AS deal_success_rate
        FROM (
            SELECT 
                A.episode_id,
                A.season_id,
                C.company_name,
                ROW_NUMBER() OVER (PARTITION BY A.episode_id, A.season_id ORDER BY A.company_id) AS pitch_order,
                CASE WHEN I.investment_id IS NOT NULL THEN 'Got Deal' ELSE 'No Deal' END AS deal_status
            FROM Ask A
            JOIN Company C ON A.company_id = C.company_id
            LEFT JOIN Investment I ON A.company_id = I.company_id AND A.episode_id = I.episode_id AND A.season_id = I.season_id
        ) AS pitch_data
        WHERE pitch_order <= 5  -- Focus on first 5 pitch positions
        GROUP BY pitch_order
        ORDER BY pitch_order;
        """

    elif "Companies from a given city" in query_name:
        # QUERY 9: Companies from a given city/state and their deal stats
        # PURPOSE: Analyze geographic patterns in Shark Tank success rates
        # BUSINESS LOGIC: Identifies which cities/states produce most successful companies
        # STAKEHOLDERS: Economic development agencies, Companies (relocation decisions)
        # TECHNICAL APPROACH:
        # - JOIN chain: Entrepreneur -> Own -> Company -> Investment to link location to deals
        # - GROUP BY city and state for geographic aggregation
        # - COUNT(DISTINCT C.company_id) for total companies per location
        # - CASE WHEN with COUNT DISTINCT for conditional counting of successful companies
        # - Deal success rate = companies_with_deals / total_companies
        # - HAVING clause filters locations with <2 companies (statistical significance)
        # - WHERE clause allows optional filtering by user input (city name)
        # - LIKE '%{user_input}%' enables partial matching for city names
        sql = f"""
        SELECT 
            E.location_city AS city,
            E.location_state AS state,
            COUNT(DISTINCT C.company_id) AS total_companies,
            COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) AS companies_with_deals,
            ROUND(
                COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) * 1.0 / 
                NULLIF(COUNT(DISTINCT C.company_id), 0), 3
            ) AS deal_success_rate
        FROM Entrepreneur E
        JOIN Own O ON E.entrepreneur_id = O.entrepreneur_id
        JOIN Company C ON O.company_id = C.company_id
        LEFT JOIN Investment I ON C.company_id = I.company_id
        WHERE E.location_city LIKE '%{user_input if user_input else ''}%'
        GROUP BY E.location_city, E.location_state
        HAVING COUNT(DISTINCT C.company_id) >= 2  -- Only show cities with at least 2 companies
        ORDER BY deal_success_rate DESC, total_companies DESC;
        """

    elif "Companies by industry" in query_name:
        # QUERY 10: Companies by industry and their deal stats
        # PURPOSE: Analyze industry-level success patterns and investment amounts
        # BUSINESS LOGIC: Shows which industries have highest success rates and typical funding amounts
        # STAKEHOLDERS: Entrepreneurs (industry selection), Investors (sector analysis)
        # TECHNICAL APPROACH:
        # - Similar structure to Query 9 but grouped by industry instead of location
        # - Additional calculation: AVG(CASE WHEN...) for average investment amount
        # - Only averages investment amounts for successful deals (WHERE I.investment_id IS NOT NULL)
        # - ROUND functions for readable financial figures
        # - HAVING clause ensures statistical significance (>=2 companies per industry)
        # - WHERE clause allows optional filtering by industry name
        # - Combines success rate analysis with financial performance metrics
        sql = f"""
        SELECT 
            C.industry_name AS industry,
            COUNT(DISTINCT C.company_id) AS total_companies,
            COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) AS companies_with_deals,
            ROUND(
                COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) * 1.0 / 
                NULLIF(COUNT(DISTINCT C.company_id), 0), 3
            ) AS deal_success_rate,
            ROUND(AVG(CASE WHEN I.investment_id IS NOT NULL THEN I.equity_amount END), 0) AS average_amount_raised
        FROM Entrepreneur E
        JOIN Own O ON E.entrepreneur_id = O.entrepreneur_id
        JOIN Company C ON O.company_id = C.company_id
        LEFT JOIN Investment I ON C.company_id = I.company_id
        WHERE C.industry_name LIKE '%{user_input if user_input else ''}%'
        GROUP BY C.industry_name
        HAVING COUNT(DISTINCT C.company_id) >= 2  -- Only show industries with at least 2 companies
        ORDER BY deal_success_rate DESC, total_companies DESC;
        """

    elif "highest total amount invested" in query_name:
        # QUERY 11: Companies with highest total amount invested
        # PURPOSE: Identify companies that received the largest total investment amounts
        # BUSINESS LOGIC: Shows which companies attracted the most financial interest from sharks
        # STAKEHOLDERS: Media (success stories), Entrepreneurs (benchmarking)
        # TECHNICAL APPROACH:
        # - INNER JOIN between Investment and Company (only companies with investments)
        # - SUM(I.equity_amount) aggregates all investment amounts per company
        # - GROUP BY company_name to aggregate multiple investments per company
        # - ORDER BY total_invested DESC to rank by total investment amount
        # - Simple but effective query for identifying top performers
        sql = """
        SELECT C.company_name, SUM(I.equity_amount) AS total_invested
        FROM Investment I
        JOIN Company C ON I.company_id = C.company_id
        GROUP BY C.company_name
        ORDER BY total_invested DESC
        """

    elif "Episodes with highest accepted deal count" in query_name:
        # QUERY 12: Episodes with highest accepted deal count
        # PURPOSE: Identify episodes with the most successful deal-making activity
        # BUSINESS LOGIC: Shows which episodes were most productive for investments
        # STAKEHOLDERS: Show producers (content analysis), Researchers (episode factors)
        # TECHNICAL APPROACH:
        # - JOIN Episode with Season for complete episode identification
        # - LEFT JOIN with Investment to include episodes even without deals
        # - COUNT(DISTINCT I.investment_id) counts unique deals per episode
        # - GROUP BY episode and season for proper aggregation
        # - HAVING clause filters out episodes with zero deals
        # - ORDER BY accepted_deals DESC to rank most active episodes
        sql = """
        SELECT E.episode_id, S.season_id, COUNT(DISTINCT I.investment_id) AS accepted_deals
        FROM Episode E
        JOIN Season S ON E.season_id = S.season_id
        LEFT JOIN Investment I ON E.episode_id = I.episode_id AND E.season_id = I.season_id
        GROUP BY E.episode_id, S.season_id
        HAVING COUNT(DISTINCT I.investment_id) > 0
        ORDER BY accepted_deals DESC
        """

    elif "Average investment stats per season" in query_name:
        # QUERY 13: Average investment stats per season with deal success rate
        # PURPOSE: Analyze investment patterns and success rates across seasons
        # BUSINESS LOGIC: Shows financial metrics and deal success rates per season
        # STAKEHOLDERS: Show analysts (season performance), Investors (temporal trends)
        # TECHNICAL APPROACH:
        # - Uses Ask table to get all companies that pitched per season
        # - LEFT JOIN with Investment to identify successful deals
        # - Replicates Query 8 logic: AVG(CASE WHEN...) for deal success rate calculation
        # - COUNT(DISTINCT A.company_id) for total pitches per season
        # - COUNT(DISTINCT I.investment_id) for successful deals per season
        # - Financial aggregations only on successful investments
        # - COALESCE handles NULL values in financial calculations
        # - Deal success rate = successful_deals / total_pitches
        sql = """
        SELECT
            S.season_id,
            COUNT(DISTINCT A.company_id) AS total_pitches,
            COUNT(DISTINCT I.investment_id) AS total_investments,
            ROUND(
                AVG(CASE WHEN I.investment_id IS NOT NULL THEN 1.0 ELSE 0.0 END), 3
            ) AS deal_success_rate,
            COALESCE(SUM(I.equity_amount), 0) AS total_invested,
            ROUND(AVG(I.equity_amount), 0) AS avg_investment
        FROM Season S
        LEFT JOIN Ask A ON S.season_id = A.season_id
        LEFT JOIN Investment I ON A.company_id = I.company_id AND A.season_id = I.season_id AND A.episode_id = I.episode_id
        GROUP BY S.season_id
        HAVING COUNT(DISTINCT A.company_id) > 0  -- Only seasons with pitches
        ORDER BY S.season_id;
        """

    else:
        # FALLBACK HANDLER
        # Return empty DataFrame if query name doesn't match any known queries
        # This prevents application crashes from invalid query names
        conn.close()
        return pd.DataFrame()

    # QUERY EXECUTION AND RESULT PROCESSING
    # Execute the SQL query and return results as pandas DataFrame for Streamlit display
    try:
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        # Handle any SQL execution errors gracefully
        conn.close()
        print(f"Query execution error: {e}")
        return pd.DataFrame()
