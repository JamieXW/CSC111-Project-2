# === visualization.py ===
"""
This module visualizes the graph of apartments and areas using Plotly and NetworkX.
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure

APARTMENT_COLOR = 'rgb(105, 89, 205)'  # Purple for apartments
EDGE_COLOR = 'rgb(210, 210, 210)'  # Light gray for edges
NODE_BORDER_COLOR = 'rgb(50, 50, 50)'  # Dark gray for node borders


def visualize_graph(G: nx.Graph, layout: str = 'spring_layout', output_file: str = '') -> None:
    """
    Visualize the graph using Plotly and NetworkX.

    :param G: The NetworkX graph to visualize.
    :param layout: The layout algorithm to use.
    :param output_file: If provided, save the visualization to this file instead of displaying it.
    """

    # Build positions for all nodes based on their coordinates.
    pos = {}
    for node in G.nodes:
        if 'coord' in G.nodes[node]:
            lat, lon = G.nodes[node]['coord']
            pos[node] = (lon, lat)
        else:
            pos[node] = (0, 0)

    # Prepare x and y values for node markers.
    x_values = [pos[node][0] for node in G.nodes]
    y_values = [pos[node][1] for node in G.nodes]

    # Create custom labels for each node:
    # For apartment nodes, calculate the price per bed (displayed above the node).
    # For hover text, we use the node's name (e.g., the address for apartments).
    price_per_bed_labels = []
    hover_labels = []
    for node in G.nodes:
        node_data = G.nodes[node]
        if node_data['type'] == 'apartment':
            price = node_data.get('price', 0)
            bedrooms = node_data.get('bedrooms', 1)  # Avoid division by zero.
            price_per_bed = price / bedrooms if bedrooms != 0 else 0
            price_per_bed_labels.append(f"${price_per_bed:.2f}")
            hover_labels.append(node)  # Assume node name is the address.
        else:
            price_per_bed_labels.append("")
            hover_labels.append(node)

    # Determine the color for each node.
    colors = [
        G.nodes[node]['color'] if G.nodes[node]['type'] == 'area' else APARTMENT_COLOR
        for node in G.nodes
    ]

    # Build edge coordinates.
    x_edges = []
    y_edges = []
    for edge in G.edges:
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

    # Create node trace with markers and text:
    # Markers show the nodes and text (price per bed) is displayed above.
    # The hover text shows the address for apartments (or node name).
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
        text=price_per_bed_labels,  # Display price per bed above the node.
        textposition='top center',
        hovertext=hover_labels,  # Display the address on hover.
        textfont=dict(
            size=7  # Set this to your desired font size.
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
