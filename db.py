import mysql.connector
import pandas as pd

def connect_db():
    """
    Establishes connection to the MySQL database hosted on Google Cloud Platform.
    
    Returns:
        mysql.connector.connection: Active database connection object
        
    Note:
        - Uses hardcoded credentials for the cloud-hosted MySQL instance
        - Database name: 'Shark_Tank'
        - Host: Google Cloud Platform instance
    """
    return mysql.connector.connect(
        host="34.27.179.176", user="root", password="mpcsdatabase2025", database="Shark_Tank"
    )

def get_filtered_data(category, filters=None):
    """
    Retrieves filtered data from the database based on category and optional filters.
    This function serves multiple purposes:
    1. Populating dropdown menus in the Streamlit interface
    2. Fetching data for visualizations
    3. Retrieving raw table data for browsing
    
    Args:
        category (str): Type of data to retrieve (e.g., 'industry', 'shark', 'season', etc.)
        filters (dict, optional): Dictionary of filter criteria to apply
        
    Returns:
        list or pandas.DataFrame: Depends on category:
            - For dropdown data: list of unique values
            - For visualization data: pandas DataFrame
            - For raw tables: pandas DataFrame
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    # DROPDOWN DATA RETRIEVAL SECTION
    # These queries populate the filter dropdowns in the Streamlit sidebar
    
    if category == "industry":
        # Get all unique industry names for the industry filter dropdown
        cursor.execute("SELECT DISTINCT industry_name FROM Industry")
        return [row["industry_name"] for row in cursor.fetchall()]

    if category == "shark":
        # Get all unique shark names for the shark filter dropdown
        cursor.execute("SELECT DISTINCT shark_name FROM Shark")
        return [row["shark_name"] for row in cursor.fetchall()]

    if category == "season":
        # Get all season IDs ordered numerically for the season filter dropdown
        cursor.execute("SELECT DISTINCT season_id FROM Season ORDER BY season_id")
        return [row["season_id"] for row in cursor.fetchall()]

    if category == "city":
        # Get all unique cities where entrepreneurs are located
        cursor.execute("SELECT DISTINCT location_city FROM Entrepreneur")
        return [row["location_city"] for row in cursor.fetchall()]
    
    if category == "state":
        # Get all unique states where entrepreneurs are located
        cursor.execute("SELECT DISTINCT location_state FROM Entrepreneur")
        return [row["location_state"] for row in cursor.fetchall()]
    
    # VISUALIZATION DATA RETRIEVAL SECTION
    # These queries provide data specifically formatted for charts and graphs
    
    if category == "valuation":
        """
        Calculates company valuations based on investment deals.
        Valuation formula: (equity_amount / equity_share) * 100
        Returns top 10 valuations for the valuation bar chart.
        """
        query = """
            SELECT 
                C.company_name,
                FORMAT(AVG(I.equity_amount / I.equity_share * 100), 2) AS valuation,
                Ind.industry_name,
                S.season_id
            FROM Investment I
            JOIN Company C ON I.company_id = C.company_id
            JOIN Industry Ind ON C.industry_name = Ind.industry_name
            JOIN Season S ON I.season_id = S.season_id
            WHERE I.equity_amount IS NOT NULL AND I.equity_share IS NOT NULL AND I.equity_share != 0
            GROUP BY C.company_name, Ind.industry_name, S.season_id
            ORDER BY valuation DESC
            LIMIT 10
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    if category == "network":
        """
        Identifies shark co-investment relationships for network graph visualization.
        Finds pairs of sharks who invested in the same deals.
        Used to create the shark collaboration network graph.
        """
        query = """
            SELECT S1.shark_name AS from_shark, S2.shark_name AS to_shark
            FROM Contribute C1
            JOIN Investment I ON C1.investment_id = I.investment_id
            JOIN Contribute C2 ON C1.investment_id = C2.investment_id AND C1.shark_id != C2.shark_id
            JOIN Shark S1 ON C1.shark_id = S1.shark_id
            JOIN Shark S2 ON C2.shark_id = S2.shark_id
            LIMIT 100
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    elif category == "strategy":
        """
        Analyzes shark investment strategies by industry.
        Counts how many investments each shark made in each industry.
        Used for the strategy heatmap visualization.
        """
        query = """
            SELECT S.shark_name, C.industry_name, COUNT(*) AS investment_count
            FROM Investment I
            JOIN Contribute CN ON I.investment_id = CN.investment_id
            JOIN Shark S ON CN.shark_id = S.shark_id
            JOIN Company C ON I.company_id = C.company_id
            GROUP BY S.shark_name, C.industry_name
            ORDER BY S.shark_name, investment_count DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    # RAW TABLE DATA RETRIEVAL SECTION
    # Handles requests for complete table data browsing
    
    elif category == "raw_table":
        """
        Retrieves all data from a specified table for raw data browsing.
        Used in the "Browse Raw Data" tab to display complete table contents.
        """
        if filters and "table" in filters:
            table = filters["table"]
            try:
                df = pd.read_sql(f"SELECT * FROM {table}", connect_db())
                return df
            except Exception as e:
                print(f"Error loading table {table}: {e}")
                return pd.DataFrame()
        
    # DEFAULT FALLBACK
    # Return empty list if category doesn't match any known patterns
    return []