To publish a `.hyper` file as a data source to Tableau Server using Python, you can use the `requests` library to mimic the `cURL` request. Here's how you can do it:

### **Python Code to Publish a `.hyper` File**
```python
import requests

# Define your server details
TABLEAU_SERVER = "http://MY_SERVER"
SITE_ID = "ff2a8360-3c2b-4b05-a793-7607c602e1fb"
AUTH_TOKEN = "6fSulU7ET8yjpHteQj56MQ|LrkEdTHcmPkWFcD8wOEy29hlVXm8iPo4"

# Define the request headers
headers = {
    "X-Tableau-Auth": AUTH_TOKEN,
    "Content-Type": "multipart/mixed"
}

# Define the API URL
url = f"{TABLEAU_SERVER}/api/3.4/sites/{SITE_ID}/datasources"

# Define the payload (publish-datasource.xml)
publish_xml = """<tsRequest>
  <datasource name="datasource1" description="This is a data source named datasource1.">
    <project id="522dc5c5-e1da-47b9-8e07-f02929ff5ceb" />
  </datasource>
</tsRequest>"""

# Define the files to be uploaded
files = {
    "request_payload": ("publish-datasource.xml", publish_xml, "text/xml"),
    "tableau_datasource": ("data-source.hyper", open("data-source.hyper", "rb"), "application/octet-stream"),
}

# Make the POST request
response = requests.post(url, headers=headers, files=files)

# Print the response
print(response.status_code)
print(response.text)
```

### **Explanation:**
1. **Authentication**: Uses `X-Tableau-Auth` token in the headers.
2. **Multipart Form Upload**:
   - The `.xml` payload is sent as `request_payload`.
   - The `.hyper` file is sent as `tableau_datasource`.
3. **Requests Module**: The `requests.post()` method handles the `multipart/mixed` upload.
4. **File Handling**: The `.hyper` file is opened in binary mode.

**Ensure:**
- You have the correct `SITE_ID`, `AUTH_TOKEN`, and `PROJECT_ID`.
- The `.hyper` file exists in the directory where the script runs.
