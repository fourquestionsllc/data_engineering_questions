Since you already have a **sign-in token**, you don't need to provide a username and password when publishing the data source. Instead, you can use the **token** for authentication and skip the credentials in the XML payload.

---

### **📌 Publish a `.hyper` Data Source Using Upload Session ID**
#### **🔹 Prerequisites**
- **Authentication Token (`X-Tableau-Auth`)** from sign-in
- **Site LUID (`site-id`)** from sign-in response
- **Upload Session ID (`uploadSessionId`)** from file upload step
- **Tableau Server URL**

---

### **🚀 Python Script to Publish Data Source**
```python
import requests

# ✅ Replace with your actual values
TABLEAU_SERVER = "https://your-tableau-server"
SITE_ID = "your-site-luid"  # Obtained during sign-in
UPLOAD_SESSION_ID = "your-upload-session-id"  # Obtained from file upload
TOKEN = "your-auth-token"  # Authentication token from sign-in
DATA_SOURCE_NAME = "My_Data_Source"

# ✅ API endpoint for publishing the data source
PUBLISH_URL = f"{TABLEAU_SERVER}/api/3.18/sites/{SITE_ID}/datasources"

# ✅ XML payload without username/password (since you're already authenticated)
xml_payload = f"""
<tsRequest>
    <datasource name="{DATA_SOURCE_NAME}"/>
</tsRequest>
"""

# ✅ Headers for authentication
headers = {
    "X-Tableau-Auth": TOKEN,
    "Content-Type": "application/xml"
}

# ✅ Query parameters
params = {
    "uploadSessionId": UPLOAD_SESSION_ID,  # Attach the uploaded .hyper file
    "datasourceType": "hyper",  # Specify .hyper as the data source type
    "overwrite": "true",  # Overwrite existing data source (set "false" to prevent overwriting)
    "asJob": "false"  # Set "true" for large uploads (async processing)
}

# ✅ Make the API request to publish the data source
response = requests.post(PUBLISH_URL, headers=headers, params=params, data=xml_payload)

# ✅ Check the response
if response.status_code == 201:
    print("✅ Data source published successfully!")
    print(response.json())  # Prints the response JSON with details
else:
    print("❌ Failed to publish data source:", response.text)
```

---

### **🔹 Key Adjustments**
1. **Removed `connectionCredentials`**: Since you already have an **auth token**, username and password are unnecessary.
2. **Kept `overwrite=true`**: Ensures that if the data source exists, it will be replaced.
3. **Set `asJob=false`**: Use `true` if the file is large and should be processed asynchronously.

---

### **🔹 Optional Enhancements**
- If using **asynchronous publishing (`asJob=true`)**, you can track the **job status** using:
  ```python
  JOB_ID = response.json()["job"]["id"]
  STATUS_URL = f"{TABLEAU_SERVER}/api/3.18/sites/{SITE_ID}/jobs/{JOB_ID}"
  ```
  Then poll the status until it's `Success`.

---

### **🎯 Expected API Response (Success)**
A successful response (`201 Created`) will return:
```json
{
    "datasource": {
        "id": "1234-5678-9012",
        "name": "My_Data_Source",
        "contentUrl": "My_Data_Source"
    }
}
```

---

This script ensures you can **publish a `.hyper` file** with just a **session token** without needing additional credentials. 🚀 

Would you like an enhancement to **track the publishing job status** if using `asJob=true`?
