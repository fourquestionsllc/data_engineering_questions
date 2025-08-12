Here’s a simple Python example using **`psycopg2`** to list all schemas in a PostgreSQL database and their tables:

```python
import psycopg2

# Connection details
conn = psycopg2.connect(
    host="localhost",      # or your PostgreSQL server host
    port=5432,             # default PostgreSQL port
    database="your_database",
    user="your_user",
    password="your_password"
)

cur = conn.cursor()

# Get all schemas (excluding system schemas)
cur.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
    ORDER BY schema_name;
""")
schemas = cur.fetchall()

for (schema,) in schemas:
    print(f"Schema: {schema}")
    
    # Get all tables in the schema
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
        ORDER BY table_name;
    """, (schema,))
    tables = cur.fetchall()
    
    for (table,) in tables:
        print(f"  - {table}")

cur.close()
conn.close()
```

**What this does:**

* Connects to your PostgreSQL database with `psycopg2`.
* Fetches all non-system schemas from `information_schema.schemata`.
* For each schema, retrieves table names from `information_schema.tables`.
* Prints schema and table names in a nested format.

**Install requirement:**

```bash
pip install psycopg2-binary
```

If you want, I can modify this so it **also lists column names and types** for each table. That would make it a full database map.
