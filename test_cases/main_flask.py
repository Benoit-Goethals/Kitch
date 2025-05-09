from flask import Flask, render_template
import folium
from folium.plugins import HeatMap

app = Flask(__name__)


@app.route('/')
def index():
    # Center of the map
    map_center = [51.054342, 3.717424]  # Ghent's center coordinates
    m = folium.Map(location=map_center, zoom_start=12)

    # Layer 1: Ghent city boundaries using a GeoJSON file
    folium.GeoJson(
        "ghent_boundary.geojson",  # Replace with your GeoJSON file path for Ghent
        name="Ghent City Boundaries",
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
        [51.0551, 3.7168],  # Dummy latitude and longitude points
        [51.0513, 3.7102],
        [51.0489, 3.7302],
        [51.0593, 3.7054]
    ]
    heat_layer = HeatMap(heat_data, name="Heatmap Layer")
    m.add_child(heat_layer)

    # Add LayerControl to toggle the layers on/off
    folium.LayerControl().add_to(m)

    # Save the map to HTML

    m.save('templates/map_mul.html')

    return render_template('map_mul.html')


if __name__ == '__main__':
    app.run(debug=True)
