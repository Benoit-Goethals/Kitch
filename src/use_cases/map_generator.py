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
                total_order_lines = float(sum(ph.sales_price for ph in phase.orderlines if ph.sales_price is not None))
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

    #api for post
    async def mark_points_address(self):
        try:
            postcodes=await self.db_service.get_all_postcodes()
            data=[]
            for postcode in postcodes[:20]:
                data_post = await self.db_service.get_addresses_by_postcode(postcode)
                data += data_post[:100]



            if not data:
                raise

            markers = []
            for ad in data:
                lat = ad.latitude
                lon = ad.longitude
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
                            description=ad.street + ad.municipality,
                        )
                    )

            map_center = GeoUtil.geographic_middle_point(markers)
            m = folium.Map(location=map_center, zoom_start=12)

            #for marker in markers:
            #    folium.Marker(
            #        location=marker.point_to_lst(),
            #        popup=marker.description,
            #        tooltip=marker.summary,
            #    ).add_to(m)

            heat_data = [m.point_to_lst() for m in markers]

            heat_layer = HeatMap(heat_data, name="Heatmap Layer", radius=10)
            m.add_child(heat_layer)

            # Add LayerControl to toggle the layers on/off
            folium.LayerControl().add_to(m)

            m.save("templates/Addresses.html")
            return self.templates.TemplateResponse("Addresses.html")

        except SQLAlchemyError as e:
            raise
        except Exception as e:
            raise

    async def mark_points(self):
        body = None
        data = body.get("markers", [])
        if not data:
            raise

        markers = [Point(**marker) for marker in data]
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)
        for marker in markers:
            folium.Marker(
                location=marker.point_to_lst(),
                popup=marker.description,
                tooltip=marker.summary,
            ).add_to(m)

        m.save("templates/mark_points.html")
        return None

    async def mark_points_city_names(self, request):
        body = await request.json()
        data = body.get("markers", [])
        if not data:
            raise

        markers = []
        for marker in data:
            lat, lon = GeoUtil.get_lat_lon(marker["location"])
            if lat is not None and lon is not None:
                markers.append(
                    Point(
                        summary=marker["location"],
                        description=marker["description"],
                        x=lat,
                        y=lon,
                    )
                )

        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)
        for marker in markers:
            folium.Marker(
                location=marker.point_to_lst(),
                popup=marker.description,
                tooltip=marker.summary,
            ).add_to(m)

        m.save("templates/mark_points_from_city.html")
        return self.templates.TemplateResponse("mark_points_from_city.html", {"request": request})

    async def mark_points_layers(self):
        body = None
        data = body.get("markers", {})
        if not data:
            raise

        # Use the first list of markers to determine the center
        first = next(iter(data.items()))[1]
        markers = [Point(**marker) for marker in first]
        map_center = GeoUtil.geographic_middle_point(markers)
        m = folium.Map(location=map_center, zoom_start=12)

        # Add feature groups (layers) to the map
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
        m.save("templates/mark_points_layer.html")
        return self.templates.TemplateResponse("mark_points_layer.html")



