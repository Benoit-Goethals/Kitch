from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
import folium
from Web_Layer.geo_util import GeoUtil
from Web_Layer.point import Point
from database_layer.db_service import DBService


class RestFastAPI:
    def __init__(self):
        self.app = FastAPI()
        self.db_service = DBService()
        self.templates = Jinja2Templates(directory="templates")

        # Routesb
        self.app.get("/", response_class=HTMLResponse)(self.index)
        self.app.get("/companies", response_class=HTMLResponse)(self.mark_points_companies)
        self.app.post("/markspoints", response_class=HTMLResponse)(self.mark_points)
        self.app.post("/markspoints_cityname", response_class=HTMLResponse)(self.mark_points_city_names)
        self.app.post("/Layers_markspoints", response_class=HTMLResponse)(self.mark_points_layers)

    async def index(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def mark_points_companies(self, request: Request):
        try:
            data = await self.db_service.read_all_companies()
            if not data:
                raise HTTPException(status_code=400, detail="No companies provided")

            markers = []
            for company in data:
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
                    location=marker.point_to_lst(),
                    popup=marker.description,
                    tooltip=marker.summary,
                ).add_to(m)

            m.save("templates/Companies.html")
            return self.templates.TemplateResponse("Companies.html", {"request": request})

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    async def mark_points(self, request: Request):
        body = await request.json()
        data = body.get("markers", [])
        if not data:
            raise HTTPException(status_code=400, detail="No markers provided")

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
        return self.templates.TemplateResponse("mark_points.html", {"request": request})

    async def mark_points_city_names(self, request: Request):
        body = await request.json()
        data = body.get("markers", [])
        if not data:
            raise HTTPException(status_code=400, detail="No markers provided")

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

    async def mark_points_layers(self, request: Request):
        body = await request.json()
        data = body.get("markers", {})
        if not data:
            raise HTTPException(status_code=400, detail="No markers provided")

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
        return self.templates.TemplateResponse("mark_points_layer.html", {"request": request})



if __name__ == "__main__":
    import uvicorn

    app = RestFastAPI().app  # Initialize the RestFastAPI class and access its app instance
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
