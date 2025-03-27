# === visualizer.py ===
"""
This module visualizes the graph of apartments and areas using NetworkX and Matplotlib.
"""
import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph(G: nx.Graph) -> None:
    """
    Visualize the graph using NetworkX and Matplotlib.

    :param G: The NetworkX graph to visualize.
    """
    # Create a layout for the graph
    pos = nx.spring_layout(G, seed=42)  # Use spring layout for better visualization

    # Separate nodes by type
    area_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'area']
    apartment_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'apartment']

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=area_nodes, node_color='blue', label='Areas', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=apartment_nodes, node_color='green', label='Apartments', node_size=300)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray')

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Add legend
    plt.legend(scatterpoints=1, loc='upper right', fontsize=10)
    plt.title("Graph of Apartments and Areas")
    plt.axis('off')  # Turn off the axis
    plt.show()
