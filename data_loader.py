# === data_loader.py ===
"""
This module handles loading and preprocessing housing data from a CSV file.
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
