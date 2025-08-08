To **list all databases in PostgreSQL** using **SQLAlchemy**, you can execute a raw SQL query through an engine connection — since PostgreSQL doesn’t expose database metadata through SQLAlchemy's ORM or core API directly.

---

## ✅ Example: Show All Databases in PostgreSQL via SQLAlchemy

```python
from sqlalchemy import create_engine, text

# Create engine (connect to *any* existing database, like "postgres")
engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/postgres")

with engine.connect() as conn:
    result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
    databases = [row[0] for row in result]
    print(databases)
```

---

### 🔍 Explanation:

* `pg_database` is a system catalog table in PostgreSQL.
* `datistemplate = false` filters out template databases like `template0` and `template1`.

---

## 🧠 Notes

* You must connect to an **existing database** (usually `postgres`) to query `pg_database`. You can't connect without specifying a DB in PostgreSQL.
* If you connect to a user-defined database, the query still works.

---

Let me know if you'd like to show more system info (e.g., schemas, tables, users) using SQLAlchemy!
