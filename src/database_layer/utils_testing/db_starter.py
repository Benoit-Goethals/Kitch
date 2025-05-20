import asyncio
import datetime
import time  # Import the time module for measuring the execution time

import pandas as pd

from domain.person_type import PersonType
from src.database_layer.db_service import DBService

TITLE_PERSONS = "Persons"
TITLE_COMPANIES = "Companies"
TITLE_ADDRESSES = "Address"
TITLE_PROJECTS = "Projects"
TITLE_PROJECTS_PHASES = "Project_Phases"
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
    df = pd.DataFrame(results)
    for result in results:
        print(result)
    
    # Print the elapsed time
    print(f"Execution time for {title}: {elapsed_time:.4f} seconds")

async def main():
    db_service = DBService()
    # Timing for fetching projects, as an example
    """
    await fetch_and_print(db_service, db_service.get_all_projects, TITLE_PROJECTS)
    await fetch_and_print(db_service, db_service.get_all_persons_with_address, TITLE_PERSONS)

    await fetch_and_print(
        db_service,
        lambda: db_service.get_data_for_worker_between_dates(120, datetime.date(1990, 1, 1), datetime.date(2026, 1, 1)),
        "date"
    )


    await fetch_and_print(db_service, db_service.get_all_projects_phases, TITLE_PROJECTS_PHASES)
    await fetch_and_print(db_service, db_service.get_all_persons_with_address, TITLE_PERSONS)
    await fetch_and_print(db_service, db_service.get_all_companies, TITLE_COMPANIES)
    await fetch_and_print(db_service, db_service.get_all_addresses, TITLE_ADDRESSES)
    await fetch_and_print(db_service, lambda:db_service.get_all_projects_phases_year("2023"), "project_phases_year")
    """
    #await fetch_and_print(db_service, lambda:db_service.get_all_persons_type(PersonType.WORKER), "worker_persons_type")
    #await fetch_and_print(db_service, db_service.get_all_projects_phases, TITLE_PROJECTS_PHASES)
    await fetch_and_print(db_service, lambda: db_service.get_phases_by_project("1"), "project")
if __name__ == "__main__":
    asyncio.run(main())