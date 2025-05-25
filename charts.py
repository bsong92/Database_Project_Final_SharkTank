import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

def plot_valuation_chart(df):
    return px.bar(df, x="company_name", y="valuation", color="industry_name", title="Top 10 Valuations")

def plot_network_graph(df):
    G = nx.from_pandas_edgelist(df, "from_shark", "to_shark")
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')
    node_trace = go.Scatter(
        x=[pos[n][0] for n in G.nodes()],
        y=[pos[n][1] for n in G.nodes()],
        text=list(G.nodes),
        mode='markers+text',
        marker=dict(size=10, color='LightSkyBlue')
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Shark Co-Investment Network", showlegend=False)
    return fig

def plot_strategy_heatmap(df):
    if df.empty:
        return px.imshow([[0]], labels=dict(x="Industry", y="Shark", color="Investments"))

    return px.density_heatmap(
        df,
        x="industry_name",
        y="shark_name",
        z="investment_count",
        color_continuous_scale="Blues",
        title="Shark Investment Strategy by Industry"
    )