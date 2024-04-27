import asyncpg
import requests
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'pharmacy_service/app'))
sys.path.append(str(BASE_DIR / 'pharmacy_api_service/app'))

from pharmacy_service.app.main import service_alive as pharmacy_status
from pharmacy_api_service.app.main import service_alive as pharmacy_api_status

@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

@pytest.mark.asyncio
async def test_pharmacy_service_connection():
    r = await pharmacy_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_pharmacy_api_service_connection():
    r = await pharmacy_api_status()
    assert r == {'message': 'service alive'}
