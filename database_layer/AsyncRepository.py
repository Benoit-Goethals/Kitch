import logging
from datetime import datetime

from sqlalchemy import BooleanClauseList
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database_layer.configuration_manager import ConfigurationManager


class AsyncRepository:

    def __init__(self):

        async_engine = ConfigurationManager().config_db
        self.SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


    async def create(self,model, **kwargs):
        new_instance = model(**kwargs)
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

    async def read_all(self,model):
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(select(model))  # Query all rows
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



    async def read_by_id(self,model, id_object):
        async with self.SessionLocal() as session:
            try:
               result = await session.get(model, id_object)
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

    async def read_all_filter(self, model,filters: dict):
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
                if not hasattr(model, key):
                    logging.error(f"Model '{model.__name__}' has no attribute '{key}'")
                    return None
            # Build conditions
            conditions = [getattr(model, key) == value for key, value in filters.items()]
        else:
            logging.error("Filters must be a dictionary or a SQLAlchemy BooleanClauseList. "
                          f"Received: {type(filters).__name__}")
            return None

        async with self.SessionLocal() as session:
            try:
                stmt = select(model).filter(*conditions)
                result = await session.execute(stmt)
                return result.scalars().all()  # Fetch the matching rows
            except Exception as e:
                logging.error(f"Error in repository read_all_filter: {e}")
                return None




