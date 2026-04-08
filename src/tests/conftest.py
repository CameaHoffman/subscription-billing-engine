import pytest
import sqlite3
from billing.repos.database import get_connection

@pytest.fixture(autouse=True)
def setup_test_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")
        conn.commit()

    yield

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")
        conn.commit()

