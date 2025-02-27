You're right! `tableauserverclient` does **not** have a `TableauType` attribute. The correct way to define a Hyper table is to manually map `pandas` column types to `tableauhyperapi.SqlType`. Below is the corrected version of your script.  

---

### **1. Install Dependencies**
```bash
pip install tableauserverclient pandas requests tableauhyperapi
```

---

### **2. Corrected Python Code**

#### **Step 1: Authenticate with Tableau Server**
```python
import tableauserverclient as TSC

# Tableau Server details
TABLEAU_SERVER = "https://your-tableau-server-url"
TOKEN_NAME = "your-token-name"
TOKEN_VALUE = "your-token-secret"
SITE_ID = ""  # Leave empty for the default site

# Sign in to Tableau Server
auth = TSC.PersonalAccessTokenAuth(TOKEN_NAME, TOKEN_VALUE, SITE_ID)
server = TSC.Server(TABLEAU_SERVER, use_server_version=True)

with server.auth.sign_in(auth):
    print("Successfully signed in!")
```

---

#### **Step 2: Convert CSV to Hyper File**
```python
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter, TableName
import pandas as pd

# Read CSV file
csv_file = "data.csv"
df = pd.read_csv(csv_file)

# Define Hyper File Path
hyper_file = "data.hyper"

# Map Pandas dtypes to Tableau Hyper SQL Types
def map_pandas_dtype_to_sqltype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return SqlType.big_int()
    elif pd.api.types.is_float_dtype(dtype):
        return SqlType.double()
    elif pd.api.types.is_bool_dtype(dtype):
        return SqlType.bool()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return SqlType.timestamp()
    else:
        return SqlType.text()

# Define Hyper Table Schema
table_definition = TableDefinition(
    TableName("Extract"),
    [
        (col, map_pandas_dtype_to_sqltype(df[col].dtype)) for col in df.columns
    ],
)

# Create Hyper File
with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(endpoint=hyper.endpoint, database=hyper_file, create_mode="create_and_replace") as connection:
        connection.catalog.create_table(table_definition)

        # Insert Data
        with Inserter(connection, table_definition) as inserter:
            inserter.add_rows(df.values.tolist())
            inserter.execute()

print(f"Hyper file '{hyper_file}' created successfully!")
```

---

#### **Step 3: Publish Hyper File to Tableau Server**
```python
# Define project name in Tableau
PROJECT_NAME = "Your Project Name"

# Find the project
with server.auth.sign_in(auth):
    all_projects, _ = server.projects.get()
    project = next((p for p in all_projects if p.name == PROJECT_NAME), None)

    if project is None:
        raise Exception(f"Project '{PROJECT_NAME}' not found on Tableau Server.")

    # Create the Data Source Object
    new_datasource = TSC.DatasourceItem(project.id)

    # Publish Data Source
    new_datasource = server.datasources.publish(new_datasource, hyper_file, TSC.Server.PublishMode.Overwrite)
    print(f"Data Source published successfully with ID: {new_datasource.id}")
```

---

### **3. Summary of Fixes**
✅ **Fixed the `TableauType` issue** by using `tableauhyperapi.SqlType` instead.  
✅ **Added a function to map Pandas data types to Tableau Hyper types** dynamically.  
✅ **Ensured correct column type handling** for integers, floats, booleans, timestamps, and text.  

