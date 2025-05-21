import sys
import asyncpg.connection
import yaml
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
import logging
import platform
from src.database_layer.singleton import Singleton

class ConfigurationManager(metaclass=Singleton):
    """
    ConfigurationManager is responsible for managing the application's configuration settings.

    This class helps in loading and managing application configurations from YAML files,
    fetching specific configuration parameters, and setting up database connections as
    specified in the configuration files.

    :ivar __config_path: Path to the configuration file that the manager loads and operates with.
    :type __config_path: Path
    :ivar __app_config: Stores the application-specific configurations loaded from the file.
    :type __app_config: Any
    :ivar __logger: Logger instance used for logging events occurring within the class.
    :type __logger: logging.Logger
    :ivar __config_db: Database connection or configuration object created from the loaded configuration file.
    :type __config_db: asyncpg.connection
    """
    def __init__(self):
        self.__config_path = None
        self.__app_config = None
        self.__logger = logging.getLogger(__name__)
        self.__config_db = None


    @staticmethod
    def __get_project_root() -> Path:
        """
        Identifies the project's root directory.
        Traces upward from the current file's location until the project's root is located.

        Example:
        - Stops at the first directory containing `pyproject.toml`, `.env`, or a parent marker directory.

        Returns:
            Path: The project's root directory path.
        """
        current_path = Path(__file__).resolve().parent
        while current_path != current_path.root:
            if any((current_path / marker_file).exists() for marker_file in
                   ["pyproject.toml", "requirements.txt", ".env"]):
                return current_path
            current_path = current_path.parent

        # Fallback to the parent of the current file
        return Path(__file__).resolve().parent

    def load(self, file_name: str = None):
        """
        Loads the application configuration based on the operating system or custom file name provided.

        This function determines the appropriate configuration file path based on the operating system
        or uses a specified file name. It verifies the existence of the configuration file and initializes
        the system by loading the configuration and database connection properties.

        :param file_name: Optional custom configuration file name
        :type file_name: str, optional
        :return: Returns the initialized instance after loading and setting up configurations
        :rtype: object
        :raises SystemExit: Exits the application if the configuration file is not found or an unexpected error occurs
        """
        try:
            system_name = platform.system()
            if file_name is not None:
                self.__config_path = Path.joinpath(self.__get_project_root(), "src","configurations", file_name)
            elif system_name == "Windows":
                logging.info("Running on Windows")
                path = Path("C:\\ProgramData\\Kitch")
                self.__config_path = Path.joinpath(path, "configurations", "config.yml")
                if not path.exists() or not self.__config_path.exists():
                    self.__logger.error(f"Configuration file not found in expected Windows locations.{path.absolute()}")
            elif system_name == "Linux":
                logging.info("Running on Linux")
                self.__config_path = Path.joinpath(Path.home(), "configurations", "config.yml")
                if not self.__config_path.exists():
                  self.__logger.error(f"Configuration file not found in expected Linux location.{self.__config_path.absolute()}")
            else:
                self.__logger.error(f"Unsupported platform: {system_name}")

            if self.__config_path is None:
                sys.exit("Configuration file not found")


            config = self.__load_configuration()
            logging.info("Application configuration loaded successfully.")
            self.__config_db = self.__setup_connection_from_yaml(config)
            return self

        except Exception as error:
            logging.error(f"Unexpected error occurred while loading configuration: {error}")
            sys.exit("Error occurred while loading configuration")

    @staticmethod
    def __setup_connection_from_yaml(config) -> asyncpg.connection:
        """
        Establishes a database connection using configuration details provided in a YAML file,
        utilizing SQLAlchemy's asyncpg engine for PostgreSQL. This method configures the
        connection pool and associated settings to optimize performance for concurrent
        requests.

        The connection ensures proper authentication and is tuned for production-level
        requirements while maintaining a balance between stability and resource utilization.

        :param config: Dictionary containing database connection details. The required fields are:
                       - db.username: Username for the PostgreSQL database connection.
                       - db.password: Password for the PostgreSQL database connection.
                       - db.host: Host address of the PostgreSQL database server.
                       - db.port: Port number of the PostgreSQL database server.
                       - db.database: Database name to connect to.

        :return: An asynchronous SQLAlchemy database engine configured to manage
                 database connections using asyncpg.
        :rtype: asyncpg.connection
        """
        return create_async_engine(
            url=f"postgresql+asyncpg://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['database']}",
            echo=False,  # Set to False for production to reduce excessive logging overhead
            future=True,
            pool_size=20,  # Increase pool size for handling more concurrent requests
            max_overflow=30,  # Allow more connection overflow
            pool_recycle=3600,  # Recycle less often if connections are stable
            pool_timeout=30  # Increase timeout for waiting connections
        )

    @property
    def config_db(self) -> asyncpg.connection:
        return self.__config_db

    @staticmethod
    def __load_yaml_file( file_path:Path):
        """Helper method to load YAML data from a given file."""
        try:
            with open(file_path.absolute(), 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        except yaml.YAMLError as error:
            raise ValueError(f"Error parsing YAML file: {file_path}, Error: {error}")

    def __load_configuration(self):
        """Loads the configuration data."""
        return self.__load_yaml_file(self.__config_path)

    def get_config_value(self, key, default=None):
        """
        Fetches a specific configuration value by key.
        :param key: Key to search in the configuration file.
        :param default: Default value if the key is not present.
        """
        config = self.__load_configuration()
        return config.get(key, default)