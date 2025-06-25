To connect to an **Oracle database** using Python, you can use the `cx_Oracle` or the newer `oracledb` package (preferred in modern environments). Below is a full example using the `oracledb` package.

---

### ✅ 1. **Install the Oracle Python driver**

```bash
pip install oracledb
```

---

### ✅ 2. **Basic example to connect and run a query**

```python
import oracledb

# Optional: run in thin mode (no Oracle client required)
oracledb.init_oracle_client(lib_dir=None)  # or remove this line entirely for thin mode

# Replace with your actual values
username = "your_username"
password = "your_password"
dsn = "your_host:your_port/your_service_name"  # e.g. "dbhost.example.com:1521/orclpdb1"

# Connect
conn = oracledb.connect(user=username, password=password, dsn=dsn)

# Create cursor and run a query
cursor = conn.cursor()
cursor.execute("SELECT * FROM your_table")

# Fetch results
for row in cursor:
    print(row)

# Cleanup
cursor.close()
conn.close()
```

---

### ✅ 3. **DSN formats**

The `dsn` string has several formats you can use:

#### EZConnect (most common):

```
hostname:port/service_name
```

Example:

```
mydb.example.com:1521/XEPDB1
```

---

### ✅ 4. **Advanced: Use `cx_Oracle.makedsn()` to build DSN (optional)**

```python
import oracledb

dsn = oracledb.makedsn("mydb.example.com", 1521, service_name="XEPDB1")
conn = oracledb.connect(user="scott", password="tiger", dsn=dsn)
```

---
