import math

import requests


class GeoUtil:

    @staticmethod
    def geographic_middle_point(coords):
        if not coords:
            return None

        x_total = y_total = z_total = 0.0

        for coord in coords:
            lat=coord.x
            lon=coord.y
            lat_rad = math.radians(lat)
            lon_rad = math.radians(lon)

            x_total += math.cos(lat_rad) * math.cos(lon_rad)
            y_total += math.cos(lat_rad) * math.sin(lon_rad)
            z_total += math.sin(lat_rad)

        total = len(coords)
        x_avg = x_total / total
        y_avg = y_total / total
        z_avg = z_total / total

        lon_avg = math.atan2(y_avg, x_avg)
        hyp = math.sqrt(x_avg * x_avg + y_avg * y_avg)
        lat_avg = math.atan2(z_avg, hyp)

        return (math.degrees(lat_avg), math.degrees(lon_avg))

    @staticmethod
    def get_lat_lon(address):
        """Get latitude and longitude of a location using Nominatim."""
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "YourAppNameHere"  # Nominatim requires a User-Agent
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return float(lat), float(lon)
        return None, None