import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import pandas as pd

def plot_valuation_chart(df):
    """
    Creates a horizontal bar chart showing the top 10 company valuations.
    
    Args:
        df (pandas.DataFrame): DataFrame containing company valuation data with columns:
            - company_name: Name of the company
            - valuation: Calculated valuation amount
            - industry_name: Industry category for color coding
    
    Returns:
        plotly.graph_objects.Figure: Interactive horizontal bar chart
        
    Features:
        - Color-coded by industry for easy pattern recognition
        - Horizontal orientation for better company name readability
        - Interactive hover information
    """
    return px.bar(
        df,
        x="valuation",
        y="company_name",
        color="industry_name",
        orientation="h",
        title="Top 10 Valuations",
        labels={"valuation": "Valuation ($)", "company_name": "Company"},
    )

def plot_network_graph(df):
    """
    Creates an interactive network graph showing shark collaboration patterns.
    Uses NetworkX for graph calculations and Plotly for interactive visualization.
    
    Args:
        df (pandas.DataFrame): DataFrame with shark collaboration data containing:
            - from_shark: First shark in collaboration
            - to_shark: Second shark in collaboration
    
    Returns:
        plotly.graph_objects.Figure: Interactive network graph
        
    Technical Details:
        - Node size represents number of connections (degree centrality)
        - Edge thickness represents collaboration frequency
        - Spring layout algorithm for optimal node positioning
        - Interactive hover shows connection details
    """
    # STEP 1: Calculate edge weights (frequency of co-investments between shark pairs)
    # Group by shark pairs and count occurrences to determine collaboration strength
    edge_weights = df.groupby(['from_shark', 'to_shark']).size().reset_index(name='weight')

    # STEP 2: Create NetworkX graph object with weighted edges
    # This allows us to use graph theory algorithms for layout and analysis
    G = nx.from_pandas_edgelist(edge_weights, 'from_shark', 'to_shark', edge_attr='weight')

    # STEP 3: Calculate node positions using spring layout algorithm
    # Spring layout creates aesthetically pleasing node arrangements by simulating physical forces
    # seed=42 ensures reproducible layouts across runs
    pos = nx.spring_layout(G, seed=42)

    # STEP 4: Prepare edge traces for Plotly visualization
    # Convert NetworkX edges to Plotly-compatible coordinate lists
    edge_x, edge_y, edge_widths = [], [], []
    for u, v, d in G.edges(data=True):
        x0, y0 = pos[u]  # Starting node coordinates
        x1, y1 = pos[v]  # Ending node coordinates
        edge_x += [x0, x1, None]  # None creates line breaks between edges
        edge_y += [y0, y1, None]
        edge_widths.append(d['weight'])  # Store edge weight for potential thickness variation

    # Create edge trace (lines connecting sharks)
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color='#888'),
        mode='lines'
    )

    # STEP 5: Prepare node traces for Plotly visualization
    # Node size is proportional to degree (number of connections)
    degrees = dict(G.degree())  # Calculate degree centrality for each shark
    node_x = [pos[node][0] for node in G.nodes()]  # X coordinates
    node_y = [pos[node][1] for node in G.nodes()]  # Y coordinates
    node_sizes = [degrees[node] * 5 for node in G.nodes()]  # Scale node size by connections
    node_text = [f"{node}<br>Connections: {degrees[node]}" for node in G.nodes()]  # Hover text

    # Create node trace (shark names and connection points)
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=list(G.nodes()),  # Shark names displayed on nodes
        textposition='top center',
        hovertext=node_text,  # Detailed hover information
        marker=dict(
            size=node_sizes,
            color='LightSkyBlue',
            line=dict(width=2)
        )
    )

    # STEP 6: Combine traces and create final figure
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Shark Co-Investment Network",
        showlegend=False,  # No legend needed for network graphs
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor='white'
    )

    return fig


def plot_strategy_heatmap(df):
    """
    Creates a heatmap showing shark investment strategies across different industries.
    
    Args:
        df (pandas.DataFrame): DataFrame containing shark investment strategy data with columns:
            - shark_name: Name of the shark investor
            - industry_name: Industry category
            - investment_count: Number of investments made
    
    Returns:
        plotly.graph_objects.Figure: Interactive heatmap visualization
        
    Features:
        - Color intensity represents investment frequency
        - Sharks ordered by total investment activity (most active at bottom)
        - Industry categories on X-axis for easy comparison
        - Dynamic height based on number of sharks
    """
    # EDGE CASE: Handle empty dataframes
    if df.empty:
        # Return minimal heatmap if no data available
        return px.imshow([[0]], labels=dict(x="Industry", y="Shark", color="Investments"))

    # STEP 1: Calculate total investments per shark for ordering
    # This ensures most active sharks appear at the top of the heatmap
    total_by_shark = (
        df.groupby("shark_name")["investment_count"]
        .sum()
        .sort_values(ascending=True)  # Most active sharks first
    )

    # STEP 2: Convert shark names to ordered categorical data
    # This ensures consistent ordering in the visualization
    df["shark_name"] = pd.Categorical(df["shark_name"], categories=total_by_shark.index, ordered=True)

    # STEP 3: Create density heatmap using Plotly Express
    # density_heatmap automatically handles the aggregation and color mapping
    fig = px.density_heatmap(
        df.sort_values("shark_name"),  # Ensure DataFrame respects category order
        x="industry_name",  # Industries on X-axis
        y="shark_name",     # Sharks on Y-axis
        z="investment_count",  # Color intensity based on investment count
        color_continuous_scale="Blues",  # Blue color scheme for professional appearance
        title="Shark Investment Strategy by Industry"
    )

    # STEP 4: Customize layout for better readability
    fig.update_layout(
        height=40 * df["shark_name"].nunique(),  # Dynamic height: 40px per shark
        yaxis_nticks=df["shark_name"].nunique(),  # Show all shark names on Y-axis
        xaxis=dict(showgrid=True, tickangle=45),  # Angled industry names for readability
    )

    return fig