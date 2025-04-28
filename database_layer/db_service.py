from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar, Optional, List, Any, Coroutine, Sequence
from sqlalchemy import and_, select, Row, RowMapping, update
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from Web_Layer.geo_util import GeoUtil
from database_layer.configuration_manager import ConfigurationManager
from domain.DatabaseModelClasses import Person, Company, Address, Assignment

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


class DBService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

        async_engine = ConfigurationManager().config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

    async def read_all_persons(self) -> Sequence[Person] | None:
        try:
            async with self.SessionLocal() as session:
                # Fetch all persons with joined eager loading of relationships
                result = await session.execute(
                    select(Person).options(joinedload(Person.companies))  # Use joinedload for eager loading
                )

                # Use scalars to extract the `Person` objects, ensuring uniqueness
                res = result.unique().scalars().all()

                if not res:
                    self.__logger.error("No persons found.")
                    return None
                return res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all_persons: {e}")
            return None

    async def read_all_persons_with_address(self) -> Sequence[Person] | None:
        try:
            async with self.SessionLocal() as session:
                # Fetch all persons with joined eager loading of relationships
                result = await session.execute(
                    select(Person).options(joinedload(Person.address))  # Use joinedload for eager loading
                )

                # Use scalars to extract the `Person` objects, ensuring uniqueness
                res = result.unique().scalars().all()

                if not res:
                    self.__logger.error("No persons found.")
                    return None
                return res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all_persons: {e}")
            return None

    async def read_all_companies(self) -> Sequence[Company] | None:
        try:
            async with self.SessionLocal() as session:
                result = await session.execute(
                    select(Company).options(
                        selectinload(Company.address),
                        selectinload(Company.contact_person)
                    )
                )
                res = result.scalars().all()
                if res is None:
                    self.__logger.error("No companies found.")
                    return None
                return res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all_companies: {e}")
            return None

    async def read_all_address(self) -> Sequence[Address] | None:
        try:
            async with self.SessionLocal() as session:
                result = await session.execute(
                    select(Address).options(
                        selectinload(Address.companies),
                    )
                )

                # Use `unique()` before extracting scalars to ensure no duplicates
                res = result.unique().scalars().all()

                if not res:
                    self.__logger.error("No Address found.")
                    return None

                return res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all_Address {e}")
            return None

    async def read_all_assignment(self) -> Optional[Sequence[Assignment]]:
        try:
            async with self.SessionLocal() as session:  # Ensure SessionLocal is properly configured
                result = await session.execute(
                    select(Assignment).options(
                        selectinload(Assignment.sub_assignments),
                    )
                )
                res = result.unique().scalars().all()
                if not res:
                    self.__logger.info("No assignments found in the database.")  # Change to info/warning
                    return None
                return res
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in read_all_assignment: {e}")
            return None
        except Exception as e:  # Catch unexpected runtime errors
            self.__logger.error(f"Unexpected error in read_all_assignment: {e}")
            return None

    async def replace_lat_lon(self):
        """Replace latitude and longitude for addresses based on their fields."""
        try:
            async with self.SessionLocal() as session:
                # Fetch all addresses
                result = await session.execute(select(Address))
                addresses = result.scalars().unique().all()

                # If no addresses are found
                if not addresses:
                    self.__logger.info("No addresses found to update lat/lon.")
                    return False
                
                # Update lat/lon for addresses with valid address fields
                for address in addresses:
                    # Construct full address from address fields
                    if address.street and address.postal_code and address.municipality and address.country:
                        full_address = (
                            f"{address.street}, "
                            f"{address.postal_code}, "
                            f"{address.municipality}, "
                            f"{address.country}"
                        )

                        # Get lat/lon using GeoUtil
                        try:
                            lat, lon = await GeoUtil.get_lat_lon_async(full_address)
                            if lat is None or lon is None:
                                small_address = (
                                    f"{address.street}, "
                                    f"{address.municipality}, "
                                    f"{address.country}"
                                )
                                lat, lon = await GeoUtil.get_lat_lon_async(small_address)
                            if lat is None or lon is None:
                                small_address = (
                                    f"{address.municipality}, "
                                    f"{address.country}"
                                )
                                lat, lon = await GeoUtil.get_lat_lon_async(small_address)

                            if lat is None or lon is None:
                                self.__logger.warning(f"Failed to get lat/lon for address: {full_address}.")
                                continue
                        except Exception as e:
                            self.__logger.warning(f"Failed to get lat/lon for address: {full_address}. Error: {e}")
                            continue
                        
                        # Update the address with geo-coordinates
                        if lat is not None and lon is not None:
                            address.latitude = lat
                            address.longitude = lon

                # Commit changes to the database
                await session.commit()
                self.__logger.info("Successfully updated lat/lon for addresses.")
                return True

        except SQLAlchemyError as e:
            self.__logger.error(f"Database error in replace_lat_lon: {e}")
            return False
        except Exception as e:
            self.__logger.error(f"Unexpected error in replace_lat_lon: {e}")
            return False
    async def add_person(self, person: Person):
        """
        Add a new person to the database.

        Args:
            person (Person): An instance of the Person class to be added to the database.

        Returns:
            bool: True if the person was added successfully, False otherwise.
        """
        try:
            async with self.SessionLocal() as session:
                # Add and commit the Person instance to the database
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