```
import requests
from requests.auth import HTTPBasicAuth

# Configuration details
host = "your-oracle-hostname"
port = "your-port-number"
service_name = "your-service-name"
username = "your-username"
password = "your-password"
query_endpoint = f"http://{host}:{port}/ords/{service_name}/your_api_endpoint"

# Headers for JSON request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Execute SQL query via REST API
sql_query = "SELECT * FROM your_table FETCH FIRST 10 ROWS ONLY"
payload = {"statement": sql_query}

# Make POST request
response = requests.post(query_endpoint, json=payload, headers=headers, auth=HTTPBasicAuth(username, password))

# Process response
if response.status_code == 200:
    data = response.json()
    print(data)  # JSON response
else:
    print(f"Error {response.status_code}: {response.text}")
```
