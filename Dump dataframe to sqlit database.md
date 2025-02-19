You can use the `to_sql` method in pandas to dump a DataFrame into an SQLite table. Here’s how you do it:

### Steps:
1. Install SQLite (if not already available) and ensure you have `sqlite3` and `pandas` installed.
2. Connect to the SQLite database using `sqlite3` or `SQLAlchemy`.
3. Use the `to_sql` method to store the DataFrame into the database.

### Example:
```python
import sqlite3
import pandas as pd

# Create a sample DataFrame
data = {'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
df = pd.DataFrame(data)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Dump the DataFrame into an SQLite table
df.to_sql('users', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
```

### Explanation:
- `to_sql('users', conn, if_exists='replace', index=False)`:  
  - `'users'`: Name of the SQLite table.
  - `conn`: SQLite connection.
  - `if_exists='replace'`: Replaces the table if it already exists. Use `'append'` to add new records instead.
  - `index=False`: Prevents pandas from writing the DataFrame index as a column.

This will create (or replace) a table named `users` in the SQLite database `example.db` with the data from the DataFrame.
