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
        [lat, lon,50],  # San Francisco

    ]
    HeatMap(data).add_to(m)
    m.save("heatmap.html")




def get_lat_lon(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "YourAppNameHere"  # Nominatim requires a user-agent
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return float(lat), float(lon)
    else:
        return None, None




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
