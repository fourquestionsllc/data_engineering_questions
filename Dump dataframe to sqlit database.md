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


If a column in your DataFrame contains dictionaries (i.e., nested data structures), you cannot directly store it in SQLite because SQLite does not have a native `dict` type. However, you can handle this by converting the dictionary into a string format (e.g., JSON) before storing it.  

### Solution: Convert Dictionary Column to JSON
You can use the `json.dumps()` method from the `json` module to serialize dictionaries before writing to SQLite. Later, you can deserialize them using `json.loads()` when reading back.

### Example:
```python
import sqlite3
import pandas as pd
import json

# Sample DataFrame with a dictionary column
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'details': [{'age': 25, 'city': 'NY'}, {'age': 30, 'city': 'LA'}, {'age': 35, 'city': 'SF'}]  # Dictionary column
}

df = pd.DataFrame(data)

# Convert dictionary column to JSON strings
df['details'] = df['details'].apply(json.dumps)

# Connect to SQLite database
conn = sqlite3.connect('example.db')

# Store the DataFrame in SQLite
df.to_sql('users', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
```

### Reading Back and Converting JSON to Dictionary:
When reading from the database, convert the JSON string back into a dictionary:
```python
# Reconnect to the database
conn = sqlite3.connect('example.db')

# Read the data
df = pd.read_sql('SELECT * FROM users', conn)

# Convert JSON string back to dictionary
df['details'] = df['details'].apply(json.loads)

# Close connection
conn.close()

print(df)
```

### Explanation:
1. **Serialization (`json.dumps`)**: Converts dictionary objects into JSON strings before storing.
2. **Storage**: The DataFrame is saved in SQLite.
3. **Deserialization (`json.loads`)**: Converts JSON strings back into Python dictionaries when reading from the database.

This approach ensures that you can store and retrieve dictionary-type data while maintaining its structure. 🚀
