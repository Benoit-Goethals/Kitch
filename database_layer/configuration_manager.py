import sys

import asyncpg.connection
import yaml
from pathlib import Path

from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import create_async_engine


import logging
import platform

from database_layer.singleton import Singleton
from sqlalchemy.pool import NullPool

class ConfigurationManager(metaclass=Singleton):
    def __init__(self):
        self.__app_config = None
        system_name = platform.system()
        if system_name == "Windows":
            logging.info("Running on Windows")
            path=Path("C:\\ProgramData\\check")
            self.__config_path = Path.joinpath(path,  "configurations/config.yml")
            if not path.exists() or not self.__config_path.exists():
              logging.error("One of 3 Configfiles is not present")
              sys.exit(1)
        elif system_name == "Linux":
            logging.info("Running on Linux")
           # self.__config_path=Path.joinpath(Path.home(),"configurations", "configurations/config.yml")
            self.__config_path = Path.joinpath(Path.home(),  "configurations/config.yml")
            if not self.__config_path.exists():
                logging.error("One of 3 Configfiles is not present")
                sys.exit(1)
        else:
            logging.info(f"Running on {system_name}")
        self.__config_db = None
        self.load()

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

    def load(self):
        try:
            config = self.__load_configuration()
            logging.info("Application configuration loaded successfully.")
            self.__config_db = self.__setup_connection_from_yaml(config)

        except Exception as error:
            logging.error(f"Failed to load configuration: {error}")



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