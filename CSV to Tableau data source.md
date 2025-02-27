To create a Tableau data source from a CSV file using RESTful API and Python, follow these steps:

1. Convert the CSV file to a `.hyper` file using Tableau Hyper API.
2. Use Tableau REST API to publish the `.hyper` file to Tableau Server or Tableau Cloud.

### Step 1: Convert CSV to `.hyper` File
Using the Hyper API, the provided guide shows how to create a Hyper file from a CSV. Below is a Python script to do this:

```python
from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Telemetry, Inserter
import csv

# Define the schema of the table
tableau_table = TableDefinition("Extract", [
    TableDefinition.Column("Column1", SqlType.text()), 
    TableDefinition.Column("Column2", SqlType.int()),  
    TableDefinition.Column("Column3", SqlType.double()) 
])

# Create a Hyper file
with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(endpoint=hyper.endpoint, database="data.hyper", create_mode="create_and_replace") as connection:
        connection.catalog.create_table(tableau_table)

        # Insert CSV data into the Hyper file
        with Inserter(connection, tableau_table) as inserter:
            with open("data.csv", "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    inserter.add_row(row)
            inserter.execute()
```

### Step 2: Publish the Hyper File using Tableau REST API
Now, use Tableau REST API to publish the `.hyper` file:

#### 1. Authenticate with Tableau Server:
```python
import requests

TABLEAU_SERVER = "https://your-tableau-server.com"
USERNAME = "your-username"
PASSWORD = "your-password"
SITE_ID = ""  # Leave empty for default site

# Authenticate and get token
auth_payload = {
    "credentials": {
        "name": USERNAME,
        "password": PASSWORD,
        "site": {"contentUrl": SITE_ID}
    }
}

auth_response = requests.post(f"{TABLEAU_SERVER}/api/3.15/auth/signin", json=auth_payload)
auth_data = auth_response.json()
TOKEN = auth_data["credentials"]["token"]
SITE_ID = auth_data["credentials"]["site"]["id"]
USER_ID = auth_data["credentials"]["user"]["id"]
```

#### 2. Upload and Publish Hyper File:
```python
from pathlib import Path

headers = {
    "X-Tableau-Auth": TOKEN
}

# Create a new datasource
datasource_name = "MyDataSource"
file_path = Path("data.hyper")

# Initiate file upload
upload_response = requests.post(f"{TABLEAU_SERVER}/api/3.15/sites/{SITE_ID}/fileUploads", headers=headers)
upload_session_id = upload_response.json()["fileUpload"]["uploadSessionId"]

# Upload chunks
with open(file_path, "rb") as f:
    requests.put(f"{TABLEAU_SERVER}/api/3.15/sites/{SITE_ID}/fileUploads/{upload_session_id}",
                 headers=headers, data=f)

# Publish the data source
publish_url = f"{TABLEAU_SERVER}/api/3.15/sites/{SITE_ID}/datasources"
publish_payload = {
    "datasource": {"name": datasource_name},
    "uploadSessionId": upload_session_id,
    "overwrite": "true"
}

publish_response = requests.post(publish_url, headers=headers, json=publish_payload)
print("Published:", publish_response.json())
```

This script:
1. Converts CSV to a `.hyper` file.
2. Authenticates with Tableau REST API.
3. Uploads the `.hyper` file in chunks.
4. Publishes the file as a data source.

Let me know if you need modifications! 🚀
