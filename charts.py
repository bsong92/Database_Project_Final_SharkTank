import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

def plot_valuation_chart(df):
    return px.bar(df, x="company_name", y="valuation", color="industry_name", title="Top 10 Valuations")

def plot_network_graph(df):
    # Calculate edge weights (number of co-investments between sharks)
    edge_weights = df.groupby(['from_shark', 'to_shark']).size().reset_index(name='weight')

    # Create graph with edge weights
    G = nx.from_pandas_edgelist(edge_weights, 'from_shark', 'to_shark', edge_attr='weight')

    pos = nx.spring_layout(G, seed=42)

    # Edges with varying thickness
    edge_x, edge_y, edge_widths = [], [], []
    for u, v, d in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_widths.append(d['weight'])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color='#888'),
        mode='lines'
    )

    # Node size = number of connections (degree)
    degrees = dict(G.degree())
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_sizes = [degrees[node] * 5 for node in G.nodes()]  # Scale node size
    node_text = [f"{node}<br>Connections: {degrees[node]}" for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=list(G.nodes()),
        textposition='top center',
        hovertext=node_text,
        marker=dict(
            size=node_sizes,
            color='LightSkyBlue',
            line=dict(width=2)
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Shark Co-Investment Network",
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor='white'
    )

    return fig

# def plot_network_graph(df):
#     G = nx.from_pandas_edgelist(df, "from_shark", "to_shark")
#     pos = nx.spring_layout(G)
#     edge_x, edge_y = [], []
#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x += [x0, x1, None]
#         edge_y += [y0, y1, None]
    
#     edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')
#     node_trace = go.Scatter(
#         x=[pos[n][0] for n in G.nodes()],
#         y=[pos[n][1] for n in G.nodes()],
#         text=list(G.nodes),
#         mode='markers+text',
#         marker=dict(size=10, color='LightSkyBlue')
#     )
    
#     fig = go.Figure(data=[edge_trace, node_trace])
#     fig.update_layout(title="Shark Co-Investment Network", showlegend=False)
#     return fig

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