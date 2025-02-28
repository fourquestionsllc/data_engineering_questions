Here is the equivalent Python code using the `requests` library:  

```python
import requests

# Define your server details
TABLEAU_SERVER = "http://MY_SERVER"
SITE_ID = "ff2a8360-3c2b-4b05-a793-7607c602e1fb"
AUTH_TOKEN = "6fSulU7ET8yjpHteQj56MQ|LrkEdTHcmPkWFcD8wOEy29hlVXm8iPo4"

# Define the API URL
url = f"{TABLEAU_SERVER}/api/3.4/sites/{SITE_ID}/datasources"

# Define headers
headers = {
    "X-Tableau-Auth": AUTH_TOKEN,
    "Content-Type": "multipart/mixed"
}

# Define the files to be uploaded
files = {
    "request_payload": ("publish-datasource.xml", open("publish-datasource.xml", "rb"), "text/xml"),
    "tableau_datasource": ("data-source.tds", open("data-source.tds", "rb"), "application/octet-stream"),
}

# Make the POST request
response = requests.post(url, headers=headers, files=files)

# Print the response
print(response.status_code)
print(response.text)
```

### **Explanation:**
- Uses `requests.post()` to send a multipart form-data request.
- `request_payload` (the XML file) is sent with `"text/xml"` MIME type.
- `tableau_datasource` (the `.tds` file) is sent with `"application/octet-stream"` MIME type.
- Authentication is passed via the `X-Tableau-Auth` header.

Make sure `publish-datasource.xml` and `data-source.tds` exist in the script's directory before running.
