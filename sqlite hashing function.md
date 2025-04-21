In SQLite, you can hash a string using extensions or built-in functions **if compiled with certain options**. By default, SQLite doesn't have built-in `MD5` or `SHA` hashing functions, but here are your main options:

---

## ✅ **Option 1: Use `sqlite3-pcre` or `crypto` Extension (if available)**

If your SQLite build includes the **`crypto` extension**, you can use:

```sql
SELECT sha256('your string here');
```

Or:

```sql
SELECT md5('your string here');
```

> ❗️Note: Most pre-built SQLite binaries **do not include** this extension by default. You’ll need to compile SQLite with the extension or load it manually.

---

## ✅ **Option 2: Use a Custom Function via Application Layer (Python, etc.)**

If you're using SQLite via Python, you can register a custom hash function:

```python
import sqlite3
import hashlib

def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

conn = sqlite3.connect("your.db")
conn.create_function("sha256", 1, sha256)

cursor = conn.cursor()
cursor.execute("SELECT sha256(?)", ("hello",))
print(cursor.fetchone()[0])
```

Now you can use `sha256()` in your SQL queries.

---

## ✅ **Option 3: Use the `load_extension` Method (If Enabled)**

You can dynamically load an extension:

```sql
SELECT load_extension('libcrypto');
SELECT sha256('some text');
```

> But this works **only if**:
> - Extensions are enabled (`sqlite3_enable_load_extension`)
> - You have a shared object like `libcrypto.so` or `crypto.dll`

---

## 🚫 No Native Hash Functions in Pure SQL

Without an extension or external function, **SQLite itself can’t hash strings** using native SQL.

---

## 🧪 Workaround Example (MD5 via Python + SQLite)

```python
import sqlite3
import hashlib

conn = sqlite3.connect(':memory:')
conn.create_function("md5", 1, lambda x: hashlib.md5(x.encode()).hexdigest())

cursor = conn.cursor()
cursor.execute("SELECT md5('Austin')")
print(cursor.fetchone()[0])  # Output: 8783b993587a188a888f29c3325b8b7c
```

---
