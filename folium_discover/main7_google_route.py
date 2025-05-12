import webbrowser
import folium
from folium.plugins import AntPath
import random

def generate_google_maps_url(coords):
    """
    Generates a Google Maps URL for directions based on a list of coordinates.

    Args:
        coords (list of tuples): A list of (latitude, longitude) tuples.

    Returns:
        str: A Google Maps URL for the given coordinates.
    """
    base_url = "https://www.google.be/maps/dir/"
    coord_strings = [f"{lat},{lon}" for lat, lon in coords]
    return base_url + "/".join(coord_strings)

def main():
    # Example coordinates in Belgium
    coords = [
        (51.35115, 4.45248), 
        (51.22303, 4.42761),  
        (51.18409, 4.35690),  
        (51.18499, 4.16375),  
        (51.04856, 3.75008)   
    ]



    # Generate Google Maps URL
    google_maps_url = generate_google_maps_url(coords)
    print("Google Maps URL:", google_maps_url)

    # Create a Folium map
    m = folium.Map(location=coords[0], zoom_start=8)

    # Add markers with URLs
    for coord in coords:
        folium.Marker(
            location=coord,
            popup=f'<a href="{google_maps_url}" target="_blank">Route in Google Maps</a>'
        ).add_to(m)

    # Add AntPath
    AntPath(coords).add_to(m)

    # Save the map to an HTML file
    m.save("main5_routes.html")


if __name__ == "__main__":
    main()
    webbrowser.open("main5_routes.html")