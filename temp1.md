You can do that easily by combining **`psycopg2`** with **`pandas.read_sql`** so you don’t have to manually `fetchall()` and convert.

Here’s the updated version:

```python
import psycopg2
from psycopg2 import sql
import pandas as pd

# Connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="your_database",
    user="your_user",
    password="your_password"
)

# Parameters
schema_name = "my_schema"
table_name = "my_table"

# Build the query safely
query = sql.SQL("SELECT * FROM {}.{}").format(
    sql.Identifier(schema_name),
    sql.Identifier(table_name)
)

# Execute and load into DataFrame
df = pd.read_sql(query.as_string(conn), conn)

print(df.head())

conn.close()
```

**Why this works well:**

* `pandas.read_sql()` automatically reads the query results directly into a DataFrame.
* `.as_string(conn)` turns the `psycopg2.sql` object into a proper SQL string for pandas to run.
* This keeps it safe for dynamic schema/table names.

If you want to also **filter, sort, or limit rows dynamically**, you can still build the query with `sql.SQL()` and add parameters.

Do you want me to make a **version that takes db, schema, table, and optional WHERE clause** as arguments and returns a DataFrame? That would make it reusable.
