# === main.py ===
"""
This is the entry point for the Toronto Housing Graph program.
"""
from data_loader import load_and_clean_data, get_coordinates
from graph_builder import Apartment, Area, build_graph
from visualizer import draw_graph


def main() -> None:
    df = load_and_clean_data('toronto_apartments.csv')

    # Manually define a few example areas (in a real project you’d automate this)
    neighborhoods = {
        'Downtown': (43.654, -79.388),
        'Midtown': (43.705, -79.399),
        'Liberty Village': (43.637, -79.423)
    }

    coords = get_coordinates(df['address'].tolist())

    areas = [Area(name, coord) for name, coord in neighborhoods.items()]

    for _, row in df.iterrows():
        address = row['address']
        if address in coords:
            apt = Apartment(address, row['price'], coords[address])
            # Assign to closest area by distance
            closest_area = min(areas, key=lambda a: geodesic(a.coord, apt.coord).km)
            closest_area.add_apartment(apt)

    G = build_graph(areas)
    draw_graph(G)


if __name__ == '__main__':
    main()
