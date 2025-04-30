import csv
import requests
import folium
import pandas as pd
from folium.plugins import HeatMap


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


def main():
    csv_file = "kazernes.csv"
    mapped_list = []

    with open(csv_file, mode="r") as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Iterate through each row and map it to a dictionary
        for row in csv_reader:
            mapped_list.append(row)

    # Output the list to check
    print(mapped_list)
    address = "Koning Albertlaan 50, Gent, België"
    lat, lon = get_lat_lon(address)
    print(f"Latitude: {lat}, Longitude: {lon}")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    for row in mapped_list:
        address = row["Straat"] + ", " + row["Stad"] + ", België"
        print(address)
        lat, lon = get_lat_lon(address)
        if lat is not None and lon is not None:
            data2 = [lat, lon]
            folium.Marker(
                location=data2,
                popup=f"{row["Naam"]}{address}",  # Optional popup text
                tooltip="Click for info",  # Optional h
            ).add_to(m)

    m.save("kazernes.html")


if __name__ == "__main__":
    main()
