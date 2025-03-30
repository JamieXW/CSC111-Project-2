# === graph_builder.py ===
"""
This module constructs a graph of apartments and areas using NetworkX.
"""
from typing import Optional

import networkx as nx
import pandas as pd
from data_loader import load_neighbourhood_data, load_apartment_data
import math


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

    def avg_price(self) -> float:
        """Calculate the average price of apartments in this area.
        """
        if not self.apartments:
            return 0.0
        return sum(a.price for a in self.apartments) / len(self.apartments)


class Apartment:
    """An apartment property.

    Instance Attributes:
        - beds: the number of beds in the apartment.
        - bathrooms: the number of bathrooms in the apartment.
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
    bathrooms: int
    address: str
    price: float
    coord: tuple[float, float]
    closest_area: Optional['Area']

    def __init__(self, beds: int, bathrooms: int, address: str, price: float, coord: tuple[float, float]):
        """Initialize a new apartment with the given attributes.
        """
        self.beds = beds
        self.bathrooms = bathrooms
        self.address = address
        self.price = price
        self.coord = coord
        self.closest_area = None

    def price_per_bed(self) -> float:
        """Return the price per bedroom for this apartment.
        """
        return self.price / self.beds


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


    def add_edge(self, apartment_node: Apartment, area_node: Area) -> None:
        """
        Add an edge between an apartment and an area in the graph.
        """
        if apartment_node in self.apartments and area_node in self.areas:
            apartment_node.closest_area = area_node
        else:
            raise ValueError("Either the apartment or the area is not part of the graph.")


    def build_graph(self, neighbourhood_file: str, apartment_file: str) -> nx.Graph:
        """
        Build a graph from neighborhood and apartment data, filtering apartments based on user preferences.
        """
        # Prompt the user for filtering preferences
        print("Enter your preferences for apartments:")
        beds_pref = input("Number of beds (specific number or 'any'): ").strip().lower()
        baths_pref = input("Number of baths (specific number or 'any'): ").strip().lower()
        price_per_bed_pref = input("Price per bed (specific number or 'any'): ").strip().lower()

        # Convert preferences to numeric values if applicable
        if beds_pref.isdigit():
            beds_pref = int(beds_pref)
        else:
            beds_pref = None
        if baths_pref.isdigit():
            baths_pref = int(baths_pref)
        else:
            baths_pref = None

        price_per_bed_pref = price_per_bed_pref.replace('$', '')     #convert user input to remove $
        print(str(price_per_bed_pref))
        try:
            price_per_bed_pref = float(price_per_bed_pref)
        except ValueError:
            # If conversion fails, disable the filter
            print("valuee rror")
            price_per_bed_pref = None


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
            if area.coord is None or not all(isinstance(c, (int, float)) for c in area.coord):
                print(f"Skipping area with invalid coordinates: {area.name}")
                continue

            self.areas.append(area)
            G.add_node(
                area.name,
                type="area",
                assault_rate=area.assault_rate,
                homicide_rate=area.homicide_rate,
                theft_rate=area.theft_rate,
                coord=area.coord
            )

        # Add apartment nodes and connect to the closest area node
        for _, row in apartments.iterrows():
            apartment = Apartment(
                beds=row['Bedroom'],
                bathrooms=row['Bathroom'],
                address=row['Address'],
                price=row['Price'],
                coord=(row['Lat'], row['Long'])
            )

            # Validate apartment coordinates
            if apartment.coord is None or not all(isinstance(c, (int, float)) for c in apartment.coord):
                continue

            # Apply filtering based on user preferences
            if beds_pref is not None and apartment.beds != beds_pref:
                continue
            if baths_pref is not None and apartment.bathrooms != baths_pref:
                continue
            if price_per_bed_pref is not None:
                price_per_bed = apartment.price_per_bed()
                if price_per_bed > price_per_bed_pref:
                    continue

            self.apartments.append(apartment)
            G.add_node(
                apartment.address,
                type="apartment",
                coord=apartment.coord,
                price=apartment.price,
                bedrooms=apartment.beds,
                bathrooms=apartment.bathrooms
            )

            # Find the closest area node using Euclidean distance
            closest_area = self.areas[0]
            min_distance = math.sqrt(
                (apartment.coord[0] - closest_area.coord[0]) ** 2 +
                (apartment.coord[1] - closest_area.coord[1]) ** 2
            )
            for area in self.areas:
                distance = math.sqrt(
                    (apartment.coord[0] - area.coord[0]) ** 2 +
                    (apartment.coord[1] - area.coord[1]) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_area = area

            if closest_area:
                self.add_edge(apartment, closest_area)
                G.add_edge(apartment.address, closest_area.name, relation="located_in", distance=min_distance)

        return G
