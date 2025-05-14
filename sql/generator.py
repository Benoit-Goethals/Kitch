import os
from faker import Faker
import csv


def generate_persons(table_name, num_records, output_path):
    """
    Generate a single SQL insert statement for random persons and write to a file.
    """
    fake = Faker()
    titles = ["Dhr.", "Mevr.", "Dr.", "Prof."]
    values = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        title = fake.random_element(titles)
        email = fake.email()
        phone = fake.phone_number()
        values.append(
            f"('{first_name.replace("'", "''")}', '{last_name.replace("'", "''")}', '{title}', '{phone.replace("'", "''")}', '{email.replace("'", "''")}')"
        )
    sql = (
        f"INSERT INTO {table_name} (name_first, name_last, name_title, phone_number, email)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(f"Generated {num_records} SQL insert statements in {output_path}")


def generate_address(table_name, csv_path, num_records, output_path):
    """
    Generate a single SQL insert statement for addresses from the first num_records lines of a CSV file and write to a file.
    If the CSV file does not exist, create an empty one.
    Maps openaddress-bevlg.csv columns to the correct SQL fields.
    """
    if not os.path.exists(csv_path):
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(
                "streetname_nl,house_number,postcode,municipality_name_nl,EPSG:4326_lat,EPSG:4326_lon\n"
            )  # Write header only
    values = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for count, row in enumerate(reader):
            if count >= num_records:
                break
            street = row.get("streetname_nl", "").replace("'", "''")
            house_number = row.get("house_number", "").replace("'", "''")
            postal_code = row.get("postcode", "").replace("'", "''")
            municipality = row.get("municipality_name_nl", "").replace("'", "''")
            latitude = row.get("EPSG:4326_lat", "")
            longitude = row.get("EPSG:4326_lon", "")
            values.append(
                f"('{street}', '{house_number}', '{postal_code}', '{municipality}', {latitude}, {longitude})"
            )
    sql = (
        f"INSERT INTO {table_name} (street, house_number, postal_code, municipality, latitude, longitude)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(f"Generated {len(values)} SQL insert statements in {output_path}")


def main():
    table_name = "person"
    num_records = 120  # Change as needed
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_person.sql")
    generate_persons(table_name, num_records, output_file)

    table_name = "address"
    num_records = 500  # Change as needed
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "addresses", "openaddress-bevlg.csv"
    )
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_address.sql")
    generate_address(table_name, csv_path, num_records, output_file)


if __name__ == "__main__":
    main()
