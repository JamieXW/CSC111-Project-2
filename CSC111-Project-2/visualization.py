
# === visualizer.py ===
"""
This module visualizes the graph of apartments and areas using Plotly and NetworkX.
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure

# Colors for different node types
AREA_COLOR = 'rgb(89, 205, 105)'  # Green for areas
APARTMENT_COLOR = 'rgb(105, 89, 205)'  # Purple for apartments
EDGE_COLOR = 'rgb(210, 210, 210)'  # Light gray for edges
NODE_BORDER_COLOR = 'rgb(50, 50, 50)'  # Dark gray for node borders


def visualize_graph(G: nx.Graph, layout: str = 'spring_layout', output_file: str = '') -> None:
    """
    Visualize the graph using Plotly and NetworkX.

    :param G: The NetworkX graph to visualize.
    :param layout: The layout algorithm to use (e.g., 'spring_layout', 'circular_layout').
    :param output_file: If provided, save the visualization to this file instead of displaying it.
    """
    # Generate the layout for the graph
    # Build a position dictionary from the node's coord attribute
    pos = {}
    for node in G.nodes:
        if 'coord' in G.nodes[node]:
            # Usually 'coord' is stored as (latitude, longitude).
            # If you want X=longitude and Y=latitude, do this:
            lat, lon = G.nodes[node]['coord']
            pos[node] = (lon, lat)
        else:
            # Fallback if the node somehow has no 'coord'
            pos[node] = (0, 0)

    # Extract node positions, labels, and types
    x_values = [pos[node][0] for node in G.nodes]
    y_values = [pos[node][1] for node in G.nodes]
    labels = list(G.nodes)
    types = [G.nodes[node]['type'] for node in G.nodes]

    # Assign colors based on node type
    colors = [AREA_COLOR if node_type == 'area' else APARTMENT_COLOR for node_type in types]

    # Extract edge positions
    x_edges = []
    y_edges = []
    for edge in G.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # Create edge traces
    edge_trace = Scatter(
        x=x_edges,
        y=y_edges,
        mode='lines',
        line=dict(color=EDGE_COLOR, width=1),
        hoverinfo='none',
        name='edges'
    )

    # Create node traces
    node_trace = Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(
            symbol='circle-dot',
            size=10,
            color=colors,
            line=dict(color=NODE_BORDER_COLOR, width=0.5)
        ),
        text=labels,
        hovertemplate='%{text}',
        hoverlabel={'namelength': 0},
        name='nodes'
    )

    # Combine traces into a figure
    fig = Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        title="Graph Visualization"
    )

    # Display or save the visualization
    if output_file:
        fig.write_html(output_file)
    else:
        fig.show()
