Great! You can combine schema/table discovery with querying and displaying the top 3 rows from **each table** into **Pandas DataFrames**.

---

## ✅ Full Example: Show Top 3 Rows per Table (per Schema) in DataFrames

```python
from sqlalchemy import create_engine, inspect, text
import pandas as pd

# Database connection URL
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/your_db_name"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create inspector
inspector = inspect(engine)

# Get all schemas (excluding system schemas)
schemas = [s for s in inspector.get_schema_names() if not s.startswith("pg_") and s != "information_schema"]

# Store results in a dictionary of DataFrames
dataframes = {}

with engine.connect() as conn:
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)

        for table in tables:
            try:
                qualified_name = f'"{schema}"."{table}"'  # quote identifiers to handle case sensitivity
                query = text(f'SELECT * FROM {qualified_name} LIMIT 3')

                df = pd.read_sql(query, conn)
                key = f"{schema}.{table}"
                dataframes[key] = df

                print(f"\n📄 {key} (Top 3 rows):")
                print(df)

            except Exception as e:
                print(f"⚠️ Failed to query {schema}.{table}: {e}")
```

---

## ✅ Output

This will:

* Discover all non-system schemas
* Get all tables in each schema
* Query `SELECT * FROM schema.table LIMIT 3`
* Load results into a `pandas.DataFrame`
* Print them, and store them in a dictionary `dataframes` for further use

---

## 🧠 Notes

* Using double quotes (`"schema"."table"`) handles special characters or capitalized names.
* If a table has no rows, the DataFrame will be empty.
* You can access each result by `dataframes["schema.table_name"]`.

---

Let me know if you want to:

* Export the results to CSV
* Include column names/types
* Use async or SQLAlchemy ORM instead
