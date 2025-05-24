from abc import ABC, abstractmethod

class Report(ABC):
    """
    Represents a blueprint for creating various types of reports,
    each with unique content and naming conventions. This class
    provides the skeleton for concrete report implementations,
    enforcing a consistent interface through abstract methods.

    :ivar db_service: Database service used for data fetching and operations.
    :type db_service: Any
    """
    def __init__(self):
        self.db_service = None

    @abstractmethod
    async def get_content(self)->[]:
        pass

    @staticmethod
    @abstractmethod
    def name_suffix()->str:
        pass

