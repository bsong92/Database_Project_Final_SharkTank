# insert_data.py
# IMPORTS SECTION
# Core libraries for data insertion functionality
import streamlit as st  # Web interface framework
from db import connect_db  # Database connection function
import mysql.connector  # MySQL database connector for error handling
from datetime import datetime  # Date/time handling (imported but not currently used)

def insert_into_table(table):
    """
    Creates dynamic forms for inserting data into each database table with comprehensive validation.
    
    This function serves as the main entry point for all data insertion operations.
    It generates appropriate form fields based on the selected table and handles:
    - Input validation and sanitization
    - Foreign key constraint checking
    - Database transaction management
    - User feedback and error reporting
    
    Args:
        table (str): Name of the database table to insert data into
        
    Features:
        - Dynamic form generation based on table schema
        - Real-time validation with helpful error messages
        - Foreign key dependency guidance
        - Transaction rollback on errors
        - User-friendly success/error notifications
    """
    # DATABASE CONNECTION SETUP
    # Establish connection and cursor for database operations
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # INDUSTRY TABLE INSERTION
        # Base table with no foreign key dependencies - good starting point
        if table == "Industry":
            st.markdown("### Insert New Industry")
            
            # Form fields with validation hints
            industry_name = st.text_input("Industry Name*", help="Name of the industry (e.g., 'Technology', 'Food & Beverage')")
            market_size = st.text_input("Market Size*", help="Market size description (optional)")
            growth_rate = st.text_input("Growth Rate*", help="Growth rate description (optional)")
            
            # FORM SUBMISSION AND VALIDATION
            if st.button("Insert Industry", type="primary"):
                if industry_name:  # Only industry_name is truly required
                    try:
                        # Parameterized query to prevent SQL injection
                        cursor.execute("INSERT INTO Industry (industry_name, market_size, growth_rate) VALUES (%s, %s, %s)", 
                                     (industry_name, market_size if market_size else None, growth_rate if growth_rate else None))
                        conn.commit()  # Commit transaction
                        st.success(f"✅ Successfully inserted industry: {industry_name}")
                    except mysql.connector.IntegrityError as e:
                        # Handle duplicate key or constraint violations
                        st.error(f"❌ Error: Industry '{industry_name}' may already exist. {str(e)}")
                    except Exception as e:
                        # Handle any other database errors
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ Industry Name is required!")

        # SEASON TABLE INSERTION
        # Base table with date validation
        elif table == "Season":
            st.markdown("### Insert New Season")
            
            # Form fields with appropriate input types
            season_id = st.number_input("Season ID*", min_value=1, step=1, help="Unique season number")
            start_date = st.date_input("Start Date*", help="Season start date")
            end_date = st.date_input("End Date*", help="Season end date")
            
            if st.button("Insert Season", type="primary"):
                if season_id and start_date and end_date:
                    # BUSINESS LOGIC VALIDATION
                    # Ensure end date is after start date
                    if end_date >= start_date:
                        try:
                            cursor.execute("INSERT INTO Season (season_id, start_date, end_date) VALUES (%s, %s, %s)", 
                                         (season_id, start_date, end_date))
                            conn.commit()
                            st.success(f"✅ Successfully inserted Season {season_id}")
                        except mysql.connector.IntegrityError as e:
                            st.error(f"❌ Error: Season {season_id} may already exist. {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Database error: {str(e)}")
                    else:
                        st.error("❌ End date must be after start date!")
                else:
                    st.error("❌ All fields are required!")

        # SHARK TABLE INSERTION
        # Entity table with demographic information
        elif table == "Shark":
            st.markdown("### Insert New Shark")
            
            # Comprehensive form fields for shark information
            shark_id = st.number_input("Shark ID*", min_value=1, step=1, help="Unique shark identifier")
            shark_name = st.text_input("Shark Name*", help="Full name of the shark")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"], help="Shark's gender")
            age = st.number_input("Age*", min_value=18, max_value=100, step=1, help="Shark's age")
            occupation = st.text_input("Occupation*", help="Shark's primary occupation/business")
            is_guest = st.checkbox("Is Guest Shark?", help="Check if this is a guest shark (not a main panel member)")
            
            if st.button("Insert Shark", type="primary"):
                # Validate all required fields (excluding optional checkbox)
                if shark_id and shark_name and gender and age and occupation:
                    try:
                        cursor.execute("INSERT INTO Shark (shark_id, shark_name, gender, age, occupation, is_guest) VALUES (%s, %s, %s, %s, %s, %s)", 
                                     (shark_id, shark_name, gender, age, occupation, is_guest))
                        conn.commit()
                        st.success(f"✅ Successfully inserted shark: {shark_name}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Shark ID {shark_id} may already exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields except 'Is Guest Shark' are required!")

        # ENTREPRENEUR TABLE INSERTION
        # Entity table with geographic information
        elif table == "Entrepreneur":
            st.markdown("### Insert New Entrepreneur")
            
            # Form fields for entrepreneur demographics and location
            entrepreneur_id = st.number_input("Entrepreneur ID*", min_value=1, step=1, help="Unique entrepreneur identifier")
            entrepreneur_name = st.text_input("Entrepreneur Name*", help="Full name of the entrepreneur")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"], help="Entrepreneur's gender")
            location_city = st.text_input("City*", help="City where entrepreneur is based")
            location_state = st.text_input("State*", help="State where entrepreneur is based")
            
            if st.button("Insert Entrepreneur", type="primary"):
                if entrepreneur_id and entrepreneur_name and gender and location_city and location_state:
                    try:
                        cursor.execute("INSERT INTO Entrepreneur (entrepreneur_id, entrepreneur_name, gender, location_city, location_state) VALUES (%s, %s, %s, %s, %s)", 
                                     (entrepreneur_id, entrepreneur_name, gender, location_city, location_state))
                        conn.commit()
                        st.success(f"✅ Successfully inserted entrepreneur: {entrepreneur_name}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Entrepreneur ID {entrepreneur_id} may already exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields are required!")

        # EPISODE TABLE INSERTION
        # Depends on Season table (foreign key relationship)
        elif table == "Episode":
            st.markdown("### Insert New Episode")
            
            # Form fields for episode information
            episode_id = st.number_input("Episode ID*", min_value=1, step=1, help="Unique episode identifier")
            season_id = st.number_input("Season ID*", min_value=1, step=1, help="Season this episode belongs to")
            guest_present = st.checkbox("Guest Present?", help="Check if a guest shark was present in this episode")
            air_date = st.date_input("Air Date*", help="Date the episode aired")
            viewership = st.number_input("Viewership (millions)*", min_value=0.0, step=0.1, help="Viewership in millions")
            
            if st.button("Insert Episode", type="primary"):
                if episode_id and season_id and air_date and viewership:
                    try:
                        cursor.execute("INSERT INTO Episode (episode_id, season_id, guest_present, air_date, viewership) VALUES (%s, %s, %s, %s, %s)", 
                                     (episode_id, season_id, guest_present, air_date, viewership))
                        conn.commit()
                        st.success(f"✅ Successfully inserted Episode {episode_id} from Season {season_id}")
                    except mysql.connector.IntegrityError as e:
                        # Foreign key constraint violation likely means season doesn't exist
                        st.error(f"❌ Error: Episode may already exist or Season {season_id} doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields except 'Guest Present' are required!")

        # COMPANY TABLE INSERTION
        # Depends on Industry table (foreign key relationship)
        elif table == "Company":
            st.markdown("### Insert New Company")
            
            # Form fields for company information
            company_id = st.number_input("Company ID*", min_value=1, step=1, help="Unique company identifier")
            company_name = st.text_input("Company Name*", help="Name of the company")
            business_description = st.text_area("Business Description*", help="Description of what the company does", max_chars=5000)
            company_website = st.text_input("Company Website", help="Company website URL (optional)")
            industry_name = st.text_input("Industry Name*", help="Industry this company belongs to (must exist in Industry table)")
            
            if st.button("Insert Company", type="primary"):
                if company_id and company_name and business_description and industry_name:
                    try:
                        # Handle optional website field
                        cursor.execute("INSERT INTO Company (company_id, company_name, business_description, company_website, industry_name) VALUES (%s, %s, %s, %s, %s)", 
                                     (company_id, company_name, business_description, company_website if company_website else None, industry_name))
                        conn.commit()
                        st.success(f"✅ Successfully inserted company: {company_name}")
                    except mysql.connector.IntegrityError as e:
                        # Could be duplicate company ID or non-existent industry
                        st.error(f"❌ Error: Company ID {company_id} may already exist or Industry '{industry_name}' doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ Company ID, Name, Business Description, and Industry Name are required!")

        # ASK TABLE INSERTION
        # Transaction table linking Episode, Season, and Company
        elif table == "Ask":
            st.markdown("### Insert New Ask")
            
            # Form fields for funding requests
            episode_id = st.number_input("Episode ID*", min_value=1, step=1, help="Episode where the ask was made")
            season_id = st.number_input("Season ID*", min_value=1, step=1, help="Season where the ask was made")
            company_id = st.number_input("Company ID*", min_value=1, step=1, help="Company making the ask")
            equity_amount = st.number_input("Equity Amount ($)*", min_value=0, step=1000, help="Amount of money requested")
            equity_share = st.number_input("Equity Share (%)*", min_value=0.0, max_value=100.0, step=0.1, help="Percentage of equity offered")
            
            if st.button("Insert Ask", type="primary"):
                if episode_id and season_id and company_id and equity_amount and equity_share:
                    try:
                        cursor.execute("INSERT INTO Ask (episode_id, season_id, company_id, equity_amount, equity_share) VALUES (%s, %s, %s, %s, %s)",
                                     (episode_id, season_id, company_id, equity_amount, equity_share))
                        conn.commit()
                        st.success(f"✅ Successfully inserted ask for Company {company_id}")
                    except mysql.connector.IntegrityError as e:
                        # Multiple foreign key dependencies could fail
                        st.error(f"❌ Error: Ask may already exist or referenced Episode/Season/Company doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields are required!")

        # INVESTMENT TABLE INSERTION
        # Complex transaction table with multiple optional fields
        elif table == "Investment":
            st.markdown("### Insert New Investment")
            
            # Core investment fields
            investment_id = st.number_input("Investment ID*", min_value=1, step=1, help="Unique investment identifier")
            episode_id = st.number_input("Episode ID*", min_value=1, step=1, help="Episode where investment was made")
            season_id = st.number_input("Season ID*", min_value=1, step=1, help="Season where investment was made")
            company_id = st.number_input("Company ID*", min_value=1, step=1, help="Company receiving investment")
            equity_amount = st.number_input("Equity Amount ($)*", min_value=0, step=1000, help="Amount invested")
            equity_share = st.number_input("Equity Share (%)*", min_value=0.0, max_value=100.0, step=0.1, help="Percentage of equity received")
            
            # Optional investment terms
            loan = st.number_input("Loan Amount ($)", min_value=0, step=1000, help="Loan component (if any)")
            advisory_shares_equity = st.number_input("Advisory Shares Equity (%)", min_value=0.0, max_value=100.0, step=0.1, help="Advisory shares percentage")
            has_conditions = st.checkbox("Has Conditions?", help="Check if investment has special conditions")
            involve_royalty = st.checkbox("Involves Royalty?", help="Check if investment involves royalty payments")
            
            if st.button("Insert Investment", type="primary"):
                # Validate required fields only
                if investment_id and episode_id and season_id and company_id and equity_amount and equity_share:
                    try:
                        cursor.execute("INSERT INTO Investment (investment_id, episode_id, season_id, company_id, equity_amount, equity_share, loan, advisory_shares_equity, has_conditions, involve_royalty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                     (investment_id, episode_id, season_id, company_id, equity_amount, equity_share, loan, advisory_shares_equity, has_conditions, involve_royalty))
                        conn.commit()
                        st.success(f"✅ Successfully inserted Investment {investment_id}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Investment ID {investment_id} may already exist or referenced Episode/Season/Company doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ Investment ID, Episode ID, Season ID, Company ID, Equity Amount, and Equity Share are required!")

        # CONTRIBUTE TABLE INSERTION
        # Junction table linking Investments to Sharks (many-to-many relationship)
        elif table == "Contribute":
            st.markdown("### Insert New Contribution")
            
            # Form fields for shark contributions to investments
            investment_id = st.number_input("Investment ID*", min_value=1, step=1, help="Investment this contribution is part of")
            shark_id = st.number_input("Shark ID*", min_value=1, step=1, help="Shark making the contribution")
            equity_amount = st.number_input("Equity Amount ($)*", min_value=0, step=1000, help="Amount contributed by this shark")
            equity_share = st.number_input("Equity Share (%)*", min_value=0.0, max_value=100.0, step=0.1, help="Percentage of equity this shark receives")
            
            if st.button("Insert Contribution", type="primary"):
                if investment_id and shark_id and equity_amount and equity_share:
                    try:
                        cursor.execute("INSERT INTO Contribute (investment_id, shark_id, equity_amount, equity_share) VALUES (%s, %s, %s, %s)",
                                     (investment_id, shark_id, equity_amount, equity_share))
                        conn.commit()
                        st.success(f"✅ Successfully inserted contribution for Shark {shark_id} in Investment {investment_id}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Contribution may already exist or referenced Investment/Shark doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields are required!")

        # OWN TABLE INSERTION
        # Junction table linking Companies to Entrepreneurs (many-to-many relationship)
        elif table == "Own":
            st.markdown("### Insert New Ownership")
            
            # Simple relationship linking form
            company_id = st.number_input("Company ID*", min_value=1, step=1, help="Company being owned")
            entrepreneur_id = st.number_input("Entrepreneur ID*", min_value=1, step=1, help="Entrepreneur who owns the company")
            
            if st.button("Insert Ownership", type="primary"):
                if company_id and entrepreneur_id:
                    try:
                        cursor.execute("INSERT INTO Own (company_id, entrepreneur_id) VALUES (%s, %s)",
                                     (company_id, entrepreneur_id))
                        conn.commit()
                        st.success(f"✅ Successfully linked Entrepreneur {entrepreneur_id} to Company {company_id}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Ownership relationship may already exist or referenced Company/Entrepreneur doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ Both Company ID and Entrepreneur ID are required!")

        # JUDGE TABLE INSERTION
        # Junction table linking Episodes to Sharks (which sharks judged which episodes)
        elif table == "Judge":
            st.markdown("### Insert New Judge Assignment")
            
            # Form fields for judge assignments
            episode_id = st.number_input("Episode ID*", min_value=1, step=1, help="Episode where shark is judging")
            season_id = st.number_input("Season ID*", min_value=1, step=1, help="Season where shark is judging")
            shark_id = st.number_input("Shark ID*", min_value=1, step=1, help="Shark who is judging")
            
            if st.button("Insert Judge Assignment", type="primary"):
                if episode_id and season_id and shark_id:
                    try:
                        cursor.execute("INSERT INTO Judge (episode_id, season_id, shark_id) VALUES (%s, %s, %s)",
                                     (episode_id, season_id, shark_id))
                        conn.commit()
                        st.success(f"✅ Successfully assigned Shark {shark_id} as judge for Episode {episode_id}, Season {season_id}")
                    except mysql.connector.IntegrityError as e:
                        st.error(f"❌ Error: Judge assignment may already exist or referenced Episode/Season/Shark doesn't exist. {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.error("❌ All fields are required!")

        # UNSUPPORTED TABLE HANDLER
        else:
            st.error(f"❌ Table '{table}' is not supported for insertion.")

    # GLOBAL ERROR HANDLING
    except Exception as e:
        # Catch any unexpected errors not handled by specific table sections
        st.error(f"❌ Unexpected error: {str(e)}")
    finally:
        # CLEANUP: Always close database connection
        conn.close()


