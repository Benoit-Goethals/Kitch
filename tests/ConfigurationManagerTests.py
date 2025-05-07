import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import platform
import yaml

from database_layer.configuration_manager import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):

    def test_load_configuration(self):
         self.assertIsNotNone(ConfigurationManager().load("config_test.yml").config_db)

    def test_load_raises_file_not_found_error(self):
      with self.assertRaises(FileNotFoundError):
           ConfigurationManager().load("config_test_not_found.yml")


if __name__ == "__main__":
    unittest.main()