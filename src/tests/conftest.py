import pytest
import sqlite3
from billing.repos.database import get_connection, init_db

@pytest.fixture(autouse=True)
def setup_test_db():
    
    init_db()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")
        conn.commit()

    yield

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")
        conn.commit()

