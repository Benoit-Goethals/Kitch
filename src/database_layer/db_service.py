import logging
from typing import List, Optional, Sequence
from sqlalchemy import select, extract, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload
from src.Web_Layer.geo_util import GeoUtil
from src.configurations.configuration_manager import ConfigurationManager
from src.domain.DatabaseModelClasses import Employee, Worker
from src.domain.DatabaseModelClasses import OrderLine, Phase, Assignment
from src.domain.DatabaseModelClasses import Person, Company, Address, Project
from src.domain.person_type import PersonType


class DBService:
    NO_ENTITY_FOUND_MSG = "No {entity} found."

    def __init__(self, file_name: str = None):
        """
        Initializes the database session manager with the provided configuration.

        The constructor ensures that the database can be configured properly using the specified
        configuration file. It sets up logging for the SQLAlchemy engine to suppress unnecessary
        logging at the error level. The async session maker is configured to interact with the
        database. If the database configuration cannot be loaded, the initialization process will
        raise an exception and provide an appropriate error message.

        :param file_name: Name of the configuration file to load. If not specified,
            defaults will be applied to locate the configuration.
        :type file_name: str or None
        :raises ValueError: If the database configuration is missing or cannot be loaded
        """
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
        self.__logger = logging.getLogger(__name__)
        async_engine = ConfigurationManager(file_name).config_db
        if async_engine is None:
            self.__logger.error("Database configuration not found. Please check your configuration file.")
            raise ValueError("Database configuration not found. Please check your configuration file.")
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

    async def fetch_and_log(self, entity, query, log_entity_name: str):
        """
        Fetches entities from the database using the given query and logs necessary
        information. Ensures error handling for SQLAlchemy-specific errors as well
        as unexpected exceptions. It logs a message if no entities are found and
        returns the fetched results if successful.

        :param entity: The entity for which data is being queried.
        :type entity: Any
        :param query: SQLAlchemy query to be executed for fetching the entities.
        :type query: sqlalchemy.sql.selectable.Select
        :param log_entity_name: Name of the entity to be logged for clarity in error
                                or information messages.
        :type log_entity_name: str
        :return: A list of unique scalar results if entities are found, or None
                 otherwise.
        :rtype: list[Any] | None
        """
        try:
            async with self.SessionLocal() as session:
                result = await session.execute(query)
                res = result.unique().scalars().all()
                if not res:
                    self.__logger.error(self.NO_ENTITY_FOUND_MSG.format(entity=log_entity_name))
                    self.__logger.info("No entities found. Please check your database and try again.")
                    return None
                return res
        except SQLAlchemyError as e:
            self.__logger.error(f"SQLAlchemy error fetching {log_entity_name}: {e}")
            return None
        except Exception as e:
            self.__logger.error(f"Unexpected error fetching {log_entity_name}: {e}")
            return None

    async def get_all_persons(self) -> Sequence[Person] | None:
        """
        Fetches all person records from the database.

        This asynchronous method executes a database query to retrieve all records
        of the `Person` table. It uses the `fetch_and_log` method for executing the
        query and logging the results.

        :return: A sequence of `Person` objects if records are found,
                 otherwise None
        :rtype: Sequence[Person] | None
        """
        query = select(Person)
        return await self.fetch_and_log(Person, query, "persons")

    async def get_all_persons_type(self, type_person: PersonType) -> Sequence[Person] | None:
        """
        Asynchronously retrieves all persons of a specified type. This function fetches
        the data from the database using pre-defined queries mapped to specific person
        types, and uses a logging mechanism to track the retrieval process.

        :param type_person: The type of person to retrieve, defined as a `PersonType`.
        :return: A sequence of `Person` objects matching the specified type,
                 or `None` if no such persons exist.
        :rtype: Sequence[Person] | None
        :raises ValueError: If an invalid `type_person` value is provided.
        """
        type_to_query_mapping = {
            PersonType.WORKER.value: select(Worker).options(joinedload(Worker.person)),
            PersonType.EMPLOYEE.value: select(Employee).options(joinedload(Employee.person)),
        }

        query = type_to_query_mapping.get(type_person.value, None)
        if query is None:
            raise ValueError(f"Invalid person type: {type_person}")

        return await self.fetch_and_log(Person, query, "persons")

    async def get_all_persons_with_address(self) -> Sequence[Person] | None:
        """
        Retrieves all persons with their associated addresses from the database.

        The function executes an asynchronous query to fetch all records of `Person`
        with a joined load of their `address` relationships. If no records are found,
        the function may return None. This is done while logging the query result for
        diagnostic or debugging purposes.

        :rtype: Sequence[Person] | None
        :return: A sequence of `Person` objects including their associated `address`
            or None if no records are available.
        """
        query = select(Person).options(joinedload(Person.address))

        return await self.fetch_and_log(Person, query, "persons with address")

    async def get_all_companies(self) -> Sequence[Company] | None:
        """
        Fetches all companies from the database asynchronously.

        This method performs a database query to retrieve all instances of the `Company`
        model. It utilizes the `fetch_and_log` helper method to execute the query,
        log the operation for debugging purposes, and handle the results. If no
        companies exist in the database, it will return None.

        :raises DatabaseError: Raised if there is an underlying error during the
            database query execution.
        :return: A sequence of `Company` objects if any exist in the database,
            otherwise None.
        :rtype: Sequence[Company] | None
        """
        query = select(Company)

        return await self.fetch_and_log(Company, query, "companies")

    async def get_all_addresses(self) -> Sequence[Address] | None:
        """
        Fetches and retrieves all addresses from the database.

        This method constructs a query to select all entries from the Address
        table. The retrieved data is fetched asynchronously and logged with a
        specific label for tracking purposes. If no addresses are found, the
        method may return None.

        :return: A sequence of Address objects representing all entries in the
            Address table, or None if no entries exist.
        :rtype: Sequence[Address] | None
        """
        query = select(Address)
        return await self.fetch_and_log(Address, query, "addresses")

    async def get_addresses_by_postcode(self, postcode: str) -> Sequence[Address] | None:
        """
        Retrieve a list of addresses based on the provided postcode.

        This asynchronous method queries the Address table to find all addresses
        matching the specified postal code. It then fetches the results and logs
        them, returning the results if found.

        :param postcode: The postal code to filter addresses by.
        :type postcode: str
        :return: A sequence of `Address` objects matching the postcode,
                 or None if no addresses are found.
        :rtype: Sequence[Address] | None
        """
        query = select(Address).where(Address.postal_code == postcode)

        return await self.fetch_and_log(Address, query, "addresses")

    async def get_all_postcodes(self) -> Sequence[str] | None:
        """
        Retrieves all distinct postal codes from the Address table.

        This asynchronous method queries the database to fetch all unique
        postal codes from the Address model and logs the results. It returns
        a sequence of postal codes or None if no postal codes are found.

        :return: A sequence of distinct postal codes or None if no postal codes are found.
        :rtype: Sequence[str] | None
        """
        query = select(Address.postal_code).distinct()
        return await self.fetch_and_log(Address, query, "postcodes")

    async def get_all_phases(self) -> Sequence[Phase] | None:
        """
        Asynchronously fetches all records of `Phase` from the database.

        This method retrieves all phases available in the database by executing a
        SQL SELECT query on the `Phase` table. If no records are present, it
        returns `None`.

        :return: A sequence of `Phase` objects if found, otherwise `None`.
        :rtype: Sequence[Phase] | None
        """
        query = select(Phase)
        return await self.fetch_and_log(Phase, query, "phases")

    async def get_all_projects(self, ) -> Optional[Sequence[Project]]:
        """
        Fetch and return all project records from the database.

        This asynchronous method retrieves all instances of the `Project` class
        by executing a database query. It uses the associated fetch and log
        mechanism to fetch and log the data for monitoring or debugging purposes.

        :return: A sequence of `Project` objects if any are found, otherwise None.
        :rtype: Optional[Sequence[Project]]
        """
        query = select(Project)
        return await self.fetch_and_log(Project, query, "projects")

    async def add_person(self, person: Person, type_personnel) -> bool:
        """Add a new person to the database."""
        try:
            async with self.SessionLocal() as session:
                session.add(person)
                await session.flush()

                if type_personnel == PersonType.WORKER:
                    worker = Worker(person_id=person.person_id)
                    session.add(worker)
                elif type_personnel == PersonType.EMPLOYEE:
                    employee = Employee(person_id=person.person_id)
                    session.add(employee)

                await session.commit()
                self.__logger.info(f"Successfully added {type_personnel.name}: {person.name_first} {person.name_last}.")
                return True
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in add_person: {e}")
            return False
        except Exception as e:
            self.__logger.error(f"Unexpected error in add_person: {e}")
            return False

    async def add_address(self, address: Address) -> bool:
        """Add a new address to the database."""
        try:
            async with self.SessionLocal() as session:
                session.add(address)
                await session.flush()
                await session.commit()
                self.__logger.info(
                    f"Successfully added address: {address.street}, {address.postal_code}, {address.municipality}, {address.country}.")
                return True
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in add_address: {e}")
            return False

    async def replace_lat_lon(self) -> bool:
        """
        Replaces latitude and longitude of addresses in the database if
        applicable. Fetches addresses from the database, generates different
        address variants for geocoding, retrieves latitude and longitude
        for the generated variants, and updates the database accordingly.

        :return: Returns True if latitude and longitude of addresses are
                 successfully updated, otherwise False.
        :rtype: bool
        """
        try:
            async with self.SessionLocal() as session:
                addresses = await self.fetch_and_log(Address, select(Address), "addresses")
                if not addresses:
                    return False

                for address in addresses:
                    address_variants = self.create_address_variants(address)
                    lat, lon = await self.get_lat_lon_from_variants(address_variants)
                    if lat is not None and lon is not None:
                        address.latitude = lat
                        address.longitude = lon
                    session.add(address)
                await session.flush()
                await session.commit()
                self.__logger.info("Successfully updated lat/lon for addresses.")
                return True
        except Exception as e:
            self.__logger.error(f"Error in replace_lat_lon: {e}")
            return False

    @staticmethod
    def create_address_variants(address: Address) -> List[str]:
        """Create different address variations based on the available address fields."""
        variants = [
            f"{address.street}, {address.postal_code}, {address.municipality}, {address.country}",
            f"{address.street}, {address.municipality}, {address.country}",
            f"{address.municipality}, {address.country}"
        ]
        return [variant for variant in variants if variant]

    async def get_lat_lon_from_variants(self, address_variants: List[str]) -> tuple[Optional[float], Optional[float]]:
        """
        Retrieves the latitude and longitude for the given address variants asynchronously.

        This method iterates through a list of address variants and attempts to retrieve
        the latitude and longitude for each variant using an external utility. If a valid
        latitude and longitude are obtained, the method returns the values immediately.
        Errors encountered during the retrieval process for individual address variants are
        logged, and the method continues with the next variant. If no valid coordinates are
        obtained for any variant, the method returns None for both latitude and longitude.

        :param address_variants: A list of address strings for which latitude and longitude
            should be determined.
        :type address_variants: List[str]
        :return: A tuple containing optional latitude and longitude values. Returns
            (None, None) if no valid coordinates are found for any variant.
        :rtype: tuple[Optional[float], Optional[float]]
        """
        for variant in address_variants:
            try:
                lat, lon = await GeoUtil.get_lat_lon_async(variant)
                if lat is not None and lon is not None:
                    return lat, lon
            except Exception as e:
                self.__logger.warning(f"GeoUtil failed for address: {variant}, Error: {e}")
        return None, None

    async def get_all_order_lines(self):
        """
        Retrieve all order line records from the database.

        This method executes a database query to fetch all instances of the
        `OrderLine` model. The query is logged for monitoring enabled
        with a descriptive message. It is designed to work asynchronously
        to improve performance and handle concurrent tasks efficiently.

        :return: A list of `OrderLine` records retrieved from the database.
        :rtype: list
        """
        query = select(Project)
        return await self.fetch_and_log(OrderLine, query, "order_lines")

    async def get_phases_by_project(self, selected_project: str) -> Sequence[Phase] | None:
        """
        Fetches phases associated with a given project asynchronously.

        This method retrieves all phases related to the provided project identifier
        by constructing a SQL query and executing it against the database. If
        phases are found for the specified project, they are returned as a sequence.
        If no phases are found, the method returns None. The process also includes
        logging of the fetched phase details for debugging or monitoring purposes.

        :param selected_project: The identifier of the project whose phases are
                                 to be retrieved.
        :type selected_project: str
        :return: A sequence of "Phase" objects associated with the project if found;
                 otherwise, None.
        :rtype: Sequence[Phase] | None
        """
        query = (
            select(Phase).options(joinedload(Phase.assignments))
            .where(Phase.project_id == int(selected_project))
        )
        return await self.fetch_and_log(Phase, query, "phases for the selected project")

    async def get_all_projects_phases(self):
        """
        Fetch all projects with their associated phases.

        This method executes a database query to fetch all project entries from the
        database, including their related phases, if any. The method uses the
        ``select`` statement with ``joinedload`` to efficiently load associated
        phases data. After executing the query, it logs the results for auditing
        or debugging purposes.

        :raises SQLAlchemyError: If an error occurs during the execution of
            the database query.
        :raises Exception: If any unexpected issue occurs during the process.

        :return: A list of ``Project`` objects, each including its associated phases.
        :rtype: List[Project]
        """
        query = (
            select(Project)
            .options(joinedload(Project.phases))
        )
        return await self.fetch_and_log(Project, query, "projects with phases")

    async def get_all_projects_phases_year(self, year):
        """
        Fetches all projects and their associated phases for a given year.

        This asynchronous method constructs a database query to retrieve all projects
        and their phases where the starting date of the project matches the specified
        year. The retrieved projects and phases are then fetched from the database
        and logged for further processing.

        :param year: The year to filter projects by.
        :type year: int
        :return: A list of projects with their loaded phases for the specified year.
        :rtype: List[Project]
        """
        query = (
            select(Project)
            .options(joinedload(Project.phases))
            .where(extract('year', Project.date_start) == int(year))
        )

        return await self.fetch_and_log(Project, query, "projects with phases")

    async def get_data_for_worker_between_dates(self, person_id, start_date, end_date):
        """
        Asynchronously retrieves a list of projects and their associated phases for a specific worker within the given
        date range. The query ensures that only projects active within the given date range, and associated with the
        specified worker, are retrieved. This is achieved by filtering based on the worker's ID and the project's
        start and end dates. The necessary relationships (phases, assignments, and workers) are eagerly loaded
        to optimize database interaction.

        :param person_id: The unique identifier of the worker whose data is being queried.
        :type person_id: int
        :param start_date: The start date of the filtering range. Projects must have started on or before this date.
        :type start_date: datetime.date
        :param end_date: The end date of the filtering range. Projects must have ended on or after this date.
        :type end_date: datetime.date
        :return: A coroutine that resolves to the list of project records matching the criteria.
        :rtype: Coroutine
        """
        query = (
            select(Project)
            .join(Project.phases)
            .join(Phase.assignments)
            .join(Assignment.worker)
            .where(
                Assignment.worker_id == int(person_id),  # Filter person assignment
                and_(
                    Project.date_start <= end_date,  # Project start date
                    Project.date_end >= start_date  # Project end date
                )
            )
            .options(
                joinedload(Project.phases),  # Eager load phases
                joinedload(Project.phases, Phase.assignments),  # Eager load assignments
                joinedload(Project.phases, Phase.assignments, Assignment.worker)  # Eagerly load person
            )
        )
        return await self.fetch_and_log(Project, query, "projects and phases for specific person and date range")

    async def delete_person(self, person_id: int) -> bool | None:
        """
        Deletes a person record from the database based on the specified person_id.
        Performs this operation within an asynchronous session and commits the
        transaction if successful. Logs information for successful deletions or
        errors encountered during the operation.

        :param person_id: The unique identifier of the person to be deleted.
        :type person_id: int
        :return: True if the deletion was successful, None if an error occurred.
        :rtype: bool | None
        """
        try:
            async with self.SessionLocal() as session:
                session.query(Person).filter(Person.person_id == person_id).delete()
                await session.commit()
                self.__logger.info(f"Successfully deleted person with ID {person_id}.")
                return True
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in delete_person: {e}")
            return None

    async def get_person_by_id(self, person_id: int) -> Person | None:
        """
        Retrieve a person by their unique identifier.

        This asynchronous method queries a database to find a person record
        based on the provided person ID. If a matching record is found, it
        returns an instance of the `Person` model. If no record is found,
        it returns None.

        :param person_id: The unique identifier of the person to retrieve.
        :return: An instance of the `Person` model if a record is found;
                 otherwise, returns None.
        """
        query = select(Person).where(Person.person_id == person_id)
        return await self.fetch_and_log(Person, query, "person with ID")

    async def get_project(self, id_project: int):
        """
        Fetch a project from the database by its unique project ID asynchronously.

        This method constructs a query to retrieve a project from the database using
        the provided `id_project`. The fetched project is logged and returned.

        :param id_project: The unique identifier of the project to fetch.
        :type id_project: int
        :return: The project object corresponding to the provided `id_project`.
        :rtype: Project
        """
        selection = select(Project).options(joinedload(Project.phases)).where(Project.project_id == id_project)
        return await self.fetch_and_log(Project, selection, f"project_{id_project}")
