For **async Python**, the most popular and performant PostgreSQL library is [`asyncpg`](https://github.com/MagicStack/asyncpg).

---

## ✅ Step-by-Step: Using `asyncpg`

### 1. **Install `asyncpg`**

```bash
pip install asyncpg
```

---

### 2. **Basic Async Query Example**

```python
import asyncio
import asyncpg

async def fetch_data():
    # Connect to the PostgreSQL database
    conn = await asyncpg.connect(
        user='your_username',
        password='your_password',
        database='your_db_name',
        host='your_host',    # e.g., 'localhost'
        port=5432
    )

    try:
        # Execute a query
        rows = await conn.fetch('SELECT * FROM your_table_name;')

        # Print results
        for row in rows:
            print(dict(row))  # convert Record to dict
    finally:
        # Always close the connection
        await conn.close()

# Run the async function
asyncio.run(fetch_data())
```

---

### 3. **Inserting Data Example**

```python
await conn.execute(
    'INSERT INTO your_table_name(column1, column2) VALUES($1, $2)',
    'value1', 'value2'
)
```

Note: `$1`, `$2`, etc. are **parameter placeholders** (not `?` like in SQLite or MySQL).

---

### 4. **Using a Connection Pool (Recommended for Web Apps)**

```python
async def fetch_with_pool():
    pool = await asyncpg.create_pool(
        user='your_username',
        password='your_password',
        database='your_db_name',
        host='your_host',
        port=5432,
        min_size=1,
        max_size=10
    )

    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM your_table_name')
        for row in rows:
            print(dict(row))

    await pool.close()

asyncio.run(fetch_with_pool())
```

---

## 🧠 Tips

* `conn.fetch()` returns a list of `Record` objects (like dicts).
* Use `fetchrow()` to get one row, or `fetchval()` to get a single value.
* For performance, use **connection pooling** in async web servers (e.g., FastAPI).


