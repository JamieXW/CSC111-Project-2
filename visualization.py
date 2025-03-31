# === visualizer.py ===
"""
This module visualizes the graph of apartments and areas using Plotly and NetworkX.
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure


APARTMENT_COLOR = 'rgb(105, 89, 205)'  # Purple for apartments
EDGE_COLOR = 'rgb(210, 210, 210)'  # Light gray for edges
NODE_BORDER_COLOR = 'rgb(50, 50, 50)'  # Dark gray for node borders


def visualize_graph(graph: nx.Graph, output_file: str = '') -> None:
    """
    Visualize the graph using Plotly and NetworkX.

    :param G: The NetworkX graph to visualize.
    :param layout: The layout algorithm to use
    :param output_file: If provided, save the visualization to this file instead of displaying it.
    """

    pos = {}
    for node in graph.nodes:
        if 'coord' in graph.nodes[node]:
            lat, lon = graph.nodes[node]['coord']
            pos[node] = (lon, lat)
        else:
            pos[node] = (0, 0)

    x_values = [pos[n][0] for n in graph.nodes]
    y_values = [pos[n][1] for n in graph.nodes]

    price_per_bed_labels = []
    hover_labels = []
    for n in graph.nodes:
        node_data = graph.nodes[node]
        if node_data['type'] == 'apartment':
            price = node_data.get('price', 0)
            bedrooms = node_data.get('bedrooms', 1)
            price_per_bed = price / bedrooms if bedrooms != 0 else 0
            price_per_bed_labels.append(f"${price_per_bed:.2f}")
            hover_labels.append(node)
        else:
            price_per_bed_labels.append("")
            hover_labels.append(node)

    colors = [
        graph.nodes[node]['color'] if graph.nodes[node]['type'] == 'area' else APARTMENT_COLOR
        for node in graph.nodes
    ]

    x_edges = []
    y_edges = []
    for edge in graph.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    edge_trace = Scatter(
        x=x_edges,
        y=y_edges,
        mode='lines',
        line=dict(color=EDGE_COLOR, width=1),
        hoverinfo='none',
        name='edges'
    )

    node_trace = Scatter(
        x=x_values,
        y=y_values,
        mode='markers+text',
        marker=dict(
            symbol='circle-dot',
            size=10,
            color=colors,
            line=dict(color=NODE_BORDER_COLOR, width=0.5)
        ),
        text=price_per_bed_labels,
        textposition='top center',
        hovertext=hover_labels,
        textfont=dict(
            size=7
        ),
        hoverinfo='text',
        name='nodes'
    )

    fig = Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        title="Graph Visualization"
    )

    if output_file:
        fig.write_html(output_file)
    else:
        fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objs'],
        'allowed-io': [],
        'max-line-length': 120,
    })
