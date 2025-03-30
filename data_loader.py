# === data_loader.py ===
"""
This module handles loading and preprocessing housing and neighborhood data from CSV files.
"""
import pandas as pd
import googlemaps


def get_coordinates(addresses: list[str]) -> dict[str, tuple[float, float]]:
    """
    Get latitude and longitude for a list of addresses, with optional city and country context.
    """

    gmaps = googlemaps.Client(key="AIzaSyCBsh-FGuizrdf88wvfOE5Tm7UZFQkIqWM")
    coords = {}
    for address in addresses:
        result = gmaps.geocode(f"{address}, Toronto, ON")
        if result:
            location = result[0]['geometry']['location']
            coords[address] = (location['lat'], location['lng'])

    return coords


def load_neighbourhood_data(csv_file: str) -> pd.DataFrame:
    """
    Load and preprocess the neighborhood crime rates dataset.
    """
    df = pd.read_csv(csv_file)

    coords = get_coordinates(df['NEIGHBOURHOOD_NAME'].tolist())
    df['latitude'] = df['NEIGHBOURHOOD_NAME'].map(lambda name: coords.get(name, (None, None))[0])
    df['longitude'] = df['NEIGHBOURHOOD_NAME'].map(lambda name: coords.get(name, (None, None))[1])

    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    df = df.dropna(subset=['latitude', 'longitude'])

    return df


def load_apartment_data(csv_file: str) -> pd.DataFrame:
    """
    Load and preprocess the apartment prices dataset.
    """
    df = pd.read_csv(csv_file)

    # Filter rows where the 'Address' contains 'Toronto'
    df = df[df['Address'].str.lower().str.contains('toronto', na=False)]

    # Ensure the 'Price' column is treated as strings before applying string operations
    df['Price'] = df['Price'].astype(str)  # Convert to string
    df['Price'] = (
        df['Price']
        .str.replace('$', '', regex=False)  # Remove dollar signs
        .str.replace(',', '', regex=False)  # Remove commas
    )

    # Convert the 'Price' column to float, handling any invalid values
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Drop rows with invalid or missing prices
    df = df.dropna(subset=['Price'])

    return df