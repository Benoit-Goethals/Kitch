import asyncio
import time  # Import the time module for measuring the execution time

from database_layer.db_service import DBService
from domain.DatabaseModelClasses import Person, Address

TITLE_PERSONS = "Persons"
TITLE_COMPANIES = "Companies"
TITLE_ADDRESSES = "Address"
TITLE_PROJECTS = "Projects"
MSG_NO_RESULTS = "No {} found."

async def fetch_and_print(db_service, fetch_function, title):
    """
    Utility function to fetch data using a DBService function and print the results.
    """
    
    start_time = time.perf_counter()  # Start the timer
    results = await fetch_function()  # Await the fetch operation
    elapsed_time = time.perf_counter() - start_time  # Calculate elapsed time

    if results is None:
        print(MSG_NO_RESULTS.format(title.lower()))
        return
    
    print(title + ":")
    for result in results:
        print(result)
    
    # Print the elapsed time
    print(f"Execution time for {title}: {elapsed_time:.4f} seconds")

async def main():
    db_service = DBService()
    # Timing for fetching projects, as an example

    await fetch_and_print(db_service, db_service.get_all_persons_with_address, TITLE_PERSONS)
    await fetch_and_print(db_service, db_service.get_all_projects, TITLE_PROJECTS)
    await fetch_and_print(db_service, db_service.get_all_persons_with_address, TITLE_PERSONS)
    await fetch_and_print(db_service, db_service.get_all_companies, TITLE_COMPANIES)
    await fetch_and_print(db_service, db_service.get_all_addresses, TITLE_ADDRESSES)


if __name__ == "__main__":
    asyncio.run(main())