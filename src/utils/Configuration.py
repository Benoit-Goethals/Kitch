import logging
import platform
import shutil
from pathlib import Path

class Configuration:
    __logger = logging.getLogger(__name__)

    @classmethod
    def configuration_files_check(cls):
        system_name = platform.system()
        if not system_name:
            cls.__logger.error(f"Unsupported platform: {system_name}")
            return
        cls.log_message(f"Running on {system_name}", "info")

        base_path, config_path, src_path = cls.get_paths(system_name)
        if  not base_path.exists():
            if not cls.create_directories(base_path):
                cls.log_message("Error creating directories. Please check the permissions.", "error")
                return
            else:
                cls.copy_configuration_file(src_path, config_path)

    @classmethod
    def get_paths(cls, system_name):
        if system_name == "Windows":
            base_path = Path("C:\\ProgramData\\Kitch")
        elif system_name == "Linux":
            base_path = Path.home() / "configurations"
        else:
            return None, None, None
        
        config_path = base_path / "configurations" / "config.yml"
        src_path = Path("src/configurations/config.yml")
        return base_path, config_path, src_path

    @classmethod
    def log_message(cls, message, level):
        if level == "info":
            cls.__logger.info(message)
        elif level == "error":
            cls.__logger.error(message)

    @classmethod
    def create_directories(cls, base_path):
        try:
            Path(base_path / "configurations").mkdir(parents=True, exist_ok=True)
            Path(base_path / "photos").mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            cls.log_message(f"Error creating directories at {base_path}: {e}", "error")
            return False

    @classmethod
    def copy_configuration_file(cls, src_path, dest_path):
        try:
            shutil.copy(src_path, dest_path)
            cls.log_message(f"Configuration file copied from {src_path} to {dest_path}", "info")
        except FileNotFoundError:
            cls.log_message(f"Source configuration file not found at {src_path}. Please check the source path.", "error")
        except Exception as e:
            cls.log_message(f"Unexpected error while copying configuration file: {e}", "error")