# === data_loader.py ===
"""
This module handles loading and preprocessing housing and neighborhood data from CSV files.
"""
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def load_and_clean_data(csv_file: str) -> pd.DataFrame:
    """
    Load and clean the housing dataset.
    """
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['address', 'price'])
    # Clean the price column by removing non-numeric characters
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    return df


def get_coordinates(addresses: list[str]) -> dict[str, tuple[float, float]]:
    """
    Get latitude and longitude for a list of addresses.
    """
    geolocator = Nominatim(user_agent="csc111-housing")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    coords = {}
    for address in addresses:
        try:
            location = geocode(address)
            if location:
                coords[address] = (location.latitude, location.longitude)
            else:
                print(f"Geocoding failed for address: {address}")
        except Exception as e:
            print(f"Error geocoding address {address}: {e}")
    return coords


def load_neighbourhood_data(csv_file: str) -> pd.DataFrame:
    """
    Load and preprocess the neighborhood crime rates dataset.
    """
    df = pd.read_csv(csv_file)
    # Ensure required columns are present
    required_columns = ['NEIGHBOURHOOD_NAME', 'ASSAULT_RATE_2024', 'HOMICIDE_RATE_2024', 'ROBBERY_RATE_2024']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Add latitude and longitude columns if they are missing
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        geolocator = Nominatim(user_agent="csc111-housing")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        def get_coords(neighbourhood_name):
            location = geocode(neighbourhood_name)
            if location:
                return location.latitude, location.longitude
            else:
                print(f"Geocoding failed for neighborhood: {neighbourhood_name}")
                return None, None

        df['latitude'], df['longitude'] = zip(*df['NEIGHBOURHOOD_NAME'].apply(get_coords))

    return df


def load_apartment_data(csv_file: str) -> pd.DataFrame:
    """
    Load and preprocess the apartment prices dataset.
    """
    df = pd.read_csv(csv_file, names=['bedrooms', 'bathrooms', 'address', 'latitude', 'longitude', 'price'])
    # Ensure required columns are present
    required_columns = ['bedrooms', 'bathrooms', 'address', 'latitude', 'longitude', 'price']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Clean the price column by removing non-numeric characters
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    return df
