import mysql.connector
import pandas as pd

def connect_db():
    return mysql.connector.connect(
        host="34.27.179.176", user="root", password="mpcsdatabase2025", database="Shark_Tank"
    )

def get_filtered_data(category, filters=None):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    if category == "industry":
        cursor.execute("SELECT DISTINCT industry_name FROM Industry")
        return [row["industry_name"] for row in cursor.fetchall()]

    if category == "shark":
        cursor.execute("SELECT DISTINCT shark_name FROM Shark")
        return [row["shark_name"] for row in cursor.fetchall()]

    if category == "season":
        cursor.execute("SELECT DISTINCT season_id FROM Season ORDER BY season_id")
        return [row["season_id"] for row in cursor.fetchall()]

    if category == "city":
        cursor.execute("SELECT DISTINCT location_city FROM Entrepreneur")
        return [row["location_city"] for row in cursor.fetchall()]
    
    if category == "state":
        cursor.execute("SELECT DISTINCT location_state FROM Entrepreneur")
        return [row["location_state"] for row in cursor.fetchall()]
    
    if category == "valuation":
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

    elif category == "raw_table":
        if filters and "table" in filters:
            table = filters["table"]
            try:
                df = pd.read_sql(f"SELECT * FROM {table}", connect_db())
                return df
            except Exception as e:
                print(f"Error loading table {table}: {e}")
                return pd.DataFrame()
        
    # elif category.lower() in [
    #     "company", "investment", "industry", "entrepreneur", "episode", "season", "shark", "ask", "contribute", "own", "judge"
    # ]:
    #     base_query = f"SELECT * FROM {category}"
    #     where_clauses = []

    #     if filters:
    #         if category == "company" and filters.get("industry") != "All":
    #             where_clauses.append(f"industry_name = '{filters['industry']}'")

    #         if category == "entrepreneur" and filters.get("city") != "All":
    #             where_clauses.append(f"location_city = '{filters['city']}'")

    #         if category == "episode" and filters.get("season") != "All":
    #             where_clauses.append(f"season_id = {filters['season']}")

    #         # Add more filter logic as needed...

    #     if where_clauses:
    #         base_query += " WHERE " + " AND ".join(where_clauses)

    #     try:
    #         df = pd.read_sql(base_query, conn)
    #         conn.close()
    #         return df
    #     except Exception as e:
    #         print(f"Query failed: {e}")
    #         return pd.DataFrame()

    # Fallback: return an empty list if category is unknown
    return []