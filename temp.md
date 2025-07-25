To retrieve a **Tableau view by path** using the REST API, you need to follow these steps in Python:

---

### 🔧 **Prerequisites**

* Tableau Personal Access Token (PAT) or username/password.
* Your `site-id` (or `default` if not using sites).
* API version (e.g., `3.26`).
* View's `viewUrlName` — in your case, it's `ExpenseDash`.

Given your full URL:

```
https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash
```

* **site-id (name)**: `FPNA`
* **workbook-url-name**: `EMEAExpenseDashboard`
* **view-url-name**: `ExpenseDash`

---

### ✅ **Python Code**

```python
import requests

# Configuration
SERVER = "https://dev.forecastvisualanalytics.citigroup.net"
API_VERSION = "3.26"
SITE_NAME = "FPNA"
VIEW_URL_NAME = "ExpenseDash"

# PAT authentication details
PAT_NAME = "<your-pat-name>"
PAT_SECRET = "<your-pat-secret>"

# Step 1: Sign in and get token + site ID
def sign_in():
    url = f"{SERVER}/api/{API_VERSION}/auth/signin"
    headers = {"Content-Type": "application/json"}
    payload = {
        "credentials": {
            "personalAccessTokenName": PAT_NAME,
            "personalAccessTokenSecret": PAT_SECRET,
            "site": {"contentUrl": SITE_NAME}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    resp_json = response.json()
    token = resp_json["credentials"]["token"]
    site_id = resp_json["credentials"]["site"]["id"]
    return token, site_id

# Step 2: Get view by viewUrlName
def get_view_by_path(token, site_id):
    headers = {
        "X-Tableau-Auth": token
    }
    filter_expr = f"viewUrlName:eq:{VIEW_URL_NAME}"
    url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/views?filter={filter_expr}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Step 3: Sign out (optional but good practice)
def sign_out(token):
    url = f"{SERVER}/api/{API_VERSION}/auth/signout"
    headers = {"X-Tableau-Auth": token}
    requests.post(url, headers=headers)

# Run
if __name__ == "__main__":
    try:
        token, site_id = sign_in()
        view_data = get_view_by_path(token, site_id)
        print("View Info:", view_data)
    finally:
        sign_out(token)
```

---

### 📌 Notes:

* Replace `<your-pat-name>` and `<your-pat-secret>` with your Tableau credentials.
* If you don’t have PAT, you can use username/password method instead.
* You can extract the full view URL or ID from the response JSON.

Would you like me to help extract the view ID or workbook ID from the response as well?
