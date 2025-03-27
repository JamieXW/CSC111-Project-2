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

    # Draw area nodes
    nx.draw_networkx_nodes(
        G, pos, nodelist=area_nodes, node_color='blue', label='Areas', node_size=800
    )

    # Draw apartment nodes
    nx.draw_networkx_nodes(
        G, pos, nodelist=apartment_nodes, node_color='green', label='Apartments', node_size=500
    )

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5)

    # Draw labels for area nodes
    nx.draw_networkx_labels(
        G, pos, labels={node: node for node in area_nodes}, font_size=10, font_color='white'
    )

    # Draw labels for apartment nodes
    nx.draw_networkx_labels(
        G, pos, labels={node: node for node in apartment_nodes}, font_size=8, font_color='black'
    )

    # Add legend
    plt.legend(
        handles=[
            plt.Line2D([0], [0], marker='o', color='w', label='Areas', markersize=10, markerfacecolor='blue'),
            plt.Line2D([0], [0], marker='o', color='w', label='Apartments', markersize=8, markerfacecolor='green'),
        ],
        loc='upper right',
        fontsize=10
    )

    # Add title and turn off axis
    plt.title("Graph of Apartments and Areas")
    plt.axis('off')  # Turn off the axis
    plt.show()
