import pytest
import sqlite3
from billing.repos.database import get_connection, init_db

@pytest.fixture(autouse=True)
def setup_test_db():

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS subscriptions")
        cursor.execute("DROP TABLE IF EXISTS plans")
        cursor.execute("DROP TABLE IF EXISTS customers")

        conn.commit()

    init_db()

    yield

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS subscriptions")
        cursor.execute("DROP TABLE IF EXISTS plans")
        cursor.execute("DROP TABLE IF EXISTS customers")

        conn.commit()

