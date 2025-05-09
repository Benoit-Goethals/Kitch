import unittest
from unittest.mock import AsyncMock
import pytest
from src.database_layer.db_service import DBService
from src.domain.DatabaseModelClasses import Person, Company, Address, Project, Phase, OrderLine


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.db_service = DBService()

    @pytest.mark.asyncio
    async def test_fetch_addresses(self):
        # Arrange: Mock the method to return test data
        dummy_addresses = [Address(street="Main Street", postal_code="12345", municipality="City", country="BE")]
        self.db_service.get_all_addresses = AsyncMock(return_value=dummy_addresses)

        # Act: Call the method
        addresses = await self.db_service.get_all_addresses()

        # Assert: Validate the results
        self.assertIsNotNone(addresses, "Addresses should not be None")
        self.assertGreater(len(addresses), 0, "Addresses list should not be empty")
        self.assertIsInstance(addresses, list, "Result should be a list")
        self.assertEqual(addresses[0].street, "Main Street", "Street name should be 'Main Street'")

    @pytest.mark.asyncio
    async def test_fetch_projects(self):
        # Arrange: Mock the method to return test data
        dummy_projects = [Project(project_id=1, client_id=2, projectleader=3, date_start="2023-01-01")]
        self.db_service.get_all_projects = AsyncMock(return_value=dummy_projects)

        # Act
        projects = await self.db_service.get_all_projects()

        # Assert
        self.assertIsNotNone(projects, "Projects should not be None")
        self.assertGreater(len(projects), 0, "Projects list should not be empty")
        self.assertIsInstance(projects, list, "Result should be a list")
        self.assertEqual(projects[0].project_id, 1, "Project ID should be 1")

    @pytest.mark.asyncio
    async def test_fetch_companies(self):
        # Arrange
        dummy_companies = [Company(company_name="Tech Corp")]
        self.db_service.get_all_companies = AsyncMock(return_value=dummy_companies)

        # Act
        companies = await self.db_service.get_all_companies()

        # Assert
        self.assertIsNotNone(companies, "Companies should not be None")
        self.assertGreater(len(companies), 0, "Companies list should not be empty")
        self.assertIsInstance(companies, list, "Result should be a list")
        self.assertEqual(companies[0].company_name, "Tech Corp", "Company name should be 'Tech Corp'")

    @pytest.mark.asyncio
    async def test_fetch_phases(self):
        # Arrange
        dummy_phases = [Phase(phase_id=1, project_id=2, sub_name="Phase 1")]
        self.db_service.get_all_phases = AsyncMock(return_value=dummy_phases)

        # Act
        phases = await self.db_service.get_all_phases()

        # Assert
        self.assertIsNotNone(phases, "Phases should not be None")
        self.assertGreater(len(phases), 0, "Phases list should not be empty")
        self.assertIsInstance(phases, list, "Result should be a list")
        self.assertEqual(phases[0].sub_name, "Phase 1", "Phase name should be 'Phase 1'")

    @pytest.mark.asyncio
    async def test_fetch_order_line(self):
        # Arrange
        dummy_order_lines = [OrderLine(orderline_id=11, phase_id=1, amount=10, sales_price=100)]
        self.db_service.get_all_order_lines = AsyncMock(return_value=dummy_order_lines)

        # Act
        order_lines = await self.db_service.get_all_order_lines()

        # Assert
        self.assertIsNotNone(order_lines, "Order lines should not be None")
        self.assertGreater(len(order_lines), 0, "Order lines list should not be empty")
        self.assertIsInstance(order_lines, list, "Result should be a list")
        self.assertEqual(order_lines[0].orderline_id, 11, "Order line ID should be 11")

    @pytest.mark.asyncio
    async def test_fetch_persons(self):
        # Arrange
        dummy_persons = [Person(name_first="John", name_last="Doe", email="john.doe@example.com")]
        self.db_service.get_all_persons = AsyncMock(return_value=dummy_persons)

        # Act
        persons = await self.db_service.get_all_persons()

        # Assert
        self.assertIsNotNone(persons, "Persons should not be None")
        self.assertGreater(len(persons), 0, "Persons list should not be empty")
        self.assertIsInstance(persons, list, "Result should be a list")
        self.assertEqual(persons[0].name_first, "John", "First name should be 'John'")
        self.assertEqual(persons[0].email, "john.doe@example.com", "Email should be 'john.doe@example.com'")

    @pytest.mark.asyncio
    async def test_fetch_postcodes(self):
        # Arrange
        dummy_postcodes = ["12345", "67890"]
        self.db_service.get_all_postcodes = AsyncMock(return_value=dummy_postcodes)

        # Act
        postcodes = await self.db_service.get_all_postcodes()

        # Assert
        self.assertIsNotNone(postcodes, "Postcodes should not be None")
        self.assertGreater(len(postcodes), 0, "Postcodes list should not be empty")
        self.assertIsInstance(postcodes, list, "Result should be a list")
        self.assertIn("12345", postcodes, "Postcodes list should contain '12345'")


if __name__ == "__main__":
    unittest.main()