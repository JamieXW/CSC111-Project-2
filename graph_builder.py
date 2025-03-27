# === graph_builder.py ===
"""
This module constructs a graph of apartments and areas using NetworkX.
"""
import networkx as nx
from geopy.distance import geodesic
import pandas as pd
from data_loader import load_neighbourhood_data, load_apartment_data

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

    def build_graph(self, neighbourhood_file: str, apartment_file: str) -> nx.Graph:
        """
        Build a graph from neighborhood and apartment data.
        """
        # Load data
        neighbourhoods = load_neighbourhood_data(neighbourhood_file)
        apartments = load_apartment_data(apartment_file)

        G = nx.Graph()

        # Add area nodes
        for _, row in neighbourhoods.iterrows():
            area = Area(
                name=row['NEIGHBOURHOOD_NAME'],
                assault_rate=row['ASSAULT_RATE_2024'],
                homicide_rate=row['HOMICIDE_RATE_2024'],
                theft_rate=row['ROBBERY_RATE_2024'],
                coord=(row['latitude'], row['longitude'])
            )
            self.areas.append(area)  # Add to the areas attribute
            G.add_node(
                area.name,
                type="area",
                assault_rate=area.assault_rate,
                homicide_rate=area.homicide_rate,
                theft_rate=area.theft_rate
            )

        # Add apartment nodes and connect to the closest area node
        for _, row in apartments.iterrows():
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                print(f"Skipping apartment with missing coordinates: {row['address']}")
                continue

            apartment = Apartment(
                beds=row['bedrooms'],
                address=row['address'],
                price=row['price'],
                coord=(row['latitude'], row['longitude'])
            )
            self.apartments.append(apartment)  # Add to the apartments attribute
            G.add_node(
                apartment.address,
                type="apartment",
                coord=apartment.coord,
                price=apartment.price,
                bedrooms=apartment.beds
            )

            # Find the closest area node
            closest_area = None
            min_distance = float('inf')
            for area in self.areas:
                distance = geodesic(apartment.coord, area.coord).km
                if distance < min_distance:
                    min_distance = distance
                    closest_area = area.name

            # Connect apartment to the closest area
            if closest_area:
                G.add_edge(apartment.address, closest_area, relation="located_in", distance=min_distance)

        return G
