import asyncio

from database_layer.db_service import DBService
from domain.DatabaseModelClasses import Person, Address

TITLE_PERSONS = "Persons"
TITLE_COMPANIES = "Companies"
TITLE_ADDRESSES = "Address"
TITLE_ASSIGNMENTS = "Assignments"
MSG_NO_RESULTS = "No {} found."

async def fetch_and_print(db_service, fetch_function, title):
    """
    Utility function to fetch data using a DBService function and print the results.
    """
    results = await fetch_function()
    if results is None:
        print(MSG_NO_RESULTS.format(title.lower()))
        return
    print(title + ":")
    for result in results:
        print(result)

async def main():
    db_service = DBService()
    #await fetch_and_print(db_service, db_service.read_all_persons_with_address, TITLE_PERSONS)
    #await fetch_and_print(db_service, db_service.read_all_persons, TITLE_PERSONS)
    #await fetch_and_print(db_service, db_service.read_all_companies, TITLE_COMPANIES)
    #await fetch_and_print(db_service, db_service.read_all_address, TITLE_ADDRESSES)
    #await fetch_and_print(db_service, db_service.read_all_assignment, TITLE_ASSIGNMENTS)

    new_person=Person(name_first="John", name_last="Doe", email="jo@be.be", phone_number="0123456789")
    new_person.address=Address(street="non 1",country="be",postal_code="9000",municipality="Gent",house_number="20")
    await db_service.add_person(new_person)


    # Create an Address instance
    address = Address(
        street="Main Street",
        house_number="123",
        postal_code="1000",
        municipality="Brussels",
        country="Belgium"
    )

    # Create a Person instance
    person = Person(
        name_first="John",
        name_last="Doe",
        email="johndoe@example.com",
        phone_number="1234567890",

    )
    person.address = address

    # Pass the Person instance to add_person
    await db_service.add_person(person)




if __name__ == "__main__":
    asyncio.run(main())