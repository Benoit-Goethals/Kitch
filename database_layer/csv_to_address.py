import asyncio
import csv

from database_layer.db_service import DBService
from domain.DatabaseModelClasses import Address


class DataReader:
    def __init__(self, data_source):
        """
        Initialize the DataReader with the data source.
        :param data_source: path to the CSV file.
        """
        self.data_source = data_source

    def read_as_iterator(self):
        """
        Reads the CSV file and yields rows as dictionaries one by one.
        :return: iterator yielding rows of data as dictionaries
        """
        try:
            with open(self.data_source, "r", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    yield row  # Yield each row as a dictionary
        except FileNotFoundError:
            print("Error: Data source not found.")
        except Exception as e:
            print(f"Error: {e}")


async def main():
    # Replace 'sample_data.csv' with the path to your CSV file
    data_reader = DataReader("../openaddress-bevlg.csv")
    db = DBService()
    for row in data_reader.read_as_iterator():
        # EPSG:31370_x,EPSG:31370_y,EPSG:4326_lat,EPSG:4326_lon,address_id,box_number,house_number,municipality_id,municipality_name_de,municipality_name_fr,municipality_name_nl,postcode,postname_fr,postname_nl,street_id,streetname_de,streetname_fr,streetname_nl,region_code,status
        address = Address(street=row["streetname_nl"], house_number=row["house_number"],
                          municipality=row["municipality_name_nl"], postal_code=row["postcode"], country="Be",
                          latitude=row["EPSG:4326_lat"], longitude=row["EPSG:4326_lon"])
        await db.add_address(address)

# Example usage:
if __name__ == "__main__":
    asyncio.run(main())



