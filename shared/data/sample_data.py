import random
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent / "enterprise_data_mart.db"

# -------------------------------
# Sample Master Data
# -------------------------------

CUSTOMERS = [
    ("John", "Smith", "Mumbai", "Retail"),
    ("Sarah", "Brown", "Pune", "Premium"),
    ("David", "Lee", "Delhi", "Business"),
    ("Emily", "Johnson", "Bangalore", "Retail"),
    ("Michael", "Patel", "Ahmedabad", "Premium"),
    ("Priya", "Sharma", "Mumbai", "Retail"),
    ("Rahul", "Verma", "Delhi", "Business"),
    ("Sneha", "Kulkarni", "Pune", "Premium"),
    ("Arjun", "Mehta", "Hyderabad", "Retail"),
    ("Neha", "Singh", "Chennai", "Retail"),
]

MERCHANTS = [
    ("Amazon", "E-Commerce"),
    ("Reliance Fresh", "Groceries"),
    ("Starbucks", "Food & Beverage"),
    ("Uber", "Transport"),
    ("Netflix", "Entertainment"),
    ("Swiggy", "Food Delivery"),
    ("Air India", "Travel"),
    ("Apple", "Electronics"),
    ("HP Petrol Pump", "Fuel"),
    ("Electricity Board", "Utilities"),
]

TRANSACTION_TYPES = [
    "Debit",
    "Credit",
    "Refund",
    "Transfer",
    "Interest",
    "Fee",
]

DESCRIPTIONS = [
    "Grocery Shopping",
    "Online Purchase",
    "Coffee",
    "Salary Credit",
    "Flight Booking",
    "Electricity Bill",
    "Fuel Payment",
    "Movie Tickets",
    "Restaurant",
    "ATM Withdrawal",
]