To create a table in **SQLite** using **Pandas** and insert records into it, follow these steps:

### **Steps:**
1. **Install dependencies** (if not installed):  
   ```bash
   pip install pandas sqlite3
   ```
2. **Import required libraries**:
   ```python
   import sqlite3
   import pandas as pd
   ```
3. **Create an SQLite database and connect to it**:
   ```python
   conn = sqlite3.connect('example.db')  # Creates or opens a database file
   cursor = conn.cursor()
   ```
4. **Create a table**:
   ```python
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS employees (
       id INTEGER PRIMARY KEY,
       name TEXT,
       age INTEGER,
       department TEXT
   )
   ''')
   conn.commit()
   ```
5. **Insert records into the table**:
   ```python
   cursor.execute("INSERT INTO employees (name, age, department) VALUES ('Alice', 30, 'HR')")
   cursor.execute("INSERT INTO employees (name, age, department) VALUES ('Bob', 25, 'IT')")
   conn.commit()
   ```
6. **Insert data using Pandas DataFrame**:
   ```python
   data = {'name': ['Charlie', 'David'],
           'age': [35, 40],
           'department': ['Finance', 'Marketing']}

   df = pd.DataFrame(data)

   df.to_sql('employees', conn, if_exists='append', index=False)  # Append data
   ```
7. **Fetch and display records**:
   ```python
   df_from_db = pd.read_sql("SELECT * FROM employees", conn)
   print(df_from_db)
   ```
8. **Close the connection**:
   ```python
   conn.close()
   ```

### **Output (Example)**
```
   id     name  age department
0   1   Alice   30        HR
1   2     Bob   25        IT
2   3  Charlie  35   Finance
3   4   David   40  Marketing
```
