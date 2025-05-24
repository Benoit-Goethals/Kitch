import os
import sys
import webbrowser
from folium.plugins import HeatMap
from sqlalchemy.exc import SQLAlchemyError
import folium
from starlette.templating import Jinja2Templates
from src.database_layer.db_service import DBService
from src.utils.geo_util import GeoUtil
from src.utils.point import Point


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

COUNTRY = "België"


class MapGenerator:
    """
    Handles the generation, creation, manipulation, and visualization of geographic map data
    related to addresses, entities, and associated datasets.

    The class enables interaction with a database service to fetch necessary data, processes it
    to generate map markers, and visualizes the results using Folium, a Python mapping library.
    It supports the use of external utilities for dynamic determination of geographic coordinates
    and integration with templates for file handling.

    :ivar db_service: Reference to the database service used for data retrieval.
    :type db_service: DBService
    :ivar templates: Template handler for managing HTML templates in the "templates" directory.
    :type templates: Jinja2Templates
    """
    def __init__(self, db_service: DBService):
        self.db_service = db_service
        self.templates = Jinja2Templates(directory="templates")

    async def get_coordinates(self, address):
        """
        Asynchronously retrieves the geographic coordinates (latitude and longitude) of a given
        address. If the address does not contain pre-existing latitude and longitude information,
        the method will attempt to fetch the coordinates using an external utility.

        :param address:
            The input address containing details such as street, house number, and potentially
            latitude and longitude attributes.
        :type address: Address
        :return:
            A tuple containing the latitude and longitude of the provided address. If the
            latitude and longitude are unavailable in the input address, they are fetched dynamically.
        :rtype: tuple[float, float]
        """
        lat, lon = address.latitude, address.longitude
        if lat is None or lon is None:
            lat, lon = await GeoUtil.get_lat_lon_async(
                f"{address.street}, {address.house_number}, {COUNTRY}"
            )
        return lat, lon

    async def create_markers(self, data, get_address, get_summary, get_description, get_value=None):
        """
        Asynchronously creates a list of marker objects based on provided data and
        getter functions. For each item in the input data, the function retrieves
        the address, fetches corresponding coordinates, and constructs a marker
        object containing geographic and descriptive information.

        :param data: Iterable of input items to process.
        :type data: Iterable
        :param get_address: Function to extract an address from an individual item.
        :type get_address: Callable[[Any], str]
        :param get_summary: Function to extract a summary from an individual item.
        :type get_summary: Callable[[Any], str]
        :param get_description: Function to extract a description from an individual item.
        :type get_description: Callable[[Any], str]
        :param get_value: Optional function to extract a numeric value from an
            individual item. Defaults to None.
        :type get_value: Optional[Callable[[Any], int]]
        :return: List of marker objects containing geographic information
            (latitude, longitude), summary, description, and an optional value.
        :rtype: List[Point]
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
        Saves a given folium map to a specified file and opens it in a web browser.

        This function takes a folium map object and saves it to a specified filename
        within a templates directory. After saving, the file is opened in the default
        web browser for viewing.

        :param folium_map: The folium map object to be saved.
        :param filename: The name of the file where the map object will be saved.
        :type filename: str
        :return: None

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
        Generates a folium map showing heat data for phases in euros.

        This asynchronous method retrieves data regarding phases from the database, calculates summary
        and value properties for each phase, and generates a heatmap visualization with folium. The
        location of the markers is determined from the delivery addresses of each phase, while the
        heatmap data is based on sales price sums. The map visualization is saved as an HTML file.

        :raises Exception: If no phase data is found in the database.
        :raises SQLAlchemyError: If there is an error interacting with the database.
        :raises Exception: For any other errors during the operation.

        :return: None
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
        Marks points for all companies on a map.

        This method fetches data for all companies from the database, generates geographic
        markers based on the company's attributes such as address, summary, and description,
        and then plots these markers on a folium map.

        If no data is found, an exception is raised. The generated map is centered
        geographically using the calculated middle point of all markers. The markers are
        placed with popups and tooltips containing company-specific details.

        Errors are logged and re-raised for the caller to handle further.

        :raises Exception: Raised if no companies data is found.
        :raises SQLAlchemyError: Raised if an error occurs during database operations.
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
        Fetches, processes, and visualizes the project phases for a specific person within a defined date range.

        Retrieves project phase data for a person within the provided start and end dates. The method creates
        markers for each phase, calculates geographic middle points for marker alignment, and generates a
        folium map containing a heatmap and individual marker locations for visual representation. Generated
        map is saved and opened for further inspection.

        :param person_id: Identifier of the person whose project phases are being processed
        :type person_id: int
        :param start_date: Start date of the date range filter
        :type start_date: datetime
        :param end_date: End date of the date range filter
        :type end_date: datetime
        :return: None
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
    """
    Retrieve the full path of a file within the "templates" directory.

    This function takes a filename and constructs an absolute path to the file
    located in the "templates" folder of the current script's directory. The
    function is asynchronous, allowing its usage in coroutine-based workflows.

    :param filename: Name of the file for which the full path is to be retrieved.
    :type filename: str
    :return: The absolute path to the specified file in the "templates" directory.
    :rtype: str
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates", filename)
    return template_path