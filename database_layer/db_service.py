
from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar, Optional, List

from sqlalchemy import and_


import logging

from database_layer.AsyncRepository import AsyncRepository
from database_layer.facade import Facade
from database_layer.examples.media_documen_dbt import MediaDocumentDB
from database_layer.examples.media_document import MediaDocument
from domain.DatabaseModelClasses import Klant


class DBService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__repo = AsyncRepository()


    async def read_all_klant(self) -> Optional[List[Klant]]:
        try:
            # Fetch all records from the repository
            res = await self.__repo.read_all(Klant)
            # Handle invalid responses
            if res is None or not isinstance(res, list):
                self.__logger.error("Repository returned an invalid response.")
                return None

            # Map database objects to domain objects
            return  res
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all: {e}")
            return None

    async def read_klant(self, identifier: str) -> Optional[Klant]:
        try:
            """Reads a MediaDocument based on the provided identifier."""
            media_doc = await self.__repo.read_by_id(identifier)
            return media_doc
        except Exception as e:
            self.__logger.error(f"Error: {e}")
            return None



