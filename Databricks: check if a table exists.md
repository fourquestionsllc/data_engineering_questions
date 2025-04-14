In Databricks, you can check if a table exists using PySpark or Databricks Utilities (`dbutils`). Here are a few common ways to do this in Python:

---

### ✅ **1. Using Spark SQL Catalog (`spark.catalog.tableExists`)**

```python
table_exists = spark.catalog.tableExists("database_name.table_name")
print(table_exists)
```

- If you're using the **default database**, you can omit the database name:
  
```python
table_exists = spark.catalog.tableExists("table_name")
```

---

### ✅ **2. Using SQL Query**

```python
result = spark.sql("""
    SHOW TABLES IN database_name
""").filter("tableName = 'table_name'").count() > 0

print(result)
```

---

### ✅ **3. Using `dbutils` (to check if a path exists, useful for Delta tables stored in DBFS)**

```python
table_path = "dbfs:/user/hive/warehouse/database_name.db/table_name"
exists = dbutils.fs.ls(table_path) is not None
print(exists)
```

> ⚠️ This method is more low-level and used if you're checking **physical existence** of a table directory (like Delta).

---

### ✅ **Bonus: Wrap into a function**

```python
def table_exists(db_name: str, table_name: str) -> bool:
    return spark.catalog.tableExists(f"{db_name}.{table_name}")
```

---
