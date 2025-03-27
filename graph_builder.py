# === graph_builder.py ===
"""
This module constructs a graph of apartments and areas using NetworkX.
"""
import networkx as nx
from geopy.distance import geodesic
import pandas as pd
from data_loader import load_neighbourhood_data, load_apartment_data

class Apartment:
    """An apartment property.

    Instance Attributes:
        - beds: the number of beds in the apartment.
        - address: the address of the apartment.
        - price: the price of the apartment.
        - coord: the coordinate of latitude and longtitude of the apartment.

    Representation Invariants:
        - self.beds > 0
        - self.price > 0
        - len(self.address) > 0
        - -90 <= self.coord[0] <= 90  # valid latitude
        - -180 <= self.coord[1] <= 180  # valid longitude
    """
    beds: int
    address: str
    price: float
    coord: tuple[float, float]

    def __init__(self, beds: int, address: str, price: float, coord: tuple[float, float]):
        """Initialize a new apartment with the given attributes.
        """
        self.beds = beds
        self.address = address
        self.price = price
        self.coord = coord

    def price_per_bed(self) -> float:
        """Return the price per bedroom for this apartment.
        """
        return self.price / self.beds


class Area:
    """A neighborhood area in Toronto.

    Instance Attributes:
        - name: the name of the area.
        - assault_rate: the assault rate in the area.
        - homicide_rate: the homicide rate in the area.
        - theft_rate: the theft rate in the area.
        - coord: the coordinate of latitude and longtitude of the area.

    Representation Invariants:
        - len(self.name) > 0
        - self.assault_rate >= 0
        - self.homicide_rate >= 0
        - self.theft_rate >= 0
        - -90 <= self.coord[0] <= 90
        - -180 <= self.coord[1] <= 180

    """
    name: str
    assault_rate: float
    homicide_rate: float
    theft_rate: float
    coord: tuple[float, float]

    def __init__(self, name: str, assault_rate: float, homicide_rate: float, theft_rate: float, coord: tuple[float, float]):
        """Initialize a new area with the given attributes."""
        self.name = name
        self.assault_rate = assault_rate
        self.homicide_rate = homicide_rate
        self.theft_rate = theft_rate
        self.coord = coord
        self.apartments: list[Apartment] = []

    def add_apartment(self, apt: Apartment) -> None:
        """Add an apartment to this area's collection.
        """
        self.apartments.append(apt)

    def avg_price(self) -> float:
        """Calculate the average price of apartments in this area.
        """
        if not self.apartments:
            return 0.0
        return sum(a.price for a in self.apartments) / len(self.apartments)


class Graph:
    """A graph representation connecting apartments .

    Instance Attributes:
        - areas: collection of neighborhood areas in the graph.
        - apartments: collection of apartment properties in the graph.
    """
    areas: list[Area]
    apartments: list[Apartment]

    def __init__(self):
        """Initialize an empty graph with no areas or apartments.
        """
        self.areas = []
        self.apartments = []

    def add_area(self, area: Area) -> None:
        """Add a neighborhood area to the graph.
        """
        self.areas.append(area)

    def add_apartment(self, apt: Apartment) -> None:
        """Add an apartment property to the graph.
        """
        self.apartments.append(apt)

    def build_graph(self, neighbourhood_file: str, apartment_file: str) -> nx.Graph:
        """Build a graph from neighborhood and apartment data.
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
