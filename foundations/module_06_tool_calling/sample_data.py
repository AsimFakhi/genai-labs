import random
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path("src/shared/data/enterprise_data_mart.db")


def create_database():
    """Create the SQLite database and populate it with sample data."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------------------------------------------
    # Drop existing tables
    # ---------------------------------------------------

    cursor.executescript("""
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS merchants;
    DROP TABLE IF EXISTS transaction_types;
    """)

    # ---------------------------------------------------
    # Create tables
    # ---------------------------------------------------

    cursor.executescript("""

    CREATE TABLE customers(
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        city TEXT,
        segment TEXT
    );

    CREATE TABLE accounts(
        account_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        account_type TEXT,
        balance REAL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE merchants(
        merchant_id INTEGER PRIMARY KEY,
        merchant_name TEXT,
        category TEXT
    );

    CREATE TABLE transaction_types(
        transaction_type_id INTEGER PRIMARY KEY,
        transaction_type TEXT
    );

    CREATE TABLE transactions(
        transaction_id INTEGER PRIMARY KEY,
        account_id INTEGER,
        merchant_id INTEGER,
        transaction_type_id INTEGER,
        amount REAL,
        transaction_date TEXT,
        description TEXT,

        FOREIGN KEY(account_id) REFERENCES accounts(account_id),
        FOREIGN KEY(merchant_id) REFERENCES merchants(merchant_id),
        FOREIGN KEY(transaction_type_id)
            REFERENCES transaction_types(transaction_type_id)
    );

    """)

    # ---------------------------------------------------
    # Customers
    # ---------------------------------------------------

    customers = [
        ("John", "Smith", "Mumbai", "Retail"),
        ("Sarah", "Brown", "Pune", "Premium"),
        ("David", "Lee", "Delhi", "Retail"),
        ("Emily", "Johnson", "Bangalore", "Premium"),
        ("Michael", "Patel", "Ahmedabad", "Business"),
        ("Amit", "Shah", "Mumbai", "Retail"),
        ("Neha", "Joshi", "Pune", "Premium"),
        ("Priya", "Singh", "Delhi", "Retail"),
        ("Rahul", "Verma", "Hyderabad", "Business"),
        ("Karan", "Kapoor", "Mumbai", "Premium"),
    ]

    cursor.executemany("""
        INSERT INTO customers
        (first_name,last_name,city,segment)
        VALUES (?,?,?,?)
    """, customers)

    # ---------------------------------------------------
    # Accounts
    # ---------------------------------------------------

    account_types = ["Savings", "Current"]

    for customer_id in range(1, 11):
        cursor.execute("""
            INSERT INTO accounts(customer_id,account_type,balance)
            VALUES (?,?,?)
        """, (
            customer_id,
            random.choice(account_types),
            round(random.uniform(5000, 200000), 2)
        ))

    # ---------------------------------------------------
    # Merchants
    # ---------------------------------------------------

    merchants = [
        ("Amazon", "Shopping"),
        ("Uber", "Transport"),
        ("Starbucks", "Food"),
        ("Netflix", "Entertainment"),
        ("Reliance Fresh", "Groceries"),
        ("Swiggy", "Food"),
        ("Zomato", "Food"),
        ("Apple", "Electronics"),
        ("Air India", "Travel"),
        ("Electricity Board", "Utilities"),
    ]

    cursor.executemany("""
        INSERT INTO merchants(merchant_name,category)
        VALUES (?,?)
    """, merchants)

    # ---------------------------------------------------
    # Transaction Types
    # ---------------------------------------------------

    types = [
        ("Debit",),
        ("Credit",),
        ("Refund",),
        ("Transfer",),
        ("Interest",),
    ]

    cursor.executemany("""
        INSERT INTO transaction_types(transaction_type)
        VALUES (?)
    """, types)

    # ---------------------------------------------------
    # Transactions
    # ---------------------------------------------------

    descriptions = [
        "Coffee",
        "Groceries",
        "Flight Booking",
        "Movie Tickets",
        "Fuel",
        "Electricity Bill",
        "Restaurant",
        "Electronics",
        "Salary",
        "Online Shopping"
    ]

    for _ in range(300):

        days = random.randint(0, 180)

        cursor.execute("""
            INSERT INTO transactions(
                account_id,
                merchant_id,
                transaction_type_id,
                amount,
                transaction_date,
                description
            )
            VALUES (?,?,?,?,?,?)
        """, (
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 5),
            round(random.uniform(100, 25000), 2),
            (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d"),
            random.choice(descriptions)
        ))

    conn.commit()
    conn.close()

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()