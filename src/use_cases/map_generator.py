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


async def get_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates", filename)
    return template_path


class MapGenerator:
    def __init__(self, db_service: DBService):
        self.db_service=db_service
        self.templates = Jinja2Templates(directory="templates")

    async def euros_phases(self):

        try:
            data = await self.db_service.get_all_phases()
            if not data:
               raise

            markers = []
            total = 0
            for phase in data:
                total_order_lines = float(sum(ph.sales_price for ph in phase.order_lines if ph.sales_price is not None))
                if total_order_lines > total:
                    total = total_order_lines

                lat = phase.delivery_address.latitude
                lon = phase.delivery_address.longitude
                if lat is None or lon is None:
                    lat, lon = await GeoUtil.get_lat_lon_async(
                        f"{phase.delivery_address.street}, {phase.delivery_address.house_number},  België"
                    )
                if lat is not None and lon is not None:
                    markers.append(
                        Point(
                            x=lat,
                            y=lon,
                            summary=str(total_order_lines) + " euros",
                            description=str(total_order_lines) + " euros",
                            value=total_order_lines,

                        )
                    )

            map_center = GeoUtil.geographic_middle_point(markers)
            m = folium.Map(location=map_center, zoom_start=12)

            heat_data = [m.to_points() for m in markers]

            HeatMap(
                data=heat_data,  # Data in formaat [lat, lon, waarde]
                radius=30,  # Radius van een punt
                blur=10,  # Wazigheid van de heatmap
                max_zoom=2,  # Maximale zoom
                min_opacity=0.5,  # Minimale opaciteit

            ).add_to(m)

            # Add LayerControl to toggle the layers on/off
            folium.LayerControl().add_to(m)
            template_path = await get_path("euros_phases.html")
            m.save(template_path)
            print(template_path)
            webbrowser.open(template_path)


        except SQLAlchemyError as e:
            raise
        except Exception as e:
            raise



    async def mark_points_companies(self):
        try:
            data = await self.db_service.get_all_companies()
            if not data:
                raise

            markers = []
            for company in data:
                lat = company.address.latitude
                lon = company.address.longitude
                if lat is None or lon is None:
                    lat, lon = await GeoUtil.get_lat_lon_async(
                        f"{company.address.street}, {company.address.house_number},  België"
                    )
                if lat is not None and lon is not None:
                    markers.append(
                        Point(
                            x=lat,
                            y=lon,
                            summary=company.company_name,
                            description=company.company_name,
                        )
                    )

            map_center = GeoUtil.geographic_middle_point(markers)
            m = folium.Map(location=map_center, zoom_start=12)
            for marker in markers:
                folium.Marker(
                    location=marker.to_points(),
                    popup=marker.description,
                    tooltip=marker.summary,
                ).add_to(m)

            template_path = await get_path("Companies.html")
            m.save(template_path)
            webbrowser.open(template_path)

        except SQLAlchemyError as e:
            raise
        except Exception as e:
            raise


    async def project_phases_between_date_for_person(self, person_id, start_date, end_date):
        data = await self.db_service.get_data_for_worker_between_dates(person_id, start_date, end_date)
        if not  data:
            return None
        markers = []
        for pr in data:
            for ad in pr.phases:
                lat = ad.delivery_address.latitude
                lon = ad.delivery_address.longitude
                if lat is None or lon is None:
                    lat, lon = await GeoUtil.get_lat_lon_async(
                        f"{ad.street}, {ad.house_number},  België"
                    )
                if lat is not None and lon is not None:
                    markers.append(
                        Point(
                            x=lat,
                            y=lon,
                            summary=ad,
                            description=ad.delivery_address.street + ad.delivery_address.municipality,
                        )
                    )
            map_center = GeoUtil.geographic_middle_point(markers)
            m = folium.Map(location=map_center, zoom_start=12)

            for marker in markers:
                folium.Marker(
                    location=marker.to_points(),
                    popup=marker.description,

                ).add_to(m)

            heat_data = [m.to_points() for m in markers]

            heat_layer = HeatMap(heat_data, name="Heatmap Layer", radius=10)
            m.add_child(heat_layer)

        # Add LayerControl to toggle the layers on/off
        folium.LayerControl().add_to(m)

        template_path = await get_path("euros_phases.html")
        m.save(template_path)
        print(template_path)
        webbrowser.open(template_path)



