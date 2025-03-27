# === visualizer.py ===
"""
This module visualizes the housing graph using Plotly.
"""
import plotly.graph_objects as go
import networkx as nx

# hi

def draw_graph(G: nx.Graph) -> None:
    """
    Visualize the housing graph.
    """
    pos = {node: G.nodes[node]['coord'][::-1] for node in G.nodes if 'coord' in G.nodes[node]}
    edge_x = []
    edge_y = []

    for edge in G.edges():
        if all(n in pos for n in edge):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

    edge_trace = go.Scattergeo(
        lon=edge_x,
        lat=edge_y,
        mode='lines',
        line=dict(width=0.5, color='gray'),
        hoverinfo='none'
    )

    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        if node in pos:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            info = G.nodes[node]
            if info['type'] == 'area':
                label = f"Area: {node}<br>Avg Price: ${info['avg_price']:.0f}"
            else:
                label = f"Apartment: {node}<br>Price: ${info['price']:.0f}"
            text.append(label)

    node_trace = go.Scattergeo(
        lon=node_x,
        lat=node_y,
        mode='markers',
        marker=dict(size=8, color='blue'),
        text=text,
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='Toronto Housing Graph',
        geo=dict(scope='north america', projection_type='equirectangular'),
        showlegend=False
    )
    fig.show()
