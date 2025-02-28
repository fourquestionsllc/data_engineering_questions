Here's a Python script that uploads a `.hyper` file to Tableau Server using the Tableau REST API. It follows the given reference to publish a data source.

```python
import requests
import xml.etree.ElementTree as ET

# Configuration
TABLEAU_SERVER = "https://your-tableau-server"  # Replace with your Tableau Server URL
API_VERSION = "3.24"  # Replace with the correct API version
USERNAME = "your-username"
PASSWORD = "your-password"
SITE_ID = "your-site-id"  # Replace with your site ID or "" for the default site
PROJECT_ID = "your-project-id"  # Replace with your project ID
DATA_SOURCE_NAME = "your-datasource-name"
FILE_PATH = "your-file.hyper"  # Path to the .hyper file

# Authenticate and get a token
def get_auth_token():
    url = f"{TABLEAU_SERVER}/api/{API_VERSION}/auth/signin"
    payload = {
        "credentials": {
            "name": USERNAME,
            "password": PASSWORD,
            "site": {"contentUrl": SITE_ID}
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    xml_response = ET.fromstring(response.text)
    token = xml_response.find(".//t:credentials", namespaces={'t': 'http://tableau.com/api'}).get("token")
    site_id = xml_response.find(".//t:site", namespaces={'t': 'http://tableau.com/api'}).get("id")
    
    return token, site_id

# Publish data source
def publish_datasource(token, site_id):
    url = f"{TABLEAU_SERVER}/api/{API_VERSION}/sites/{site_id}/datasources?overwrite=true"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    headers = {
        "X-Tableau-Auth": token,
        "Content-Type": f"multipart/mixed; boundary={boundary}"
    }
    
    # XML request payload
    request_payload = f"""
--{boundary}
Content-Disposition: name="request_payload"
Content-Type: text/xml

<tsRequest>
    <datasource name="{DATA_SOURCE_NAME}">
        <project id="{PROJECT_ID}" />
    </datasource>
</tsRequest>
"""
    
    # Read the file
    with open(FILE_PATH, "rb") as file:
        file_content = file.read()
    
    file_part = f"""
--{boundary}
Content-Disposition: name="tableau_datasource"; filename="{FILE_PATH}"
Content-Type: application/octet-stream

""".encode() + file_content + f"\n--{boundary}--\n".encode()
    
    body = request_payload.encode() + file_part
    
    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    print("Datasource published successfully!")

if __name__ == "__main__":
    token, site_id = get_auth_token()
    publish_datasource(token, site_id)
```

This script:
1. Authenticates with Tableau Server to obtain a session token.
2. Constructs a multipart request to publish a `.hyper` file.
3. Uses the `overwrite=true` flag to replace existing data sources if needed.
