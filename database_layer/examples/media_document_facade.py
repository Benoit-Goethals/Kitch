
from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar, Optional, List

from sqlalchemy import and_


import logging

from database_layer.facade import Facade
from database_layer.examples.media_documen_dbt import MediaDocumentDB
from database_layer.examples.media_document import MediaDocument

T = TypeVar("T")

# Concrete implementation of the Facade for MediaDocument

class MediaDocumentFacade(Facade[MediaDocument], Generic[T]):

    def read_all_filter(self, filter_data) -> Optional[List[T]]:
        pass

    async def read_all_this_week(self, filter_data: Optional[Dict] = None) -> Optional[List[T]]:
        try:
            # Calculate the start and end dates for the current week
            today = datetime.now()
            start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0,
                                                                              microsecond=0)
            end_of_week = (start_of_week + timedelta(days=6)).replace(hour=23, minute=59, second=59,
                                                                      microsecond=999999)

            # Query the repository with the filter
            res = await self.__repo.read_all_filter(and_(
                MediaDocumentDB.date >= start_of_week,
                MediaDocumentDB.date <= end_of_week
            ))

            # Handle invalid responses
            if res is None or not isinstance(res, list):
                self.__logger.error("Repository returned an invalid response.")
                return None

            # Map database objects to domain objects, ensure type conformity
            mapped_objects = [MediaDocumentMapper.to_object(document) for document in res]
            if not all(isinstance(obj, MediaDocument) for obj in mapped_objects):
                self.__logger.error("Mapped objects are not of type MediaDocument.")
                return None

            return mapped_objects  # Return final mapped objects list

        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all_this_week: {e}")
            return None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

        self.__repo = AsyncRepository(model=MediaDocumentDB)


    async def create(self, item: MediaDocument) -> None:
        try:
            """Creates a new MediaDocument."""
            item = MediaDocumentMapper.to_base(item)
            await self.__repo.create(name=item.name, path=item.path, content=item.content, date=item.date, category=item.category, keyword_match=item.keyword_match, type_document=item.type_document)
        except Exception as e:
            self.__logger.error(f"Error: {e}")

    async def read_all(self) -> Optional[List[T]]:
        try:
            # Fetch all records from the repository
            res = await self.__repo.read_all()
            # Handle invalid responses
            if res is None or not isinstance(res, list):
                self.__logger.error("Repository returned an invalid response.")
                return None

            # Map database objects to domain objects
            return  [MediaDocumentMapper.to_object(i) for i in res]
        except Exception as e:
            self.__logger.error(f"Unexpected error in read_all: {e}")
            return None

    async def read(self, identifier: str) -> Optional[MediaDocument]:
        try:
            """Reads a MediaDocument based on the provided identifier."""
            media_doc = await self.__repo.read_by_id(identifier)
            return MediaDocumentMapper.to_object(media_doc)
        except Exception as e:
            self.__logger.error(f"Error: {e}")
            return None


    async def update(self, identifier: str, item: MediaDocument) -> None:
        try:
            """Updates a MediaDocument based on the provided identifier."""
            mapp = MediaDocumentMapper.to_base(item)
            await self.__repo.update(mapp)
        except Exception as e:
            self.__logger.error(f"Error: {e}")

    async def delete(self, identifier: str) -> None:
        """Deletes a MediaDocument."""
        try:
            """Deletes a MediaDocument based on the provided identifier."""
            await self.__repo.delete(identifier)
        except Exception as e:
            self.__logger.error(f"Error: {e}")

