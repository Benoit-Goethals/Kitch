
from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar, Optional, List, Any, Coroutine, Sequence
from sqlalchemy import and_, select, Row, RowMapping
import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from database_layer.configuration_manager import ConfigurationManager
from domain.DatabaseModelClasses import Person, Company


class DBService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

        async_engine = ConfigurationManager().config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

    async def read_all_persons(self) -> Sequence[Person] | None:
        try:
            async with self.SessionLocal() as session:
                result = await session.execute(
                    select(Person).options(selectinload(Person.companies))  # Eagerly load 'companies'
                )
                res = result.scalars().all()
                if res is None:
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




