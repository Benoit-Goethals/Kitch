import os
from faker import Faker
import csv


def insert_into_address(table_name, csv_path, num_records, output_path):
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


def insert_into_person(table_name, num_records, output_path):
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


def insert_into_mapper(table_name, person_ids, output_path, role_name):
    values = [f"({pid})" for pid in person_ids]
    sql = (
        f"INSERT INTO {table_name} (person_id)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(
        f"Generated {len(person_ids)} SQL insert statements in {output_path} for {role_name}"
    )


def insert_into_employee(table_name, person_ids, output_path):
    insert_into_mapper(table_name, person_ids, output_path, "employee")


def insert_into_worker(table_name, person_ids, output_path):
    insert_into_mapper(table_name, person_ids, output_path, "worker")


def insert_into_company(table_name, person_ids, output_path):
    fake = Faker()
    values = []
    for i, pid in enumerate(person_ids, start=1):
        tax_number = fake.unique.random_number(digits=9, fix_len=True)
        address_id = i
        company_name = f"Client {chr(64 + i)}"
        values.append(f"('{tax_number}', {address_id}, '{company_name}', {pid})")
    sql = (
        f"INSERT INTO {table_name} (tax_number, address_id, company_name, contactperson_id)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(
        f"Generated {len(person_ids)} SQL insert statements in {output_path} for company"
    )


def insert_into_client():
    table_name = "client"
    company_ids = list(range(1, 81))
    values = [f"({cid})" for cid in company_ids]
    sql = (
        f"INSERT INTO {table_name} (company_id)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    output_path = os.path.join(os.path.dirname(__file__), "insert_into_client.sql")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(
        f"Generated {len(company_ids)} SQL insert statements in {output_path} for client"
    )


def insert_into_supplier():
    table_name = "supplier"
    company_ids = list(range(81, 101))
    values = [f"({cid})" for cid in company_ids]
    sql = (
        f"INSERT INTO {table_name} (company_id)\nVALUES\n    "
        + ",\n    ".join(values)
        + ";"
    )
    output_path = os.path.join(os.path.dirname(__file__), "insert_into_supplier.sql")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sql + "\n")
    print(
        f"Generated {len(company_ids)} SQL insert statements in {output_path} for supplier"
    )


def insert_into_article():
    pass


def insert_into_project():
    pass


def insert_into_phase():
    pass


def insert_into_orderline():
    pass


def insert_into_assignment():
    pass


def main():
    # PERSON
    table_name = "person"
    num_records = 120  # Change as needed
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_person.sql")
    insert_into_person(table_name, num_records, output_file)

    # ADDRESS
    table_name = "address"
    num_records = 500  # Change as needed
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "addresses", "openaddress-bevlg.csv"
    )
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_address.sql")
    insert_into_address(table_name, csv_path, num_records, output_file)

    # EMPLOYEE
    table_name = "employee"
    person_ids = list(range(101, 111))
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_employee.sql")
    insert_into_employee(
        table_name,
        person_ids,
        output_file,
    )

    # WORKER
    table_name = "worker"
    person_ids = list(range(111, 121))
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_worker.sql")
    insert_into_worker(
        table_name,
        person_ids,
        output_file,
    )

    # COMPANY
    table_name = "company"
    person_ids = list(range(1, 101))
    output_file = os.path.join(os.path.dirname(__file__), "insert_into_company.sql")
    insert_into_company(
        table_name,
        person_ids,
        output_file,
    )

    # CLIENT
    insert_into_client()

    # SUPPLIER
    insert_into_supplier()


if __name__ == "__main__":
    main()
