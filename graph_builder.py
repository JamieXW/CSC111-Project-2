# === graph_builder.py ===
"""
This module constructs a graph of apartments and areas using NetworkX.
"""
from typing import Optional
import math
import networkx as nx
from data_loader import load_neighbourhood_data, load_apartment_data


class Area:
    """A neighborhood area in Toronto.

    Instance Attributes:
        - name: the name of the area.
        - assault_rate: the assault rate in the area.
        - homicide_rate: the homicide rate in the area.
        - robbery_rate: the robbery rate in the area.
        - coord: the coordinate of latitude and longitude of the area.

    Representation Invariants:
        - len(self.name) > 0
        - self.assault_rate >= 0
        - self.homicide_rate >= 0
        - self.robbery_rate >= 0
        - -90 <= self.coord[0] <= 90
        - -180 <= self.coord[1] <= 180

    """
    name: str
    assault_rate: float
    homicide_rate: float
    robbery_rate: float
    coord: tuple[float, float]
    apartments: list['Apartment']

    def __init__(self, name: str, assault_rate: float,
                 homicide_rate: float, robbery_rate: float, coord: tuple[float, float]) -> None:
        """Initialize a new area with the given attributes."""
        self.name = name
        self.assault_rate = assault_rate
        self.homicide_rate = homicide_rate
        self.robbery_rate = robbery_rate
        self.coord = coord
        self.apartments = []

    def avg_price(self) -> float:
        """Calculate the average price of apartments in this area."""
        if not self.apartments:
            return 0.0
        return sum(apartment.price for apartment in self.apartments) / len(self.apartments)


class Apartment:
    """An apartment property.

    Instance Attributes:
        - beds: the number of beds in the apartment.
        - bathrooms: the number of bathrooms in the apartment.
        - address: the address of the apartment.
        - price: the price of the apartment.
        - coord: the coordinate of latitude and longitude of the apartment.

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

    def __init__(self, beds: int, bathrooms: int, address: str, price: float, coord: tuple[float, float]) -> None:
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
    """A graph representation connecting apartments."""

    areas: list[Area]
    apartments: list[Apartment]

    def __init__(self) -> None:
        """Initialize an empty graph with no areas or apartments."""
        self.areas = []
        self.apartments = []

    def add_area(self, area: Area) -> None:
        """Add a neighborhood area to the graph."""
        self.areas.append(area)

    def add_apartment(self, apt: Apartment) -> None:
        """Add an apartment property to the graph."""
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
        print("Enter your preferences for apartments:")
        beds_pref = input("Number of beds (specific number or 'any'): ").strip().lower()
        baths_pref = input("Number of baths (specific number or 'any'): ").strip().lower()
        price_per_bed_pref = input(
            "Price per bed (specific number or 'any' (WITHOUT QUOTATION). Enter in the form '$'price'.0 "
            "(INCLUDE .0 ALWAYS)): ").strip().lower()

        if beds_pref.isdigit():
            beds_pref = int(beds_pref)
        else:
            beds_pref = None
        if baths_pref.isdigit():
            baths_pref = int(baths_pref)
        else:
            baths_pref = None

        if price_per_bed_pref == 'any':
            price_per_bed_pref = None
        else:
            price_per_bed_pref = price_per_bed_pref.replace('$', '')
            try:
                price_per_bed_pref = float(price_per_bed_pref)
            except ValueError:
                print("Value error")
                price_per_bed_pref = None

        neighbourhoods = load_neighbourhood_data(neighbourhood_file)
        apartments = load_apartment_data(apartment_file)

        assault_norm = (neighbourhoods['ASSAULT_RATE_2024'] - neighbourhoods['ASSAULT_RATE_2024'].min()) / \
                       (neighbourhoods['ASSAULT_RATE_2024'].max() - neighbourhoods['ASSAULT_RATE_2024'].min())

        robbery_norm = (neighbourhoods['ROBBERY_RATE_2024'] - neighbourhoods['ROBBERY_RATE_2024'].min()) / \
                       (neighbourhoods['ROBBERY_RATE_2024'].max() - neighbourhoods['ROBBERY_RATE_2024'].min())

        homicide_norm = (neighbourhoods['HOMICIDE_RATE_2024'] - neighbourhoods['HOMICIDE_RATE_2024'].min()) / \
                        (neighbourhoods['HOMICIDE_RATE_2024'].max() - neighbourhoods['HOMICIDE_RATE_2024'].min())

        neighbourhoods['crime_score'] = (0.5 * assault_norm + 0.3 * robbery_norm + 0.2 * homicide_norm
                                         )

        graph = nx.Graph()

        for _, row in neighbourhoods.iterrows():
            area = Area(
                name=row['NEIGHBOURHOOD_NAME'],
                assault_rate=row['ASSAULT_RATE_2024'],
                homicide_rate=row['HOMICIDE_RATE_2024'],
                robbery_rate=row['ROBBERY_RATE_2024'],
                coord=(row['latitude'], row['longitude'])
            )

            if area.coord is None or not all(isinstance(c, (int, float)) for c in area.coord):
                print(f"Skipping area with invalid coordinates: {area.name}")
                continue

            self.add_area(area)

            crime_score = row['crime_score']

            if crime_score < 0.3:
                color = 'green'
            elif crime_score < 0.6:
                color = 'yellow'
            else:
                color = 'red'

            graph.add_node(
                area.name,
                type="area",
                assault_rate=area.assault_rate,
                robbery_rate=area.robbery_rate,
                homicide_rate=area.homicide_rate,
                coord=area.coord,
                color=color
            )

        for _, row in apartments.iterrows():
            apartment = Apartment(
                beds=row['Bedroom'],
                bathrooms=row['Bathroom'],
                address=row['Address'],
                price=row['Price'],
                coord=(row['Lat'], row['Long'])
            )

            if apartment.coord is None or not all(isinstance(c, (int, float)) for c in apartment.coord):
                continue
            if beds_pref is not None and apartment.beds != beds_pref:
                continue
            if baths_pref is not None and apartment.bathrooms != baths_pref:
                continue
            if price_per_bed_pref is not None:
                price_per_bed = apartment.price_per_bed()
                if price_per_bed > price_per_bed_pref:
                    continue

            self.add_apartment(apartment)
            graph.add_node(
                apartment.address,
                type="apartment",
                coord=apartment.coord,
                price=apartment.price,
                bedrooms=apartment.beds,
                bathrooms=apartment.bathrooms
            )

            closest_area = self.areas[0]
            min_distance = math.sqrt(
                (apartment.coord[0] - closest_area.coord[0]) ** 2 + (apartment.coord[1] - closest_area.coord[1]) ** 2
            )
            for area in self.areas:
                distance = math.sqrt(
                    (apartment.coord[0] - area.coord[0])
                    ** 2 + (apartment.coord[1] - area.coord[1]) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_area = area

            if closest_area:
                self.add_edge(apartment, closest_area)
                graph.add_edge(apartment.address, closest_area.name, relation="located_in", distance=min_distance)

        return graph


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['typing', 'networkx', 'data_loader', 'math'],
        'allowed-io': ['build_graph'],
        'max-line-length': 120,
    })
