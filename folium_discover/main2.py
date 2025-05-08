import webbrowser
import requests
import folium


def main():
    # City name and coordinates (center of Ghent)
    city_name = "Ghent, België"
    lat, lon = get_lat_lon(city_name)

    if lat and lon:
        # Create a map centered around Ghent
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Path to the local GeoJSON file
        geojson_file = "ghent_boundary.geojson"  # Replace with your file path

        # Add GeoJSON layer to the map to display the city borders
        folium.GeoJson(
            geojson_file,
            name="City Borders",
            style_function=lambda x: {
                "fillColor": "blue",
                "color": "black",
                "weight": 2,
                "fillOpacity": 0.2,
            },
        ).add_to(m)

        # Add a marker for the city center
        folium.Marker(location=[lat, lon], popup=city_name, tooltip=city_name).add_to(m)

        # Save to an HTML file
        m.save("city_borders.html")
    else:
        print("Failed to fetch city center coordinates.")


def get_lat_lon(address):
    """Get latitude and longitude of a location using Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "YourAppNameHere"}  # Nominatim requires a User-Agent

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return float(lat), float(lon)
    return None, None


if __name__ == "__main__":
    main()
    webbrowser.open("city_borders.html")
    # Open the generated HTML file in the default web browser
