import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

# Makes generated data reproducible
random.seed(42)

DB_PATH = Path(__file__).resolve().parent / "sample.db"

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Daniel",
    "Lisa", "Matthew", "Nancy", "Anthony", "Betty", "Mark", "Margaret",
    "Donald", "Sandra", "Steven", "Ashley", "Paul", "Kimberly", "Andrew",
    "Emily", "Joshua", "Donna", "Kenneth", "Michelle", "Kevin", "Dorothy",
    "Brian", "Carol", "George", "Amanda", "Timothy", "Melissa", "Ronald",
    "Deborah",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts",
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "Indianapolis", "Seattle", "Denver",
    "Boston", "Nashville", "Portland", "Las Vegas", "Detroit", "Memphis",
    "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno",
]

PRODUCT_CATALOG = [
    ("Wireless Mouse", "Electronics", 29.99),
    ("Mechanical Keyboard", "Electronics", 89.99),
    ("USB-C Hub", "Electronics", 45.50),
    ("Bluetooth Speaker", "Electronics", 59.99),
    ("Noise Cancelling Headphones", "Electronics", 199.99),
    ("4K Monitor", "Electronics", 349.99),
    ("Laptop Stand", "Electronics", 39.99),
    ("Webcam HD", "Electronics", 79.99),
    ("External SSD 1TB", "Electronics", 129.99),
    ("Smart Watch", "Electronics", 249.99),
    ("Running Shoes", "Sports", 119.99),
    ("Yoga Mat", "Sports", 34.99),
    ("Dumbbell Set", "Sports", 149.99),
    ("Tennis Racket", "Sports", 89.99),
    ("Cycling Helmet", "Sports", 54.99),
    ("Camping Tent", "Sports", 179.99),
    ("Hiking Backpack", "Sports", 69.99),
    ("Fitness Tracker", "Sports", 99.99),
    ("Basketball", "Sports", 29.99),
    ("Swim Goggles", "Sports", 19.99),
    ("Coffee Maker", "Home", 79.99),
    ("Blender", "Home", 49.99),
    ("Air Fryer", "Home", 99.99),
    ("Vacuum Cleaner", "Home", 189.99),
    ("Bed Sheet Set", "Home", 59.99),
    ("Desk Lamp", "Home", 34.99),
    ("Wall Clock", "Home", 24.99),
    ("Storage Baskets", "Home", 29.99),
    ("Cookware Set", "Home", 149.99),
    ("Electric Kettle", "Home", 39.99),
    ("Fantasy Novel", "Books", 14.99),
    ("Science Textbook", "Books", 79.99),
    ("Cookbook", "Books", 24.99),
    ("Biography", "Books", 18.99),
    ("Children's Storybook", "Books", 12.99),
    ("History Atlas", "Books", 34.99),
    ("Poetry Collection", "Books", 16.99),
    ("Business Guide", "Books", 22.99),
    ("Language Learning Kit", "Books", 49.99),
    ("Graphic Novel", "Books", 19.99),
    ("Denim Jeans", "Clothing", 59.99),
    ("Cotton T-Shirt", "Clothing", 19.99),
    ("Winter Jacket", "Clothing", 129.99),
    ("Running Shorts", "Clothing", 34.99),
    ("Leather Belt", "Clothing", 39.99),
    ("Wool Sweater", "Clothing", 69.99),
    ("Dress Shirt", "Clothing", 49.99),
    ("Sneakers", "Clothing", 89.99),
    ("Baseball Cap", "Clothing", 24.99),
    ("Socks Pack", "Clothing", 14.99),
]

CUSTOMER_COUNT = 100
PRODUCT_COUNT = 50
ORDER_COUNT = 1000


def _random_email(first: str, last: str, index: int) -> str:
    """Generate a unique-looking email."""
    domains = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "icloud.com",
        "mail.com",
    ]
    return f"{first.lower()}.{last.lower()}{index}@{random.choice(domains)}"


def _random_order_date() -> str:
    """Generate a random order date."""
    start = date(2023, 1, 1)
    end = date(2025, 12, 31)
    return (
        start +
        timedelta(days=random.randint(0, (end - start).days))
    ).isoformat()


def seed_customers(conn: sqlite3.Connection) -> None:
    """Insert random customers."""
    used_emails = set()
    rows = []

    for i in range(1, CUSTOMER_COUNT + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        email = _random_email(first, last, i)

        while email in used_emails:
            email = _random_email(
                first,
                last,
                i + random.randint(100, 999)
            )

        used_emails.add(email)

        rows.append((
            i,
            f"{first} {last}",
            email,
            random.choice(CITIES)
        ))

    conn.executemany(
        """
        INSERT INTO Customers
        VALUES (?, ?, ?, ?);
        """,
        rows,
    )


def seed_products(conn: sqlite3.Connection) -> None:
    """Insert products."""

    rows = []

    for product_id, (name, category, price) in enumerate(
        PRODUCT_CATALOG[:PRODUCT_COUNT],
        start=1
    ):

        price = max(
            0.99,
            round(price + random.uniform(-5, 5), 2)
        )

        rows.append(
            (
                product_id,
                name,
                category,
                price
            )
        )

    conn.executemany(
        """
        INSERT INTO Products
        VALUES (?, ?, ?, ?);
        """,
        rows,
    )


def seed_orders(conn: sqlite3.Connection) -> None:
    """Insert random orders."""

    rows = []

    for order_id in range(1, ORDER_COUNT + 1):

        rows.append((
            order_id,
            random.randint(1, CUSTOMER_COUNT),
            random.randint(1, PRODUCT_COUNT),
            random.randint(1, 5),
            _random_order_date(),
        ))

    conn.executemany(
        """
        INSERT INTO Orders
        VALUES (?, ?, ?, ?, ?);
        """,
        rows,
    )


def seed_database() -> None:
    """Populate the SQLite database."""

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("PRAGMA foreign_keys = ON;")

        # Clear previous data
        conn.execute("DELETE FROM Orders;")
        conn.execute("DELETE FROM Products;")
        conn.execute("DELETE FROM Customers;")

        seed_customers(conn)
        seed_products(conn)
        seed_orders(conn)

        conn.commit()

    print(f"Seeded database at: {DB_PATH}")
    print(f"Customers : {CUSTOMER_COUNT}")
    print(f"Products  : {PRODUCT_COUNT}")
    print(f"Orders    : {ORDER_COUNT}")


if __name__ == "__main__":
    seed_database()