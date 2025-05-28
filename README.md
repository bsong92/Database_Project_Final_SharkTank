# 🦈 Shark Tank Insights Explorer

A comprehensive database application built for analyzing real-world Shark Tank data through an interactive web interface. This project demonstrates the integration of database design, web development, data analytics, and business intelligence in a cohesive, user-friendly application.

## Project Overview

**Course**: Database Systems Final Project  
**Topic**: Shark Tank Investment Analysis  
**Objective**: Develop a GUI application to explore and manage Shark Tank data with advanced querying capabilities

### Purpose

The Shark Tank Insights Explorer helps users:
- **Analyze trends** in investments, industries, and shark behavior
- **Visualize** co-investment networks and strategic patterns  
- **Insert new data** entries like companies, entrepreneurs, or episodes
- **Explore** underlying Shark Tank data through interactive queries

## Architecture & Technology Stack

### **Frontend**
- **Streamlit**: Python web framework for rapid UI development
- **Plotly**: Interactive visualizations and charts
- **Pandas**: Data manipulation and analysis

### **Backend** 
- **Python**: Core application logic
- **MySQL**: Relational database management
- **NetworkX**: Graph analysis for shark collaboration networks

### **Database**
- **Host**: Google Cloud Platform MySQL instance
- **Schema**: 11 interconnected tables with proper normalization
- **Data**: Real Shark Tank episodes, investments, and participant information

## 📊 Database Schema

### **Core Entity Tables**
- **Industry**: Business sectors and market information
- **Season**: TV show seasons with temporal data
- **Shark**: Investor profiles and demographics  
- **Entrepreneur**: Business owner information and locations
- **Episode**: Individual show episodes with viewership data
- **Company**: Businesses that pitched on the show

### **Relationship Tables**
- **Ask**: Initial funding requests and terms
- **Investment**: Actual deals made with detailed terms
- **Contribute**: Individual shark contributions to investments
- **Own**: Company ownership relationships
- **Judge**: Episode judging assignments

## Features

### **1. Query Explorer** 📊
**13 Pre-built Business Intelligence Queries:**

1. **Industries with Most Appearances and Deal Rates** - Market sector analysis
2. **Average & Range of Offers per Industry** - Financial benchmarking
3. **Valuation Trends Across Seasons** - Temporal market analysis
4. **Shark Collaboration Patterns** - Partnership identification
5. **Top Sharks by Deal Frequency & Investment** - Investor rankings
6. **Shark Deal Rate** - Success rate analysis
7. **Effect of Guest Shark Presence** - Behavioral impact study
8. **Impact of Pitch Order on Success** - Presentation timing analysis
9. **Entrepreneurs by Geographic Location** - Regional success patterns
10. **Entrepreneurs by Industry Performance** - Sector-specific analysis
11. **Companies with Highest Investment Amounts** - Top performers
12. **Episodes with Most Accepted Deals** - Episode productivity
13. **Average Investment Stats per Season** - Seasonal trends

**Features:**
- Interactive result filtering
- CSV export functionality  
- Dynamic query descriptions
- Real-time data processing

### **2. Investment Strategy Visualizations** 📈
- **Strategy Heatmap**: Shark investment patterns by industry
- **Network Graphs**: Collaboration relationships between sharks
- **Valuation Charts**: Company performance comparisons

### **3. Data Management** ➕
- **Comprehensive Forms**: Insert data into all 11 tables
- **Validation**: Input validation with helpful error messages
- **Foreign Key Guidance**: Dependency management and insertion order
- **Error Handling**: Graceful handling of constraint violations

### **4. Raw Data Browser** 📂
- **Table Exploration**: View complete contents of any table
- **Data Export**: Download raw data as CSV files
- **Interactive Display**: Sortable and searchable data tables

## Installation & Setup

### **Prerequisites**
```bash
Python 3.7+
pip (Python package manager)
```

### **1. Clone Repository**
```bash
git clone <repository-url>
cd Database_Project_Final_SharkTank
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run Application**
```bash
streamlit run app.py
```

### **4. Access Application**
Open your browser and navigate to: `http://localhost:8501`

## Dependencies

```
streamlit          # Web application framework
mysql-connector-python  # MySQL database connectivity
pandas            # Data manipulation and analysis
plotly            # Interactive visualizations
networkx          # Graph analysis and network visualization
```

## Usage Guide

### **Getting Started**
1. **Launch Application**: Run `streamlit run app.py`
2. **Welcome Screen**: Click "🚀 Enter App" to access the dashboard
3. **Navigation**: Use the four main tabs to explore different features

### **Query Explorer Workflow**
1. Select a query from the dropdown menu
2. Click "Run Query" to execute
3. Use filters to refine results
4. Export data using "Export CSV" button

### **Data Insertion Workflow**
1. Navigate to "Insert Data" tab
2. Select table from dropdown
3. Fill required fields (marked with *)
4. Follow recommended insertion order for foreign keys
5. Submit form and verify success message

### **Visualization Exploration**
1. Go to "Investment Strategy" tab
2. Explore interactive heatmaps and network graphs
3. Use hover features for detailed information

## File Structure

```
Database_Project_Final_SharkTank/
├── app.py              # Main Streamlit application
├── db.py               # Database connection and data retrieval
├── query_logic.py      # Business intelligence queries
├── insert_data.py      # Data insertion functionality
├── charts.py           # Visualization components
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

### **File Descriptions**

- **`app.py`**: Main application entry point with UI components and navigation
- **`db.py`**: Database connection management and filtered data retrieval
- **`query_logic.py`**: 13 pre-built analytical queries with business logic
- **`insert_data.py`**: Dynamic form generation for data insertion
- **`charts.py`**: Plotly visualizations including heatmaps and network graphs

## Business Value

### **For Entrepreneurs**
- Market analysis and industry benchmarking
- Geographic success pattern identification
- Optimal pitch timing and strategy insights

### **For Investors**
- Shark behavior and collaboration analysis
- Investment trend identification
- Portfolio performance tracking

### **For Researchers**
- Comprehensive dataset for venture capital studies
- Network analysis of investor relationships
- Temporal trend analysis capabilities

### **For Show Producers**
- Episode performance metrics
- Guest shark impact analysis
- Content optimization insights

## 🔍 Key Technical Features

### **Advanced SQL Capabilities**
- **Window Functions**: For pitch order and ranking analysis
- **Self-Joins**: For shark collaboration detection
- **Conditional Aggregation**: For success rate calculations
- **Complex JOINs**: Multi-table relationship analysis

### **User Experience**
- **Responsive Design**: Works across different screen sizes
- **Interactive Filtering**: Real-time data manipulation
- **Error Handling**: Graceful database error management
- **Data Export**: CSV download functionality

### **Data Integrity**
- **Foreign Key Constraints**: Maintains referential integrity
- **Input Validation**: Comprehensive form validation
- **Transaction Management**: Proper database transaction handling

## 🚧 Future Enhancements

- **Advanced Filtering**: Global filters across all data views
- **Custom Query Builder**: User-defined query creation
- **Dashboard Analytics**: Real-time metrics and KPIs
- **Data Visualization**: Additional chart types and interactions
- **User Authentication**: Multi-user access control
- **API Integration**: External data source connections

## Contributing

This project was developed as a final project for a Database Systems course. For educational purposes, the codebase demonstrates:

- **Database Design**: Proper normalization and relationship modeling
- **Web Development**: Modern Python web application architecture
- **Data Analytics**: Business intelligence and statistical analysis
- **Visualization**: Interactive data presentation techniques

## License

This project is developed for educational purposes as part of a Database Systems course.

## Support

For questions about the implementation or database design, please refer to the comprehensive code comments throughout the project files.
