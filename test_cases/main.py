import requests
import folium
import pandas as pd
from folium.plugins import HeatMap


def main():
    # Example usage
    address = "Koning Albertlaan 50, Gent, België"
    lat, lon = get_lat_lon(address)
    print(f"Latitude: {lat}, Longitude: {lon}")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    data = [
        [lat, lon, 50],  # San Francisco
    ]

    lat, lon = get_lat_lon("Sportpleinstraat 14, Dendermonde, België")
    data2 = [lat, lon]

    folium.Marker(
        location=data2,
        popup="Koning Albertlaan 50, Gent, België",  # Optional popup text
        tooltip="Click for info",  # Optional h
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],  # Center of the circle
        radius=10000,  # Radius in meters
        color="blue",  # Circle border color
        fill=True,  # Fill the circle
        fill_color="blue",  # Fill color
        fill_opacity=0.4,  # Fill opacity
    ).add_to(m)

    HeatMap(data).add_to(m)

    m.save("heatmap.html")


def get_lat_lon(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "YourAppNameHere"}  # Nominatim requires a user-agent

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return float(lat), float(lon)
    else:
        return None, None


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
