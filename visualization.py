# === visualizer.py ===
"""
This module visualizes the graph of apartments and areas using PyVis.
"""
from pyvis.network import Network


def visualize_graph(G):
    """
    Visualize the graph using PyVis.

    :param G: The NetworkX graph to visualize.
    """
    # Create a PyVis network
    net = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Add nodes to the PyVis network
    for node, data in G.nodes(data=True):
        if data.get('type') == 'area':
            net.add_node(
                node,
                label=node,
                title=f"Type: Area<br>Assault Rate: {data.get('assault_rate', 'N/A')}<br>"
                      f"Homicide Rate: {data.get('homicide_rate', 'N/A')}<br>"
                      f"Theft Rate: {data.get('theft_rate', 'N/A')}",
                color="blue",
                size=20
            )
        elif data.get('type') == 'apartment':
            net.add_node(
                node,
                label=node,
                title=f"Type: Apartment<br>Price: {data.get('price', 'N/A')}<br>"
                      f"Bedrooms: {data.get('bedrooms', 'N/A')}<br>"
                      f"Bathrooms: {data.get('bathrooms', 'N/A')}",
                color="green",
                size=15
            )

    # Add edges to the PyVis network
    for source, target, data in G.edges(data=True):
        net.add_edge(
            source,
            target,
            title=f"Distance: {data.get('distance', 'N/A')} km",
            color="gray"
        )

    # Generate and open the visualization in a web browser
    net.show("graph_visualization.html")
