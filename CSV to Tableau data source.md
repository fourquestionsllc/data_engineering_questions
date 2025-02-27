To create a Tableau data source from a CSV file using the **REST API and Python**, follow these steps:

### **1. Prerequisites**
- **Tableau Server or Tableau Cloud** (Ensure you have access).
- **Personal Access Token (PAT)** or **Username & Password** with the required permissions.
- **Python libraries:** `tableauserverclient`, `requests`, `pandas`, etc.

### **2. Steps to Upload CSV as a Tableau Data Source**

#### **Step 1: Install Required Libraries**
```bash
pip install tableauserverclient pandas requests
```

#### **Step 2: Authenticate with Tableau Server**
Use Tableau Server REST API or Tableau Server Client (`TSC`).

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

#### **Step 3: Convert CSV to Hyper File (Required Format)**
Tableau requires the data source to be in **.hyper** format.

```python
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter, TableName
import pandas as pd

# Read CSV file
csv_file = "data.csv"
df = pd.read_csv(csv_file)

# Define Hyper File Path
hyper_file = "data.hyper"

# Define Hyper Table Schema
table_definition = TableDefinition(
    TableName("Extract"),
    [
        TSC.TableauType.to_hyper_column(column_name, SqlType.text())  # Change type accordingly
        for column_name in df.columns
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

#### **Step 4: Publish Hyper File to Tableau Server**
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

### **3. Summary of Workflow**
1. **Authenticate with Tableau Server** using PAT or credentials.
2. **Convert CSV to Tableau's Hyper format** using `tableauhyperapi`.
3. **Publish the Hyper file to Tableau Server** using `tableauserverclient`.
