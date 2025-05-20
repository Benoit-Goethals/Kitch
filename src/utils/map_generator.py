import os
import sys
import webbrowser

from folium.plugins import HeatMap
from sqlalchemy.exc import SQLAlchemyError
import folium
from starlette.templating import Jinja2Templates

from src.database_layer.db_service import DBService
from src.domain.DatabaseModelClasses import OrderLine
from src.Web_Layer.geo_util import GeoUtil
from src.Web_Layer.point import Point


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

COUNTRY = "België"


class MapGenerator:
    def __init__(self, db_service: DBService):
        self.db_service = db_service
        self.templates = Jinja2Templates(directory="templates")

    async def get_coordinates(self, address):
        """
        Get latitude and longitude for an address. Falls back to GeoUtil if not provided.
        """
        lat, lon = address.latitude, address.longitude
        if lat is None or lon is None:
            lat, lon = await GeoUtil.get_lat_lon_async(
                f"{address.street}, {address.house_number}, {COUNTRY}"
            )
        return lat, lon

    async def create_markers(self, data, get_address, get_summary, get_description, get_value=None):
        """
        Create a list of Point markers from the given data.
        """
        markers = []
        for item in data:
            address = get_address(item)
            lat, lon = await self.get_coordinates(address)
            if lat is not None and lon is not None:
                value = get_value(item) if get_value else 0
                markers.append(
                    Point(
                        x=lon,
                        y=lat,
                        summary=get_summary(item),
                        description=get_description(item),
                        value=value,
                    )
                )
        return markers

    async def save_and_open_map(self, folium_map, filename):
        """
        Save the map to an HTML file and open it in the default web browser.
        """
        async def get_path(filename):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "templates", filename)
            return template_path
        template_path = await get_path(filename)
        folium_map.save(template_path)
        webbrowser.open(template_path)

    async def euros_phases(self):
        """
        Generate a heatmap for euros phases.
        """
        try:
            data = await self.db_service.get_all_phases()
            if not data:
                raise Exception("No phases data found.")

            def get_address(phase): return phase.delivery_address
            def get_summary(phase): return f"{sum(ph.sales_price or 0 for ph in phase.order_lines)} euros"
            def get_description(phase): return get_summary(phase)
            def get_value(phase): return sum(ph.sales_price or 0 for ph in phase.order_lines)

            markers = await self.create_markers(data, get_address, get_summary, get_description, get_value)
            map_center = GeoUtil.geographic_middle_point(markers)
            folium_map = folium.Map(location=map_center, zoom_start=12)

            heat_data = [marker.to_points() for marker in markers]
            HeatMap(data=heat_data, radius=30, blur=10, max_zoom=2, min_opacity=0.5).add_to(folium_map)
            folium.LayerControl().add_to(folium_map)

            await self.save_and_open_map(folium_map, "euros_phases.html")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Error in euros_phases: {e}")
            raise

    async def mark_points_companies(self):
        """
        Mark companies on the map.
        """
        try:
            data = await self.db_service.get_all_companies()
            if not data:
                raise Exception("No companies data found.")

            def get_address(company): return company.address
            def get_summary(company): return company.company_name
            def get_description(company): return company.company_name

            markers = await self.create_markers(data, get_address, get_summary, get_description)
            map_center = GeoUtil.geographic_middle_point(markers)
            folium_map = folium.Map(location=map_center, zoom_start=12)

            for marker in markers:
                folium.Marker(
                    location=marker.to_points(),
                    popup=marker.description,
                    tooltip=marker.summary,
                ).add_to(folium_map)

            await self.save_and_open_map(folium_map, "Companies.html")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Error in mark_points_companies: {e}")
            raise

    async def project_phases_between_date_for_person(self, person_id, start_date, end_date):
        """
        Generate a map of project phases within a date range for a specific person.
        """
        try:
            data = await self.db_service.get_data_for_worker_between_dates(person_id, start_date, end_date)
            if not data:
                raise Exception("No project phases data found.")

            def get_address(phase): return phase.delivery_address
            def get_summary(_): return "Project Phase"
            def get_description(phase): return f"{phase.delivery_address.street}, {phase.delivery_address.municipality}"

            markers = []
            for project in data:
                markers += await self.create_markers(project.phases, get_address, get_summary, get_description)

            map_center = GeoUtil.geographic_middle_point(markers)
            folium_map = folium.Map(location=map_center, zoom_start=12)

            for marker in markers:
                folium.Marker(location=marker.to_points(), popup=marker.description).add_to(folium_map)

            heat_data = [marker.to_points() for marker in markers]
            HeatMap(data=heat_data, name="Heatmap Layer", radius=10).add_to(folium_map)
            folium.LayerControl().add_to(folium_map)

            await self.save_and_open_map(folium_map, "project_phases.html")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Error in project_phases_between_date_for_person: {e}")
            raise


async def get_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates", filename)
    return template_path