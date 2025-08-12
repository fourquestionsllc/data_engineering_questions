Here’s a Python example using `psycopg2` to:

1. Connect to PostgreSQL
2. List all schemas in a database
3. List all tables in each schema
4. Query the first 3 rows of each table as examples

```python
import psycopg2
from psycopg2 import sql

# Database connection config
db_config = {
    "host": "localhost",
    "port": 5432,
    "dbname": "your_database",
    "user": "your_username",
    "password": "your_password"
}

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Get all schemas (excluding system schemas)
    cur.execute("""
        SELECT schema_name 
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
        ORDER BY schema_name;
    """)
    schemas = [row[0] for row in cur.fetchall()]

    for schema in schemas:
        print(f"\nSchema: {schema}")

        # Get all tables in the schema
        cur.execute(sql.SQL("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            ORDER BY table_name;
        """), [schema])
        tables = [row[0] for row in cur.fetchall()]

        for table in tables:
            print(f"  Table: {table}")

            # Get first 3 rows as examples
            try:
                query = sql.SQL("SELECT * FROM {}.{} LIMIT 3").format(
                    sql.Identifier(schema),
                    sql.Identifier(table)
                )
                cur.execute(query)
                rows = cur.fetchall()

                # Print rows
                for row in rows:
                    print(f"    {row}")
                if not rows:
                    print("    (empty table)")
            except Exception as e:
                print(f"    Error reading table: {e}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Database connection failed: {e}")
```

**Notes:**

* Replace the `db_config` values with your own PostgreSQL connection details.
* It skips system schemas (`pg_catalog`, `information_schema`).
* Uses `psycopg2.sql.Identifier` to safely inject schema/table names.
* Gracefully handles empty tables or permission errors.

If you want, I can extend this so that the **column names** are also printed along with the 3 example rows for clarity. That way you’d see something like a small preview table instead of just tuples.
