import datetime
import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from datetime import datetime
import sqlalchemy
from pydyf import Object

from database_layer.media_documen_dbt import MediaDocumentDB
from database_layer.media_document import MediaDocument
from domain.DatabaseModelClasses import Base


class AbstractMediaDocumentMapper(ABC):
    @staticmethod
    @abstractmethod
    def to_object(db_object: Base) -> Object:
        """
        Converts an instance of MediaDocumentDB to MediaDocument.
        Must be implemented by subclasses.
        """
        pass

    @staticmethod
    @abstractmethod
    def to_base(domain_object) -> Base:
        """
        Converts an instance of MediaDocument to MediaDocumentDB.
        Must be implemented by subclasses.
        """
        pass


class MediaDocumentMapper(AbstractMediaDocumentMapper):
    """
    Facilitates conversion between MediaDocument and MediaDocumentDB objects.

    This class provides static methods to transform MediaDocument database objects
    (MediaDocumentDB) to domain-level objects (MediaDocument) and vice versa. It is
    designed to handle data mapping and serialization/deserialization tasks,
    enabling seamless interchange between the data and domain layers.

    """
    @staticmethod
    def to_object(db_object: MediaDocumentDB) -> MediaDocument:
        if not db_object:
            raise ValueError("Input db_object cannot be None.")
        try:
            r = MediaDocument(
                id_object=db_object.id,
                name=db_object.name,
                path=db_object.path,
                date_start=db_object.date.date() if db_object.date else None,
                type_document=None


            )
            r.keyword_match = json.loads(db_object.keyword_match) if db_object.keyword_match else {}
            r.content = db_object.content
            return r
        except JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in db_object.keyword_match: {e}")
        except Exception as e:
            raise ValueError(f"An error occurred while converting db_object to MediaDocument: {e}")


    @staticmethod
    def to_base(domain_object: MediaDocument) -> MediaDocumentDB:
        """
        Converts an instance of MediaDocument to MediaDocumentDB.
        Handles type conversion and default value assignment.
        """
        return MediaDocumentDB(
            id=domain_object.id,
            name=domain_object.name,
            path=str(domain_object.path),
            content=domain_object.content,
            date=datetime.combine(domain_object.date_start, datetime.min.time()) if domain_object.date_start else None,

            keyword_match=json.dumps(domain_object.keyword_match) if domain_object.keyword_match else None,

        )

