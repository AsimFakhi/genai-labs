from pathlib import Path
import sqlite3
import json

# ---------------------------------------------------------------------
# Database Location
# ---------------------------------------------------------------------
DB_PATH = Path("src/shared/data/enterprise_data_mart.db")

def get_connection():
    """Return a SQLite connection."""
    return sqlite3.connect(DB_PATH)

def validate_sql(sql: str):
    """Only allow read-only SQL."""
    sql = sql.strip().lower()
    if not sql.startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")

# ---------------------------------------------------------------------
# Tool 1: Execute Read-Only SQL
# ---------------------------------------------------------------------
def execute_read_only_sql(sql: str):
    """
    Execute a read-only SQL query.
    Returns JSON string of results, or error message if query fails.
    """
    try:
        validate_sql(sql)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return json.dumps(results, indent=4, default=str)

    except Exception as e:
        return f"SQL Error: {str(e)}"

# ---------------------------------------------------------------------
# Tool 2: Get Database Schema (JSON FORMAT)
# ---------------------------------------------------------------------
def get_database_schema() -> str:
    """
    Read the SQLite database schema and return as structured JSON.
    
    Returns
    -------
    str
        JSON string with tables, columns, foreign keys, and indexes.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema = {
        "database": str(DB_PATH.name),
        "tables": []
    }

    # Get all user tables
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        table_info = {
            "table_name": table_name,
            "columns": [],
            "foreign_keys": [],
            "primary_key": []
        }

        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for column in columns:
            col_data = {
                "column_name": column[1],
                "data_type": column[2],
                "not_null": bool(column[3]),
                "default_value": column[4],
                "is_primary_key": bool(column[5])
            }
            table_info["columns"].append(col_data)
            if col_data["is_primary_key"]:
                table_info["primary_key"].append(col_data["column_name"])

        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()

        for fk in foreign_keys:
            fk_data = {
                "column": fk[3],           # local column name
                "references_table": fk[2],  # referenced table
                "references_column": fk[4]  # referenced column
            }
            table_info["foreign_keys"].append(fk_data)

        schema["tables"].append(table_info)

    conn.close()

    return json.dumps(schema, indent=4)


# ---------------------------------------------------------------------
# Tool Metadata (for LLM)
# ---------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "name": "get_database_schema",
        "description": (
            "Returns the SQLite database schema as structured JSON including "
            "all tables, columns, data types, primary keys, and foreign key "
            "relationships. Use this FIRST before writing any SQL to understand "
            "the exact table and column names."
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
            "Executes a read-only SQL SELECT query against the SQLite database. "
            "Always check the schema first to know correct table and column names."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "A valid SELECT SQL query."
                }
            },
            "required": ["sql"]
        }
    }
]

# ---------------------------------------------------------------------
# Tool Registry (for Python)
# ---------------------------------------------------------------------
TOOLS_MAP = {
    "get_database_schema": get_database_schema,
    "execute_read_only_sql": execute_read_only_sql,
}