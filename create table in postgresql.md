You can do this with Python using either **SQLAlchemy** or **psycopg2**.
The cleanest approach is to use **pandas**’ `.to_sql()` along with SQLAlchemy — it creates the table automatically from your DataFrame schema and inserts the data in one go.

---

### **Option 1: Using Pandas + SQLAlchemy (Recommended)**

```python
import pandas as pd
from sqlalchemy import create_engine

# Example DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})

# PostgreSQL connection details
user = "your_username"
password = "your_password"
host = "localhost"  # or your DB host
port = "5432"
database = "your_database"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# Write DataFrame to table (creates table if not exists)
df.to_sql("my_table", engine, index=False, if_exists="replace")  
# if_exists options: 'fail', 'replace', 'append'

print("Table created and data inserted successfully.")
```

**Why use this?**

* Automatically creates the table with matching column types.
* Easy to append or replace data.
* No need to manually write SQL for table creation.

---

### **Option 2: Using psycopg2 (Manual table creation & insert)**

If you want **more control** over schema or indexes:

```python
import psycopg2
import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="your_database",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table manually
cur.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INT,
        name TEXT,
        age INT
    )
""")

# Insert rows
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO my_table (id, name, age) VALUES (%s, %s, %s)",
        (row['id'], row['name'], row['age'])
    )

conn.commit()
cur.close()
conn.close()
print("Table created and data inserted successfully.")
```

---

✅ **Recommendation**
If you just want to quickly get a DataFrame into PostgreSQL — use **pandas + SQLAlchemy** (`.to_sql`).
If you need schema control, constraints, or performance tuning — use **psycopg2** with `COPY` for bulk inserts.

---
