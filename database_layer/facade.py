from abc import ABC, abstractmethod

from typing import Dict, Generic, TypeVar, Optional, List

import logging
T = TypeVar("T")


class Facade(ABC, Generic[T]):
    """
    Defines an abstract base class for a generic CRUD facade pattern.

    This class serves as a blueprint for implementing create, read, update,
    and delete operations on entities of a generic type `T`. It forces any
    subclass to provide concrete implementations for all of its abstract
    methods. This ensures a consistent interface when dealing with CRUD
    operations, making it useful for a wide variety of applications.

    :ivar _items: Internal storage for the facade, this list holds all
        entities of type `T`.
    :type _items: Optional[List[T]]

    :ivar _logger: Logger instance for recording activities in the facade.
    :type _logger: Optional[logging.Logger]
    """
    @abstractmethod
    def create(self, item: T) -> None:
        """Creates an item of type T."""
        pass

    @abstractmethod
    def read(self, identifier: str) -> Optional[T]:
        """Reads an item of type T based on the provided identifier."""
        pass

    @abstractmethod
    def read_all(self) -> Optional[List[T]]:
        """Reads an item of type T based on the provided identifier."""
        pass

    @abstractmethod
    def read_all_filter(self, filter_data) -> Optional[List[T]]:
        """Reads an item of type T based on the provided identifier."""
        pass

    @abstractmethod
    def update(self, identifier: str, item: T) -> None:
        """Updates an existing item of type T based on the identifier."""
        pass

    @abstractmethod
    def delete(self, identifier: str) -> None:
        """Deletes an item of type T based on the identifier."""
        pass

