import webbrowser
import folium
from folium.plugins import HeatMap
from folium import PolyLine
from folium.plugins import AntPath


def main():
    # Center of the map
    map_center = [51.054342, 3.717424]  # Ghent's center coordinates
    m = folium.Map(location=map_center, zoom_start=12)
    print("hi")

    # Route Layer: Example route using PolyLine with arrows
    route_points = [
        [51.0551, 3.7168],  # Dummy latitude and longitude points
        [51.0513, 3.7102],
        [51.0489, 3.7302],
        [51.0593, 3.7054],
    ]

    # Add a PolyLine with arrows to connect the points
    polyline = PolyLine(
        locations=route_points,
        color="blue",
        weight=5,
        opacity=0.8,
        tooltip="Route with arrows",
    )
    m.add_child(polyline)

    # Add arrows to the PolyLine

    ant_path = AntPath(
        locations=route_points,
        color="blue",
        weight=5,
        delay=1000,
    )
    m.add_child(ant_path)

    # Add LayerControl to toggle the layers on/off
    folium.LayerControl().add_to(m)

    # Save the map to HTML
    m.save("map_with_routes.html")
    print("Map with routes saved as 'map_with_routes.html'")


if __name__ == "__main__":
    main()
    webbrowser.open("map_with_routes.html")
    # Open the generated HTML file in the default web browser
