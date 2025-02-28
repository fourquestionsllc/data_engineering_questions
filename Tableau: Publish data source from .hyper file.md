Here's a Python script that uploads a `.hyper` file to Tableau Server using the Tableau REST API. It follows the given reference to publish a data source.

```python
import requests
import xml.etree.ElementTree as ET
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Configuration
TABLEAU_SERVER = "YOUR_TABLEAU_SERVER"
API_VERSION = "3.24"  # Update as needed
SITE_ID = "YOUR_SITE_LUID"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
PROJECT_ID = "YOUR_PROJECT_LUID"
DATASOURCE_NAME = "YourDataSourceName"
HYPER_FILE_PATH = "path/to/your/file.hyper"

# Authenticate and get token
def authenticate():
    url = f"{TABLEAU_SERVER}/api/{API_VERSION}/auth/signin"
    headers = {"Content-Type": "application/xml"}
    
    payload = f'''<?xml version="1.0" encoding="UTF-8"?>
    <tsRequest>
        <credentials name="{USERNAME}" password="{PASSWORD}">
            <site id="{SITE_ID}" />
        </credentials>
    </tsRequest>
    '''.strip()
    
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    return root.find(".//t:token", namespaces={"t": "http://tableau.com/api"}).text

# Publish the .hyper file
def publish_datasource(auth_token):
    url = f"{TABLEAU_SERVER}/api/{API_VERSION}/sites/{SITE_ID}/datasources?overwrite=true"
    
    xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
    <tsRequest>
        <datasource name="{DATASOURCE_NAME}">
            <project id="{PROJECT_ID}" />
        </datasource>
    </tsRequest>
    '''.strip()
    
    with open(HYPER_FILE_PATH, "rb") as file:
        file_content = file.read()
    
    encoder = MultipartEncoder(
        fields={
            "request_payload": (None, xml_payload, "text/xml"),
            "tableau_datasource": (HYPER_FILE_PATH.split("/")[-1], file_content, "application/octet-stream")
        }
    )
    
    headers = {
        "X-Tableau-Auth": auth_token,
        "Content-Type": encoder.content_type
    }
    
    response = requests.post(url, headers=headers, data=encoder)
    response.raise_for_status()
    
    print("Datasource uploaded successfully:", response.text)

# Execute script
def main():
    try:
        auth_token = authenticate()
        publish_datasource(auth_token)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
```

This script:
1. Authenticates with Tableau Server to obtain a session token.
2. Constructs a multipart request to publish a `.hyper` file.
3. Uses the `overwrite=true` flag to replace existing data sources if needed.
