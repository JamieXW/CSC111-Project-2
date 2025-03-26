# === graph_builder.py ===
"""
This module constructs a graph of apartments and areas using NetworkX.
"""
import networkx as nx
from geopy.distance import geodesic


class Apartment:
    """
    """
    beds: int
    address: str
    price: float
    coord: tuple[float, float]
    
    def __init__(self, beds: int, address: str, price: float, coord: tuple[float, float]):
        self.beds = int
        self.address = address
        self.price = price
        self.coord = coord

    def price_per_bed(self) -> float:
        return self.price / self.beds


class Area:
    """
    """
    name = str
    coord = tuple[float, float]
    
    def __init__(self, name: str, coord: tuple[float, float]):
        self.name = name
        self.coord = coord
        self.apartments: list[Apartment] = []

    def add_apartment(self, apt: Apartment) -> None:
        self.apartments.append(apt)

    def avg_price(self) -> float:
        if not self.apartments:
            return 0.0
        return sum(a.price for a in self.apartments) / len(self.apartments)


def build_graph(areas: list[Area]) -> nx.Graph:
    G = nx.Graph()

    for area in areas:
        G.add_node(area.name, type="area", coord=area.coord, avg_price=area.avg_price())
        for apt in area.apartments:
            G.add_node(apt.address, type="apartment", coord=apt.coord, price=apt.price)
            G.add_edge(apt.address, area.name, relation="located_in")

    # Add edges between nearby areas (within 3km)
    for i, area1 in enumerate(areas):
        for j, area2 in enumerate(areas):
            if i < j:
                dist = geodesic(area1.coord, area2.coord).km
                if dist < 3.0:
                    G.add_edge(area1.name, area2.name, relation="nearby", distance=dist)

    return G
