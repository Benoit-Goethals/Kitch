import asyncpg.connection
import yaml
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine


import logging
import platform

from src.database_layer.singleton import Singleton


class ConfigurationManager(metaclass=Singleton):
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
        try:
            system_name = platform.system()
            if file_name is not None:
                self.__config_path = Path.joinpath(self.__get_project_root(), "src","configurations", file_name)
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