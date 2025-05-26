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

    elif "Avg & range of offers per industry" in query_name:
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

    elif "Shark deal rate" in query_name:
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
        sql = """
        SELECT 
            CASE WHEN has_guest = 1 THEN 'Yes' ELSE 'No' END AS has_guest,
            AVG(deal_count) AS average_deal_count
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

    elif "Entrepreneurs from a given city" in query_name:
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

    elif "Entrepreneurs by industry" in query_name:
        sql = f"""
        SELECT 
            C.industry_name AS industry,
            COUNT(DISTINCT C.company_id) AS total_companies,
            COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) AS companies_with_deals,
            ROUND(
                COUNT(DISTINCT CASE WHEN I.investment_id IS NOT NULL THEN C.company_id END) * 1.0 / 
                NULLIF(COUNT(DISTINCT C.company_id), 0), 3
            ) AS deal_success_rate,
            ROUND(AVG(CASE WHEN I.investment_id IS NOT NULL THEN I.equity_amount END), 2) AS average_amount_raised
        FROM Entrepreneur E
        JOIN Own O ON E.entrepreneur_id = O.entrepreneur_id
        JOIN Company C ON O.company_id = C.company_id
        LEFT JOIN Investment I ON C.company_id = I.company_id
        WHERE C.industry_name LIKE '%{user_input if user_input else ''}%'
        GROUP BY C.industry_name
        HAVING COUNT(DISTINCT C.company_id) >= 2  -- Only show industries with at least 2 companies
        ORDER BY deal_success_rate DESC, total_companies DESC;
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
