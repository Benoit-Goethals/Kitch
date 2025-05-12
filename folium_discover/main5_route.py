import webbrowser
import folium
from folium.plugins import HeatMap
from folium import PolyLine
from folium.plugins import AntPath
import random


def main():
    # Center of the map
    map_center = [51.054342, 3.717424]  # Ghent's center coordinates
    m = folium.Map(location=map_center, zoom_start=12)
    print("hi")

    # Route Layer: Example route using PolyLine with arrows
    # Generate 50 random points in Belgium
    belgium_bounds = {
        "north": 51.5,  # Northernmost latitude
        "south": 49.5,  # Southernmost latitude
        "east": 6.4,    # Easternmost longitude
        "west": 2.5     # Westernmost longitude
    }

    points = [
        [
            random.uniform(belgium_bounds["south"], belgium_bounds["north"]),
            random.uniform(belgium_bounds["west"], belgium_bounds["east"])
        ]
        for _ in range(50)
    ]

    # Add the points to the map
    for idx, point in enumerate(points, start=1):
        folium.Marker(
            location=point,
            tooltip=f"Point {idx}: {point}",
            popup=f"<b>Point {idx}</b><br>Coordinates: {point}<br><a href='https://www.google.com/maps?q={point[0]},{point[1]}' target='_blank'>Open in Google Maps</a>"
        ).add_to(m)

    # Select 10 random points to form a route
    route_points = random.sample(points, 10)

    route_points = [
        [51.0593, 3.7054],
        [51.0551, 3.7168],  # Dummy latitude and longitude points
        [51.0513, 3.7102],
        [51.0489, 3.7302],
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

    ant_path = AntPath(
        locations=route_points,
        color="blue",
        weight=5,
        delay=1000,
    )

    # Replace markers with circular markers having random colors and diameters
    for idx, point in enumerate(points, start=1):
        random_color = random.choice(colors)  # Pick a random color
        random_diameter = random.randint(5, 20)  # Generate a random diameter
        folium.CircleMarker(
            location=point,
            radius=random_diameter,  # Use the random diameter
            color=random_color,
            fill=True,
            fill_color=random_color,
            fill_opacity=0.6,
            tooltip=f"Point {idx}: {point}, Diameter: {random_diameter}",
            popup=f"<b>Point {idx}</b><br>Coordinates: {point}<br>Diameter: {random_diameter}<br><a href='https://www.google.com/maps?q={point[0]},{point[1]}' target='_blank'>Open in Google Maps</a>"
        ).add_to(m)
    m.add_child(ant_path)

    # Add fake numbers as radius for each circle
    fake_radii = [10, 15, 20, 25]  # Example fake numbers for radius
    colors = ["red", "blue", "green", "purple", "orange", "yellow"]  # List of random colors

    for idx, (point, radius) in enumerate(zip(route_points, fake_radii), start=1):
        random_color = random.choice(colors)  # Pick a random color
        folium.CircleMarker(
            location=point,
            radius=radius,  # Use the fake number as the radius
            color=random_color,
            fill=True,
            fill_color=random_color,
            fill_opacity=0.2,
            tooltip=f"Point {idx}: {point}, Radius: {radius}",
            popup=f"<b>Point {idx}</b><br>Coordinates: {point}<br>Radius: {radius}<br><a href='https://www.google.com/maps?q={point[0]},{point[1]}' target='_blank'>Open in Google Maps</a>"
        ).add_to(m)

        # Generate a Google Maps URL with the route points
        base_url = "https://www.google.be/maps/dir/"
        coords_path = "/".join([f"{lat},{lon}" for lat, lon in route_points])
        google_maps_url = f"{base_url}{coords_path}/@{route_points[0][0]},{route_points[0][1]},14z/data=!4m2!4m1!3e0?entry=ttu&g_ep=EgoyMDI1MDUwNy4wIKXMDSoASAFQAw%3D%3D"

        # Add a clickable link to the polyline
        polyline.add_child(folium.Popup(f"<a href='{google_maps_url}' target='_blank'>Open Route in Google Maps</a>"))

    # Add LayerControl to toggle the layers on/off
    folium.LayerControl().add_to(m)

    # Save the map to HTML
    m.save("map_with_routes.html")
    print("Map with routes saved as 'map_with_routes.html'")


if __name__ == "__main__":
    main()
    webbrowser.open("map_with_routes.html")
    # Open the generated HTML file in the default web browser
