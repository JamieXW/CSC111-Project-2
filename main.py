# === main.py ===
"""
Main file for the project. Builds the graph and visualizes it.
"""
from graph_builder import Graph
from visualization import visualize_graph


def main() -> None:
    """
    Main entry point for the project.

    This function builds a graph of apartments and areas using data from the specified CSV files.
    It then visualizes the graph and prints summary statistics, including the number of apartment nodes,
    area nodes, and edges in the graph.

    Preconditions:
        - The files specified in `neighbourhood_file` and `apartment_file` must exist and be formatted correctly.
    """
    print("Starting the program...")
    neighbourhood_file = 'data/Neighbourhood_crime_rates.csv'
    apartment_file = 'data/apartment_prices.csv'

    graph = Graph()
    print("Loading data...")
    new_graph = graph.build_graph(neighbourhood_file, apartment_file)
    print("Graph built successfully!")

    print("Visualizing the graph...")
    visualize_graph(new_graph)
    print("Number of apartment nodes:", sum(1 for n in new_graph.nodes if new_graph.nodes[n]['type'] == 'apartment'))
    print("Number of area nodes:", sum(1 for n in new_graph.nodes if new_graph.nodes[n]['type'] == 'area'))
    print("Number of edges:", new_graph.number_of_edges())


if __name__ == "__main__":

    # import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': ['graph_builder', 'visualization'],
    #     'allowed-io': ['main'],
    #     'max-line-length': 120,
    # })
    main()
