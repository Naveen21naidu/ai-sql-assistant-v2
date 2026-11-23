import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "sample.db"

CREATE_CUSTOMERS = """
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    city        TEXT NOT NULL
);
"""

CREATE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL,
    price      REAL NOT NULL CHECK (price >= 0)
);
"""

CREATE_ORDERS = """
CREATE TABLE IF NOT EXISTS Orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    order_date  TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
    FOREIGN KEY (product_id)  REFERENCES Products (product_id)
);
"""


def create_database() -> None:
    """
    Create the SQLite database and all required tables.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(
            CREATE_CUSTOMERS + CREATE_PRODUCTS + CREATE_ORDERS
        )
        conn.commit()

    print(f"Database created at: {DB_PATH}")


if __name__ == "__main__":
    create_database()