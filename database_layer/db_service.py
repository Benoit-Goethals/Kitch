import logging
from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from Web_Layer.geo_util import GeoUtil
from database_layer.configuration_manager import ConfigurationManager
from domain.DatabaseModelClasses import Address, Person, Company, Project


class DBService:
    NO_ENTITY_FOUND_MSG = "No {entity} found."

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        async_engine = ConfigurationManager().config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

    async def fetch_and_log(self, entity, query, log_entity_name: str):
        """Reusable method to execute queries and log results."""
        try:
            async with self.SessionLocal() as session:
                result = await session.execute(query)
                res = result.unique().scalars().all()
                if not res:
                    self.__logger.error(self.NO_ENTITY_FOUND_MSG.format(entity=log_entity_name))
                    return None
                return res
        except SQLAlchemyError as e:
            self.__logger.error(f"SQLAlchemy error fetching {log_entity_name}: {e}")
            return None
        except Exception as e:
            self.__logger.error(f"Unexpected error fetching {log_entity_name}: {e}")
            return None

    async def get_all_persons(self) -> Sequence[Person] | None:
        query = select(Person).options(joinedload(Person.companies_as_contact))
        return await self.fetch_and_log(Person, query, "persons")

    async def get_all_persons_with_address(self) -> Sequence[Person] | None:
        query = select(Person).options(joinedload(Person.address))
        return await self.fetch_and_log(Person, query, "persons with address")

    async def get_all_companies(self) -> Sequence[Company] | None:
        query = select(Company).options(
            selectinload(Company.address),
            selectinload(Company.contact_person)
        )
        return await self.fetch_and_log(Company, query, "companies")

    async def get_all_addresses(self) -> Sequence[Address] | None:
        query = select(Address).options(selectinload(Address.companies))
        return await self.fetch_and_log(Address, query, "addresses")

    async def get_all_projects(self) -> Optional[Sequence[Project]]:
        query = select(Project).options(selectinload(Project.phases))
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