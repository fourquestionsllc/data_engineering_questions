To **show all schemas** in a PostgreSQL database and **list all tables** within each schema using **Python and SQLAlchemy**, you can use the `inspect()` function from SQLAlchemy.

---

## ✅ Full Example Using SQLAlchemy

```python
from sqlalchemy import create_engine, inspect

# Replace with your DB credentials
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/your_db_name"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create inspector
inspector = inspect(engine)

# Get all schemas
schemas = inspector.get_schema_names()

print("Schemas and their tables:")
for schema in schemas:
    # Skip PostgreSQL internal schemas if you want
    if schema.startswith("pg_") or schema in ("information_schema",):
        continue

    # Get all tables for the schema
    tables = inspector.get_table_names(schema=schema)
    print(f"\nSchema: {schema}")
    for table in tables:
        print(f"  - {table}")
```

---

## 🧠 Notes

* **`get_schema_names()`**: Lists all schemas in the database.
* **`get_table_names(schema='your_schema')`**: Lists all tables in a specific schema.
* PostgreSQL includes internal schemas like:

  * `pg_catalog`
  * `information_schema`
    You can skip them unless you explicitly need them.

---

## ✅ Example Output

```
Schemas and their tables:

Schema: public
  - users
  - posts

Schema: vectors
  - embeddings
  - metadata
```

---

Would you also like to list **views** or **columns per table**? That’s also possible with the inspector.
