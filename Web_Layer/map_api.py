from flask import Flask, render_template, request, jsonify
import folium

from Web_Layer.geo_util import GeoUtil
from Web_Layer.point import Point
from database_layer.db_service import DBService


class MapAPI:

    _db_service = DBService()

    __app_flask = Flask(__name__)

    @staticmethod
    @__app_flask.route('/companies', methods=['GET'])
    async def mark_points_companies():
        data = await  MapAPI._db_service.read_all_companies()
        if not data:
            return jsonify({'error': 'No companies provided'}), 400
        markers: list[Point] = []
        for company in data:
            lat,lon=await GeoUtil.get_lat_lon_async(f"{company.address.street}, {company.address.house_number}, {company.address.city}, België")
            if lat is not None and lon is not None:
                markers.append(Point(x=lat,y=lon,summary=company.company_name,description=company.company_name))


        # Center of the map
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)
        for marker in markers:
            folium.Marker(
                location=marker.point_to_lst(),
                popup=marker.description,
                tooltip=marker.summary,
            ).add_to(m)

        m.save('templates/Companies.html')

        return render_template('Companies.html')

    @staticmethod
    @__app_flask.route('/markspoints', methods=['POST'])
    def mark_points():
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
    @__app_flask.route('/markspoints_cityname', methods=['POST'])
    def mark_points_city_names():
        data = request.json.get('markers', [])  # Expecting a list of marker dictionaries
        if not data:
            return jsonify({'error': 'No markers provided'}), 400

        markers: list[Point] = []
        for marker in data:
            lat,lon=GeoUtil.get_lat_lon(marker["location"])
            if lat is not None and lon is not None:
                markers.append(Point(summary=marker["location"],description=marker["description"],x=lat,y=lon))

        # Center of the map
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)
        for marker in markers:
            folium.Marker(
                location=marker.point_to_lst(),
                popup=marker.description,
                tooltip=marker.summary,
            ).add_to(m)

        m.save('templates/mark_points_from_city.html')

        return render_template('mark_points_from_city.html')

    @staticmethod
    @__app_flask.route('/Layers_markspoints', methods=['POST'])
    def mark_points_layers():
        # Get markers from the request JSON payload
        data = request.json.get('markers', {})  # Expecting a dictionary of marker lists keyed by layer name
        if not data:
            return jsonify({'error': 'No markers provided'}), 400

        # Center of the map (Use a default center if not calculated)
        first = next(iter(data.items()))[1]
        markers = [Point(**marker) for marker in first]
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)

        # Add layers to the map
        for layer_name, markers in data.items():
            fg = folium.FeatureGroup(name=layer_name, show=False).add_to(m)
            for marker_data in markers:
                marker = Point(**marker_data)
                folium.Marker(
                    location=marker.point_to_lst(),
                    popup=marker.description,
                    tooltip=marker.summary,
                ).add_to(fg)
        folium.LayerControl().add_to(m)
        # Save the map as an HTML template
        m.save('templates/mark_points_layer.html')

        return render_template('mark_points_layer.html')

    def run(self):
        self.__app_flask.run(debug=True)
