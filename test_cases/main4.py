import folium
from folium.plugins import HeatMap


def main():
    # Center of the map
    map_center = [51.054342, 3.717424]  # Ghent's center coordinates
    m = folium.Map(location=map_center, zoom_start=12)
    print("hi")

    # Layer 1: Ghent city boundaries using a GeoJSON file
    folium.GeoJson(
        "ghent_boundary.geojson",  # Replace with your GeoJSON file path for Ghent
        name="Ghent City Boundaries today",
        style_function=lambda x: {
            'fillColor': 'blue',
            'color': 'navy',
            'weight': 2,
            'fillOpacity': 0.4
        }
    ).add_to(m)

    # Layer 2: Example second city boundaries (use another GeoJSON file)
    folium.GeoJson(
        "nearby_boundaries.geojson",  # Replace with your GeoJSON file path for another area
        name="Nearby City Boundaries",
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'darkgreen',
            'weight': 2,
            'fillOpacity': 0.4
        }
    ).add_to(m)

    # Layer 3: Heatmap (example with dummy data)
    heat_data = [
        [51.0551, 3.7168,100],  # Dummy latitude and longitude points
        [51.0513, 3.7102,200],
        [51.0489, 3.7302,5000],
        [51.0593, 3.7054,50]
    ]
    heat_layer = HeatMap(heat_data, name="Heatmap Layer",radius=10)
    m.add_child(heat_layer)

    # Add LayerControl to toggle the layers on/off
    folium.LayerControl().add_to(m)

    # Save the map to HTML
    m.save("map_with_multiple_layers.html")
    print("Map with multiple layers saved as 'map_with_multiple_layers.html'")


if __name__ == '__main__':
    main()
