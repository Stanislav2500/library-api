import os
import pytest
import psycopg2
from app import create_app

TEST_DB_CONFIG = {
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": int(os.environ.get("POSTGRES_PORT", "5432")),
    "database": os.environ.get("POSTGRES_DB", "library_test_db"),
    "user": os.environ.get("POSTGRES_USER", "postgres"),
    "password": os.environ.get("POSTGRES_PASSWORD", "secret"),
}

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(**TEST_DB_CONFIG)
    conn.autocommit = True
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def setup_database(db_connection):
    cur = db_connection.cursor()
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
    cur.execute("CREATE SCHEMA public")
    cur.execute("""
        CREATE TABLE authors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author_id INTEGER REFERENCES authors(id),
            status VARCHAR(20) DEFAULT 'available'
        )
    """)
    cur.execute("INSERT INTO authors (name) VALUES ('John Doe'), ('Jane Smith')")
    cur.execute("INSERT INTO books (title, author_id, status) VALUES ('Book 1', 1, 'available'), ('Book 2', 2, 'checked-out')")
    cur.close()