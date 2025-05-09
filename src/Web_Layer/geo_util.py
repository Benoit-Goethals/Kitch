import math
from typing import List, NamedTuple, Tuple

class Coordinate(NamedTuple):
    x: float  # latitude in degrees
    y: float  # longitude in degrees

class GeoUtil:
    @staticmethod
    def geographic_middle_point(coords: List[Coordinate]) -> Tuple[float, float] | None:
        if not coords:
            # Better default error signaling
            return None

        x_total = y_total = z_total = 0.0
        for coord in coords:
            if not hasattr(coord, 'x') or not hasattr(coord, 'y'):
                raise ValueError("Each coordinate must have 'x' and 'y' attributes representing lat/lon.")
            
            # Ensure the inputs are in degrees
            lat = coord.x
            lon = coord.y

            # Convert to radians
            lat_rad = math.radians(lat)
            lon_rad = math.radians(lon)

            # Accumulate Cartesian coordinates
            x_total += math.cos(lat_rad) * math.cos(lon_rad)
            y_total += math.cos(lat_rad) * math.sin(lon_rad)
            z_total += math.sin(lat_rad)

        # Calculate average XYZ Cartesian coordinates
        total = len(coords)
        if total == 0:
            return None  # Extra guard against division by zero

        x_avg = x_total / total
        y_avg = y_total / total
        z_avg = z_total / total

        # Convert back to spherical coordinates
        lon_avg = math.atan2(y_avg, x_avg)
        hyp = math.sqrt(x_avg * x_avg + y_avg * y_avg)
        lat_avg = math.atan2(z_avg, hyp)

        # Return result in degrees
        return math.degrees(lat_avg), math.degrees(lon_avg)