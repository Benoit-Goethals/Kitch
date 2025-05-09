import math
from typing import Any, Coroutine

import requests
import aiohttp
import asyncio


class GeoUtil:
    __countries = {
        "AF": "Afghanistan",
        "AL": "Albania",
        "DZ": "Algeria",
        "AD": "Andorra",
        "AO": "Angola",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BT": "Bhutan",
        "BO": "Bolivia",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BR": "Brazil",
        "BN": "Brunei",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "CV": "Cabo Verde",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CO": "Colombia",
        "KM": "Comoros",
        "CD": "Congo (DRC)",
        "CG": "Congo (Republic)",
        "CR": "Costa Rica",
        "CI": "Côte d’Ivoire",
        "HR": "Croatia",
        "CU": "Cuba",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "SZ": "Eswatini",
        "ET": "Ethiopia",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GR": "Greece",
        "GD": "Grenada",
        "GT": "Guatemala",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HN": "Honduras",
        "HU": "Hungary",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "KP": "North Korea",
        "KR": "South Korea",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Laos",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "MX": "Mexico",
        "FM": "Micronesia",
        "MD": "Moldova",
        "MC": "Monaco",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "MK": "North Macedonia",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestine",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PL": "Poland",
        "PT": "Portugal",
        "QA": "Qatar",
        "RO": "Romania",
        "RU": "Russia",
        "RW": "Rwanda",
        "KN": "Saint Kitts and Nevis",
        "LC": "Saint Lucia",
        "VC": "Saint Vincent and the Grenadines",
        "WS": "Samoa",
        "SM": "San Marino",
        "ST": "Sao Tome and Principe",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "SS": "South Sudan",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syria",
        "TW": "Taiwan",
        "TJ": "Tajikistan",
        "TZ": "Tanzania",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "United Kingdom",
        "US": "United States",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VA": "Vatican City",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe"
    }

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

        return math.degrees(lat_avg), math.degrees(lon_avg)

    @staticmethod
    def get_lat_lon(address:str)-> tuple[float, float] | tuple[None, None]:
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

    @staticmethod
    async def get_lat_lon_async(address:str)-> tuple[float, float] | tuple[None, None]:

        """Get latitude and longitude of a location using Nominatim asynchronously."""
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "YourAppNameHere"  # Nominatim requires a User-Agent
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        lat = data[0]["lat"]
                        lon = data[0]["lon"]
                        return float(lat), float(lon)
                return None, None

    @staticmethod
    def country(code: str) -> str:
        """Returns the country name for a given country code."""
        return GeoUtil.__countries.get(code.upper(), "Unknown")

    @staticmethod
    def get_country_code(country: str) -> str | None:
        """Returns the country code for a given country name."""
        return next((code for code, name in GeoUtil.__countries.items() if name.lower() == country.lower()), None)


if __name__ == "__main__":
    print(GeoUtil.get_lat_lon("Brussel, BE"))