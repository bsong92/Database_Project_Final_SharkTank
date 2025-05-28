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
    # These queries populate the possible values in the Streamlit sidebar
    
    if category == "industry":
        # Get all unique industry names for the industry possible values
        cursor.execute("SELECT DISTINCT industry_name FROM Industry")
        return [row["industry_name"] for row in cursor.fetchall()]

    if category == "shark":
        # Get all unique shark names for the shark possible values
        cursor.execute("SELECT DISTINCT shark_name FROM Shark")
        return [row["shark_name"] for row in cursor.fetchall()]

    if category == "season":
        # Get all season IDs ordered numerically for the season possible values
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
    
    if category == "strategy":
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