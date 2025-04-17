from flask import Flask, render_template, request, jsonify
import folium

from Web_Layer.geo_util import GeoUtil
from Web_Layer.point import Point


class MapAPI:

    __app_flask = Flask(__name__)

    @staticmethod
    @__app_flask.route('/markspoints', methods=['POST'])
    def mark_points_layer():
        data = request.json.get('markers', [])  # Expecting a list of marker dictionaries
        if not data:
            return jsonify({'error': 'No markers provided'}), 400

        markers = [Point(**marker) for marker in data]

        # Center of the map
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)
        for marker in markers:
            folium.Marker(
                location=marker.point_to_lst(),
                popup=marker.description,
                tooltip=marker.summary,
            ).add_to(m)

        m.save('templates/mark_points.html')

        return render_template('mark_points.html')

    @staticmethod
    @__app_flask.route('/Layers_markspoints', methods=['POST'])
    def mark_points():
        # Get markers from the request JSON payload
        data = request.json.get('markers', {})  # Expecting a dictionary of marker lists keyed by layer name
        if not data:
            return jsonify({'error': 'No markers provided'}), 400

        # Center of the map (Use a default center if not calculated)
        map_center = [51.054342, 3.717424]  # Ghent's center coordinates
        m = folium.Map(location=map_center, zoom_start=12)

        # Add layers to the map
        for layer_name, markers in data.items():
            for marker_data in markers:
                marker = Point(**marker_data)
                folium.Marker(
                    location=marker.point_to_lst(),
                    popup=marker.description,
                    tooltip=marker.summary,
                ).add_to(m)

        # Save the map as an HTML template
        m.save('templates/mark_points_layer.html')

        return render_template('mark_points_layer.html')

    def run(self):
        self.__app_flask.run(debug=True)
