# query_logic.py
import pandas as pd
from db import connect_db

def run_query(query_name, user_input=None):
    conn = connect_db()

    if "Industries with most appearances" in query_name:
        sql = """
        SELECT C.industry_name, COUNT(*) AS company_count,
               SUM(CASE WHEN I.investment_id IS NOT NULL THEN 1 ELSE 0 END) AS deal_count
        FROM Company C
        LEFT JOIN Investment I ON C.company_id = I.company_id
        GROUP BY C.industry_name
        ORDER BY company_count DESC;
        """

    elif "Average & Range of Offers per Industry" in query_name:
        sql = """
        SELECT C.industry_name,
               MIN(A.equity_amount) AS Min_Amount,
               MAX(A.equity_amount) AS Max_Amount,
               AVG(A.equity_amount) AS Avg_Amount,
               AVG(A.equity_share) AS Avg_Equity
        FROM Ask A
        JOIN Company C ON A.company_id = C.company_id
        GROUP BY C.industry_name;
        """

    elif "Valuation trends across seasons" in query_name:
        sql = """
        SELECT S.season_id, C.industry_name,
               ROUND(AVG(I.equity_amount / I.equity_share * 100), 2) AS avg_valuation
        FROM Investment I
        JOIN Company C ON I.company_id = C.company_id
        JOIN Season S ON I.season_id = S.season_id
        WHERE I.equity_share > 0
        GROUP BY S.season_id, C.industry_name;
        """

    elif "Shark collaboration patterns" in query_name:
        sql = """
        SELECT S1.shark_name AS Shark1, S2.shark_name AS Shark2, COUNT(*) AS num_collaborations
        FROM Contribute C1
        JOIN Contribute C2 ON C1.investment_id = C2.investment_id AND C1.shark_id < C2.shark_id
        JOIN Shark S1 ON C1.shark_id = S1.shark_id
        JOIN Shark S2 ON C2.shark_id = S2.shark_id
        GROUP BY S1.shark_name, S2.shark_name
        ORDER BY num_collaborations DESC
        LIMIT 10;
        """

    elif "Top sharks by deal frequency" in query_name:
        sql = """
        SELECT S.shark_name,
               COUNT(*) AS total_deals,
               MAX(I.equity_amount) AS max_single_investment,
               SUM(I.equity_amount) AS total_investment
        FROM Investment I
        JOIN Contribute C ON I.investment_id = C.investment_id
        JOIN Shark S ON C.shark_id = S.shark_id
        GROUP BY S.shark_name
        ORDER BY total_investment DESC;
        """

    elif "Shark deal rate by episode and industry" in query_name:
        sql = """
        SELECT S.shark_name, COUNT(DISTINCT I.company_id) AS deals,
               COUNT(DISTINCT A.company_id) AS asks,
               ROUND(COUNT(DISTINCT I.company_id) / COUNT(DISTINCT A.company_id), 2) AS deal_rate
        FROM Ask A
        LEFT JOIN Investment I ON A.company_id = I.company_id AND A.season_id = I.season_id AND A.episode_id = I.episode_id
        LEFT JOIN Contribute C ON I.investment_id = C.investment_id
        LEFT JOIN Shark S ON C.shark_id = S.shark_id
        GROUP BY S.shark_name;
        """

    elif "guest shark presence on deals" in query_name:
        sql = """
        SELECT E.episode_id,
               MAX(S.is_guest) AS has_guest,
               COUNT(DISTINCT I.investment_id) AS deals
        FROM Episode E
        JOIN Judge J ON E.episode_id = J.episode_id
        JOIN Shark S ON J.shark_id = S.shark_id
        LEFT JOIN Investment I ON E.episode_id = I.episode_id
        GROUP BY E.episode_id;
        """

    elif "pitch order on success" in query_name:
        sql = """
        SELECT E.episode_id, C.company_name, I.investment_id IS NOT NULL AS got_investment
        FROM Episode E
        JOIN Ask A ON E.episode_id = A.episode_id
        JOIN Company C ON A.company_id = C.company_id
        LEFT JOIN Investment I ON A.company_id = I.company_id AND A.episode_id = I.episode_id;
        """

    elif "Entrepreneurs from a given city" in query_name:
        sql = f"""
        SELECT E.entrepreneur_name, E.location_city, C.company_name, I.equity_amount
        FROM Entrepreneur E
        JOIN Own O ON E.entrepreneur_id = O.entrepreneur_id
        JOIN Company C ON O.company_id = C.company_id
        LEFT JOIN Investment I ON C.company_id = I.company_id
        WHERE E.location_city LIKE '%{user_input if user_input else ''}%'
        ORDER BY E.entrepreneur_name;
        """

    elif "Entrepreneurs by industry" in query_name:
        sql = f"""
        SELECT E.entrepreneur_name, C.company_name, C.industry_name, I.equity_amount
        FROM Entrepreneur E
        JOIN Own O ON E.entrepreneur_id = O.entrepreneur_id
        JOIN Company C ON O.company_id = C.company_id
        LEFT JOIN Investment I ON C.company_id = I.company_id
        WHERE C.industry_name LIKE '%{user_input if user_input else ''}%'
        ORDER BY C.industry_name, E.entrepreneur_name;
        """

    elif "highest total amount offered" in query_name:
        sql = """
        SELECT C.company_name, SUM(I.equity_amount) AS total_offered
        FROM Investment I
        JOIN Company C ON I.company_id = C.company_id
        GROUP BY C.company_name
        ORDER BY total_offered DESC
        LIMIT 10;
        """

    elif "Episodes with highest accepted deal count" in query_name:
        sql = """
        SELECT E.episode_id, S.season_id, COUNT(DISTINCT I.investment_id) AS accepted_deals
        FROM Episode E
        JOIN Season S ON E.season_id = S.season_id
        LEFT JOIN Investment I ON E.episode_id = I.episode_id AND E.season_id = I.season_id
        GROUP BY E.episode_id, S.season_id
        HAVING COUNT(DISTINCT I.investment_id) > 0
        ORDER BY accepted_deals DESC
        LIMIT 10;
        """

    else:
        conn.close()
        return pd.DataFrame()

    df = pd.read_sql(sql, conn)
    conn.close()
    return df
