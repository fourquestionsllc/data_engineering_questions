You can connect to PostgreSQL in Python using your variables by combining the `database` dictionary you have with a library like **psycopg2** or **SQLAlchemy**.

Here’s an example using **psycopg2**:

```python
import os
import psycopg2

# Your database dictionary from the image
database = {
    'hostname': "sd-pe31-4x11.nam.nsroot.net",
    'password': os.getenv("DB_PASSWORD"),
    'port': 1524,
    'user': os.getenv("DB_USERNAME", "ctbot_ds_rw_mgd_dev"),
    'schema': "vectors",
    'db_name': "docsearch_dev"
}

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=database['hostname'],
        port=database['port'],
        dbname=database['db_name'],
        user=database['user'],
        password=database['password']
    )
    
    # Create a cursor to run SQL commands
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_schema();")
    print(cur.fetchall())
    
    # Close cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print("Database connection failed:", e)
```

---

If you want to **default to a specific schema** (`vectors` in your case), you can set it right after connecting:

```python
cur.execute(f"SET search_path TO {database['schema']};")
```

Do you want me to also show you a **SQLAlchemy** version so you can run queries with Pandas easily? That’s often more convenient for data science work.
