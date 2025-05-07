import asyncpg.connection
import yaml
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine


import logging
import platform

from src.database_layer.singleton import Singleton


class ConfigurationManager(metaclass=Singleton):
    """
    Manages the application's configuration settings.

    This class handles the loading, parsing, and management of configuration files used within
    the application, supporting platform-specific paths or custom file locations. It facilitates
    retrieval of configuration values and the setup of database connections based on the parsed
    configuration. The configuration management operates as a singleton to ensure a consistent
    application state and reduce resource redundancy.

    :ivar __config_path: The file path of the configuration file.
    :type __config_path: Path | None
    :ivar __app_config: Stores application-level configuration details.
    :type __app_config: dict | None
    :ivar __config_db: Connection object to the database as per configuration.
    :type __config_db: asyncpg.connection | None
    """
    def __init__(self):
        self.__config_path = None
        self.__app_config = None

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
        Loads the application configuration based on the system's platform or a specified file path. If no
        file name is provided, it attempts to locate a default configuration file depending on whether
        the platform is Windows or Linux. The configuration is then parsed, and a connection to the database
        is set up from the parsed YAML data.

        :param file_name: The optional name of the configuration file. If provided, the method tries to load
            the configuration using this file name. If not provided, the platform's default configuration
            path is used.
        :type file_name: str, optional

        :return: Returns the instance of the calling object after loading the configuration and setting up
            the necessary resources.
        :rtype: self

        :raises FileNotFoundError: Raised when the configuration file is not found in the expected location
            or the file name provided does not exist.
        :raises ValueError: Raised when the YAML configuration file has parsing errors.
        :raises RuntimeError: Raised for unsupported platforms.
        :raises Exception: Raised for any other unexpected issues during the configuration loading process.
        """
        try:
            system_name = platform.system()
            if file_name is not None:
                self.__config_path = Path.joinpath(self.__get_project_root(), "configurations", file_name)
            elif system_name == "Windows":
                logging.info("Running on Windows")
                path = Path("C:\\ProgramData\\check")
                self.__config_path = Path.joinpath(path, "configurations", "config.yml")
                if not path.exists() or not self.__config_path.exists():
                    raise FileNotFoundError("Configuration file not found in expected Windows locations.")
            elif system_name == "Linux":
                logging.info("Running on Linux")
                self.__config_path = Path.joinpath(Path.home(), "configurations", "config.yml")
                if not self.__config_path.exists():
                    raise FileNotFoundError("Configuration file not found in expected Linux location.")
            else:
                raise RuntimeError(f"Unsupported platform: {system_name}")

            config = self.__load_configuration()
            logging.info("Application configuration loaded successfully.")
            self.__config_db = self.__setup_connection_from_yaml(config)
            return self

        except FileNotFoundError as file_err:
            logging.error(f"Configuration file error: {file_err}")
            raise file_err
        except yaml.YAMLError as yaml_err:
            logging.error(f"YAML parsing error in configuration file: {yaml_err}")
            raise ValueError(f"Invalid YAML in configuration file: {yaml_err}")
        except Exception as error:
            logging.error(f"Unexpected error occurred while loading configuration: {error}")
            raise error

    @staticmethod
    def __setup_connection_from_yaml(config) -> asyncpg.connection:
        """
        Sets up a connection to the database using configuration details provided in
        a YAML structure. The function expects the `config` dictionary to include
        details about the database host, port, username, password, and database name.
        Additionally, this function configures the connection pooling parameters for
        enhanced performance and reliability under concurrent access.

        :param config: The database configuration details extracted from a YAML file.
                       It is expected to include the following keys:
                       - db: A dictionary containing:
                         - username: Username for the database.
                         - password: Password for the database.
                         - host: Host address of the database.
                         - port: Port number the database is running on.
                         - database: Name of the database to connect to.
                        All values should be strings except port, which should be an integer.
        :return: An asynchronous database connection engine configured with pooling settings.
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
    def __load_yaml_file( file_path):
        """Helper method to load YAML data from a given file."""
        try:
            with open(file_path, 'r') as file:
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