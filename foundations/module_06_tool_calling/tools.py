"""
Module 06 - Tool Calling

This file contains everything related to Tools.

A Tool consists of two parts:

1. A Python function
   -----------------
   This is the actual implementation that performs work.

2. Tool Metadata
   -----------------
   This is the information sent to the LLM describing:
   - Tool name
   - What it does
   - What arguments it accepts

The LLM NEVER sees the Python code.

It only sees the metadata.

When the model decides to use a tool, our application
looks up the Python function and executes it.
"""

from pathlib import Path
import sqlite3
import json

# ---------------------------------------------------------------------
# Database Location
# ---------------------------------------------------------------------

# Reuse the shared database created by sample_data.py.
# Keeping the path here makes it easy to reuse later when
# we add SQL execution.

DB_PATH = Path("src/shared/data/enterprise_data_mart.db")

def get_connection():
    """
    Return a SQLite connection.
    """

    return sqlite3.connect(DB_PATH)

def validate_sql(sql: str):
    """
    Only allow read-only SQL.
    """

    sql = sql.strip().lower()

    if not sql.startswith("select"):
        raise ValueError(
            "Only SELECT statements are allowed."
        )


# ---------------------------------------------------------------------
# Tool 1
# ---------------------------------------------------------------------
def execute_read_only_sql(sql: str):
    """
    Execute a read-only SQL query.
    """

    validate_sql(sql)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    columns = [
        column[0]
        for column in cursor.description
    ]

    rows = cursor.fetchall()
    conn.close()
    results = []

    for row in rows:
        results.append(
            dict(zip(columns, row))
        )

    return json.dumps(
        results,
        indent=4,
        default=str
    )

def get_database_schema() -> str:
    """
    Read the SQLite database schema.

    Returns
    -------
    str
        A formatted string describing all tables and columns.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema = []

    # Get all user tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        schema.append(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for column in columns:
            column_name = column[1]
            data_type = column[2]
            schema.append(
                f"   • {column_name} ({data_type})"
            )

    conn.close()

    return "\n".join(schema)


# ---------------------------------------------------------------------
# Tool Metadata
# ---------------------------------------------------------------------

"""
This metadata is what gets sent to the LLM.

Notice that we are NOT sending Python.

We are describing the tool so the model knows:

• Tool name
• Purpose
• Required parameters

The Responses API uses this information to decide
whether the tool should be called.
"""

TOOLS = [

    {
        "type": "function",

        "name": "get_database_schema",

        "description": (
            "Returns the SQLite database schema including "
            "all tables and columns."
        ),

        "parameters": {

            "type": "object",

            "properties": {},

            "required": []

        }
    },
    {
        "type": "function",
        "name": "execute_read_only_sql",
        "description": (
            "Executes a read-only SQL SELECT query "
            "against the SQLite database."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "A valid SELECT SQL query."
                }
            },
            "required": [
                "sql"
            ]
        }
    }
]


# ---------------------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------------------

"""
TOOLS_MAP is for Python.

TOOLS is for the LLM.

The model says:

"I want get_database_schema."

Python looks inside TOOLS_MAP and finds the matching
function to execute.

As we add more tools, we simply extend this dictionary.

Example:

TOOLS_MAP = {
    "get_database_schema": get_database_schema,
    "execute_read_only_sql": execute_read_only_sql,
    "get_customer": get_customer
}
"""

TOOLS_MAP = {

    "get_database_schema": get_database_schema,
    "execute_read_only_sql": execute_read_only_sql,

}

# Actual DB Schema
# The LLM never sees this code.
# It only sees the tool description.
# def get_database_schema():
#     """
#     Returns the database schema.
#     """
#     return """
#     Table:
#     costomers
#     accounts
#     transactions
#     merchants
#     transaction_types

#     Relationships

#     customer.customer_id -> accounts.customer_id

#     accounts.account_id -> transaction.account_id
    
#     merchant.merchat_id -> transaction.merchant_id

#     transaction_types.transaction_type_id -> stransaction.transaction_type_id
# """