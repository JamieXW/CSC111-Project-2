# === data_loader.py ===
"""
This module handles loading and preprocessing apartment and neighborhood data from CSV files.
"""
import pandas as pd
import googlemaps


def get_coordinates(addresses: list[str]) -> dict[str, tuple[float, float]]:
    """
    Get latitude and longitude for a list of addresses, with optional city and country context.
    """

    gmaps = googlemaps.Client(key="AIzaSyBjzPu6iM6AJmyIQvRY5PRFSjthClZtyUE")
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

    df = df[df['Address'].str.lower().str.contains('toronto', na=False)]

    df['Bedroom'] = pd.to_numeric(df['Bedroom'], errors='coerce')
    df['Bathroom'] = pd.to_numeric(df['Bathroom'], errors='coerce')

    df['Price'] = df['Price'].astype(str)
    df['Price'] = (
        df['Price']
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
    )

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    df = df.dropna(subset=['Price'])

    return df


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'googlemaps'],
        'allowed-io': [],
        'max-line-length': 120,
    })
