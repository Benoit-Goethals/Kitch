import logging
from datetime import datetime

from sqlalchemy import BooleanClauseList
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database_layer.configuration_manager import ConfigurationManager


class AsyncRepository:
    """
    Provides an asynchronous repository pattern implementation for CRUD operations on a specific
    SQLAlchemy model. Designed to work with an asynchronous SQLAlchemy session and manage
    database interactions such as creating, reading, updating, and deleting records. It also
    handles transaction management, ensuring rollbacks are performed on exceptions. The repository
    encapsulates database logic into a manageable interface.

    :ivar model: The SQLAlchemy model class associated with this repository.
    :type model: type
    :ivar SessionLocal: An asynchronous session factory for the configured database.
    :type SessionLocal: async_sessionmaker
    """
    def __init__(self, model):
        self.model = model
        async_engine = ConfigurationManager().config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)



    async def create(self, **kwargs):
        new_instance = self.model(**kwargs)
        async with self.SessionLocal() as session:
            try:
                session.add(new_instance)  # Add the instance to the session
                await session.commit()  # Commit the transaction
            except SQLAlchemyError as e:
                # Any SQLAlchemy-related exception will trigger rollback
                logging.error(f"Database error occurred: {e}")
                await session.rollback()

            except AttributeError as e:
                # Handle issues like trying to access an invalid attribute
                logging.error(f"Attribute error: {e}")
                await session.rollback()

            except Exception as e:
                # General exception handling to rollback on unexpected issues
                logging.error(f"An unexpected error occurred: {e}")
                await session.rollback()

            finally:
                # Ensure the session is always closed
                await session.close()
        return new_instance

    async def read_all(self):
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(select(self.model))  # Query all rows
                rows = result.scalars().all()  # Fetch all scalars (as a list)

                if not rows:
                    logging.info("No results were found for the query.")

                return rows

            except NoResultFound:
                logging.error("No results were found for the query.")

            except SQLAlchemyError as e:
                # Any SQLAlchemy-related exception will trigger rollback
                logging.error(f"Database error occurred: {e}")
                await session.rollback()

            except AttributeError as e:
                # Handle issues like trying to access an invalid attribute
                logging.error(f"Attribute error: {e}")
                await session.rollback()

            except Exception as e:
                # General exception handling to rollback on unexpected issues
                logging.error(f"An unexpected error occurred: {e}")
                await session.rollback()

            finally:
                # Ensure the session is always closed
                await session.close()



    async def read_by_id(self, id_object):
        async with self.SessionLocal() as session:
            try:
               result = await session.get(self.model, id_object)
               return result
            except SQLAlchemyError as e:
                # Log or handle error appropriately
                logging.error(f"Database error: {e}")
                raise

    async def update(self, id_object, **kwargs):
        instance = await self.read_by_id(id_object)
        if not instance:
            raise ValueError(f"Record with id {id_object} not found")

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        async with self.SessionLocal() as session:
            try:
                await session.commit()
            except IntegrityError as e:
                logging.error(f"Database error: {e}")
                await session.rollback()
                raise e

        return instance

    async def delete(self, id_object):
        instance = await self.read_by_id(id_object)
        if not instance:
            raise ValueError(f"Record with id {id_object} not found")
        async with self.SessionLocal() as session:
            await session.delete(instance)
            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                logging.error(f"Database error: {e}")
                raise e
            return True

    async def read_all_filter(self, filters: dict):
        """
        Filters rows based on the provided key-value pairs in the `filters` dictionary
        or a pre-constructed SQLAlchemy BooleanClauseList.
        """
        # If filters are pre-built SQLAlchemy conditions
        if isinstance(filters, BooleanClauseList):
            conditions = filters
        # Else, assume filters are a dictionary
        elif isinstance(filters, dict):
            # Validate if all attributes in filters exist in `self.model`
            for key in filters.keys():
                if not hasattr(self.model, key):
                    logging.error(f"Model '{self.model.__name__}' has no attribute '{key}'")
                    return None
            # Build conditions
            conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        else:
            logging.error("Filters must be a dictionary or a SQLAlchemy BooleanClauseList. "
                          f"Received: {type(filters).__name__}")
            return None

        async with self.SessionLocal() as session:
            try:
                stmt = select(self.model).filter(*conditions)
                result = await session.execute(stmt)
                return result.scalars().all()  # Fetch the matching rows
            except Exception as e:
                logging.error(f"Error in repository read_all_filter: {e}")
                return None




