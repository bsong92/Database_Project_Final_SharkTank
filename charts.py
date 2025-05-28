import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import pandas as pd

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
    # This ensures most active sharks appear at the bottom of the heatmap next to the x-axis
    total_by_shark = (
        df.groupby("shark_name")["investment_count"]
        .sum()
        .sort_values(ascending=False)  # Most active sharks first
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