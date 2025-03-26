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
        self.beds = beds
        self.address = address
        self.price = price
        self.coord = coord

    def price_per_bed(self) -> float:
        return self.price / self.beds


class Area:
    """
    """
    name: str
    assault_rate: float
    homicide_rate: float
    theft_rate: float
    coord: tuple[float, float]

    def __init__(self, name: str, assault_rate: float, homicide_rate: float, theft_rate: float, coord: tuple[float, float]):
        self.name = name
        self.assault_rate = assault_rate
        self.homicide_rate = homicide_rate
        self.theft_rate = theft_rate
        self.coord = coord
        self.apartments: list[Apartment] = []

    def add_apartment(self, apt: Apartment) -> None:
        self.apartments.append(apt)

    def avg_price(self) -> float:
        if not self.apartments:
            return 0.0
        return sum(a.price for a in self.apartments) / len(self.apartments)


class Graph:
    """
    """
    areas: list[Area]
    apartments: list[Apartment]

    def __init__(self):
        self.areas = []
        self.apartments = []

    def add_area(self, area: Area) -> None:
        self.areas.append(area)
    
    def add_apartment(self, apt: Apartment) -> None:
        self.apartments.append(apt)

    def build_graph(neighbourhood_file: str, apartment_file: str) -> nx.Graph:
        """
        Build a graph from neighborhood and apartment data.
        """
        # Load data
        neighbourhoods = load_neighbourhood_data(neighbourhood_file)
        apartments = load_apartment_data(apartment_file)

        G = nx.Graph()

        # Add area nodes
        for _, row in neighbourhoods.iterrows():
            G.add_node(
                row['NEIGHBOURHOOD_NAME'],
                type="area",
                assault_rate=row['ASSAULT_RATE_2024'],
                homicide_rate=row['HOMICIDE_RATE_2024'],
                theft_rate=row['ROBBERY_RATE_2024']
            )

        # Add apartment nodes and connect to the closest area node
        for _, row in apartments.iterrows():
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                print(f"Skipping apartment with missing coordinates: {row['address']}")
                continue

            # Add apartment node
            G.add_node(
                row['address'],
                type="apartment",
                coord=(row['latitude'], row['longitude']),
                price=row['price'],
                bedrooms=row['bedrooms'],
                bathrooms=row['bathrooms']
            )

            # Find the closest area node
            closest_area = None
            min_distance = float('inf')
            for _, area_row in neighbourhoods.iterrows():
                area_coord = (area_row['latitude'], area_row['longitude'])
                apartment_coord = (row['latitude'], row['longitude'])
                distance = geodesic(apartment_coord, area_coord).km
                if distance < min_distance:
                    min_distance = distance
                    closest_area = area_row['NEIGHBOURHOOD_NAME']

            # Connect apartment to the closest area
            if closest_area:
                G.add_edge(row['address'], closest_area, relation="located_in", distance=min_distance)

        return G
