# === main.py ===
"""
Main entry point for the project. Builds the graph and visualizes it.
"""
from graph_builder import Graph
from visualization import visualize_graph


def main():
    print("Starting the program...")
    # File paths for the data
    neighbourhood_file = 'data/Neighbourhood_crime_rates.csv'
    apartment_file = 'data/apartment_prices.csv'

    # Build the graph
    graph = Graph()
    print("Loading data...")
    G = graph.build_graph(neighbourhood_file, apartment_file)
    print("Graph built successfully!")

    # Visualize the graph
    print("Visualizing the graph...")
    visualize_graph(G)


if __name__ == "__main__":
    main()
