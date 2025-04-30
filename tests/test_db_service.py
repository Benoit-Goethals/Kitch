# tests/test_db_service.py
import pytest
from database_layer.db_service import DBService
from domain.DatabaseModelClasses import Person, Company, Address, Assignment
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


def test_read_all_persons(mocker):
    db_service = DBService()
    mock_session = mocker.patch.object(db_service, "SessionLocal")

    mock_session_instance = mock_session.return_value.__aenter__.return_value
    mock_query_result = mocker.MagicMock()
    mock_query_result.unique.return_value.scalars.return_value.all.return_value = [
        Person()
    ]

    mock_session_instance.execute.return_value = mock_query_result

    async def run_test():
        result = await db_service.get_all_persons()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], Person)

    asyncio.run(run_test())


def test_read_all_companies(mocker):
    db_service = DBService()
    mock_session = mocker.patch.object(db_service, "SessionLocal")

    mock_session_instance = mock_session.return_value.__aenter__.return_value
    mock_query_result = mocker.MagicMock()
    mock_query_result.scalars.return_value.all.return_value = [Company()]

    mock_session_instance.execute.return_value = mock_query_result

    async def run_test():
        result = await db_service.get_all_companies()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], Company)

    asyncio.run(run_test())


def test_read_all_address(mocker):
    db_service = DBService()
    mock_session = mocker.patch.object(db_service, "SessionLocal")

    mock_session_instance = mock_session.return_value.__aenter__.return_value
    mock_query_result = mocker.MagicMock()
    mock_query_result.unique.return_value.scalars.return_value.all.return_value = [
        Address()
    ]

    mock_session_instance.execute.return_value = mock_query_result

    async def run_test():
        result = await db_service.get_all_addresses()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], Address)

    asyncio.run(run_test())


def test_read_all_assignment(mocker):
    db_service = DBService()
    mock_session = mocker.patch.object(db_service, "SessionLocal")

    mock_session_instance = mock_session.return_value.__aenter__.return_value
    mock_query_result = mocker.MagicMock()
    mock_query_result.unique.return_value.scalars.return_value.all.return_value = [
        Assignment()
    ]

    mock_session_instance.execute.return_value = mock_query_result

    async def run_test():
        result = await db_service.get_all_projects()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], Assignment)

    asyncio.run(run_test())
