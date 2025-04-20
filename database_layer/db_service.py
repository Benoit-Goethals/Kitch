
from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar, Optional, List
from sqlalchemy import and_
import logging
from database_layer.AsyncRepository import AsyncRepository
from domain.DatabaseModelClasses import  Person


class DBService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__repo = AsyncRepository()



    async def read_all_persons(self) -> Optional[List[Person]]:
        try:
            res = await self.__repo.read_all(Person)
            if res is None or not isinstance(res, list):
                self.__logger.error("Repository returned an invalid response.")
                return None
            return res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all: {e}")
            return None

    async def read_person(self, identifier: str) -> Optional[Person]:
        try:
            media_doc = await self.__repo.read_by_id(Person, identifier)
            return media_doc
        except Exception as e:
            self.__logger.error(f"Error: {e}")
            return None



