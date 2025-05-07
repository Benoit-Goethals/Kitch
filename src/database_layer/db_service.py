import logging
from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.DatabaseModelClasses import Person, Company, Address, Project
from src.Web_Layer.geo_util import GeoUtil
from src.database_layer.configuration_manager import ConfigurationManager



class DBService:
    """
    This class provides functionalities for managing and interacting with a database, including fetching,
    inserting, and updating data related to different entities such as persons, addresses, companies,
    and projects. It abstracts complexities of database operations while employing asynchronous operations
    to enhance scalability and performance.

    The class employs SQLAlchemy for ORM and database interaction, offering methods to query and manipulate
    data while incorporating structured error handling. It includes utility functions for creating entity-specific
    variations, such as address variations, and fetching geospatial data.

    :ivar NO_ENTITY_FOUND_MSG: Message template logged when no entities are found during a query.
    :type NO_ENTITY_FOUND_MSG: str
    :ivar SessionLocal: Provides asynchronous session objects for database transactions.
    :type SessionLocal: sqlalchemy.ext.asyncio.async_sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]
    """
    NO_ENTITY_FOUND_MSG = "No {entity} found."

    def __init__(self,file_name:str=None):
        """
        Initializes an instance of the class and sets up the necessary configuration
        for database connection and session management. The logger is also configured
        to log at the required levels.

        :param file_name: The path to the configuration file that contains settings
            for initializing the database engine. If None, a default configuration
            file is used.
        :type file_name: str or None
        """
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

        self.__logger = logging.getLogger(__name__)
        async_engine = ConfigurationManager().load(file_name).config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


    async def fetch_and_log(self, entity, query, log_entity_name: str):
        """
        Fetches data from the database based on the provided query and logs relevant details.

        This asynchronous method executes a SQLAlchemy query using the given session, retrieves
        unique results, and logs an error if no entities are found or if an error occurs during
        execution. The method is designed to return all fetched results or None in case of an
        error or empty response.

        :param entity: The entity object or model to use for the query.
        :type entity: Any
        :param query: The SQLAlchemy query object used to fetch data.
        :type query: sqlalchemy.sql.Select
        :param log_entity_name: The human-readable name of the entity, used for logging purposes.
        :type log_entity_name: str
        :return: The list of results fetched from the database, or None if no results were found or
            an error occurred.
        :rtype: Optional[List[Any]]
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
        query = select(Person)
        return await self.fetch_and_log(Person, query, "persons")

    async def get_all_persons_with_address(self) -> Sequence[Person] | None:
        query = select(Person).options(joinedload(Person.address))

        return await self.fetch_and_log(Person, query, "persons with address")

    async def get_all_companies(self) -> Sequence[Company] | None:
        query = select(Company)

        return await self.fetch_and_log(Company, query, "companies")

    async def get_all_addresses(self) -> Sequence[Address] | None:
        query = select(Address)
        return await self.fetch_and_log(Address, query, "addresses")

    async def get_addresses_by_postcode(self,postcode:str) -> Sequence[Address] | None:
        query = select(Address).where(Address.postal_code == postcode)

        return await self.fetch_and_log(Address, query, "addresses")


    async def get_all_postcodes(self) -> Sequence[str] | None:
        query = select(Address.postal_code).distinct()
        return await self.fetch_and_log(Address, query, "postcodes")



    async def get_all_projects(self,) -> Optional[Sequence[Project]]:
        query = select(Project)
        return await self.fetch_and_log(Project, query, "projects")

    async def add_person(self, person: Person) -> bool:
        """Add a new person to the database."""
        try:
            async with self.SessionLocal() as session:
                session.add(person)
                await session.commit()
                self.__logger.info(f"Successfully added person: {person.name_first} {person.name_last}.")
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
                self.__logger.info(f"Successfully added address: {address.street}, {address.postal_code}, {address.municipality}, {address.country}.")
                return True
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in add_address: {e}")
            return False

    async def replace_lat_lon(self) -> bool:
        """Replace latitude and longitude for addresses where available."""
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
        """Fetch latitude and longitude using address variants."""
        for variant in address_variants:
            try:
                lat, lon = await GeoUtil.get_lat_lon_async(variant)
                if lat is not None and lon is not None:
                    return lat, lon
            except Exception as e:
                self.__logger.warning(f"GeoUtil failed for address: {variant}, Error: {e}")
        return None, None
