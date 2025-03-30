# === main.py ===
"""
Main entry point for the project. Builds the graph and visualizes it.
"""
from graph_builder import Graph
from visualization import visualize_graph

def main():
    print("Starting the program...")
    neighbourhood_file = 'data/Neighbourhood_crime_rates.csv'
    apartment_file = 'data/apartment_prices.csv'

    graph = Graph()
    print("Loading data...")
    G = graph.build_graph(neighbourhood_file, apartment_file) 
    print("Graph built successfully!")

    print("Visualizing the graph...")
    visualize_graph(G)
    print("Number of apartment nodes:", sum(1 for n in G.nodes if G.nodes[n]['type'] == 'apartment'))
    print("Number of area nodes:", sum(1 for n in G.nodes if G.nodes[n]['type'] == 'area'))
    print("Number of edges:", G.number_of_edges())


if __name__ == "__main__":
    main()