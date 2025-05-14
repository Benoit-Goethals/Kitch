import logging
import sys
from typing import List, Optional, Sequence

from sqlalchemy import select, extract, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.DatabaseModelClasses import OrderLine, Phase, Assignment
from src.domain.DatabaseModelClasses import Person, Company, Address, Project
from src.Web_Layer.geo_util import GeoUtil
from src.database_layer.configuration_manager import ConfigurationManager



class DBService:
    NO_ENTITY_FOUND_MSG = "No {entity} found."

    def __init__(self,file_name:str=None):

        logging.basicConfig(level=logging.ERROR)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

        self.__logger = logging.getLogger(__name__)
        async_engine = ConfigurationManager().load(file_name).config_db
        if async_engine is None:
            self.__logger.error("Database configuration not found. Please check your configuration file.")
            raise ValueError("Database configuration not found. Please check your configuration file.")
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


    async def fetch_and_log(self, entity, query, log_entity_name: str):
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

    async def get_all_phases(self) -> Sequence[Phase] | None:
        query = select(Phase)
        return await self.fetch_and_log(Phase, query, "phases")


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


    async def get_all_order_lines(self):
        query = select(Project)
        return await self.fetch_and_log(OrderLine, query, "order_lines")

    async def get_phases_by_project(self, selected_project: str) -> Sequence[Phase] | None:
        query = (
            select(Phase)
            .where(Phase.project_id == int(selected_project))
        )
        return await self.fetch_and_log(Phase, query, "phases for the selected project")

    async def get_all_projects_phases(self):
        query = (
            select(Project)
            .options(joinedload(Project.phases))
        )
        return await self.fetch_and_log(Project, query, "projects with phases")

    async def get_all_projects_phases_year(self,year):
        query = (
            select(Project)
            .options(joinedload(Project.phases))
            .where(extract('year', Project.date_start) == int(year))
        )

        return await self.fetch_and_log(Project, query, "projects with phases")

    async def get_data_for_person_between_dates(self, person_id, start_date, end_date):
        query = (
            select(Project)
            .join(Project.phases)
            .join(Phase.assignments)
            .join(Assignment.person)
            .where(
                Assignment.person_id == int(person_id),  # Filter person assignment
                and_(
                    Project.date_start <= end_date,  # Project start date
                    Project.date_end >= start_date  # Project end date
                )
            )
            .options(
                joinedload(Project.phases),  # Eager load phases
                joinedload(Project.phases, Phase.assignments),  # Eager load assignments
                joinedload(Project.phases, Phase.assignments, Assignment.person)  # Eagerly load person
            )
        )
        return await self.fetch_and_log(Project, query, "projects and phases for specific person and date range")

