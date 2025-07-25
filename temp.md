To retrieve a **view** from Tableau Server using the **Tableau REST API**, and map it to a URL like:

```
https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash
```

you can follow these steps:

---

### ✅ Step-by-step Plan

1. **Authenticate** to Tableau Server (sign in).
2. **Get view by path** using the REST API.
3. **(Optional)** Reconstruct or confirm the view URL using returned info.

---

### 🧠 Extracted Path Components

From the URL:

```
https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash
```

* **site**: `FPNA`
* **workbook**: `EMEAExpenseDashboard`
* **view**: `ExpenseDash`

---

### 🐍 Python Code (Using `requests`)

```python
import requests

# ---- CONFIG ----
TABLEAU_SERVER = "https://dev.forecastvisualanalytics.citigroup.net"
USERNAME = "your_tableau_username"
PASSWORD = "your_tableau_password"
SITE_NAME = "FPNA"
VIEW_PATH = "EMEAExpenseDashboard/ExpenseDash"

# ---- SIGN IN ----
signin_url = f"{TABLEAU_SERVER}/api/3.22/auth/signin"
headers = {'Content-Type': 'application/json'}
payload = {
    "credentials": {
        "name": USERNAME,
        "password": PASSWORD,
        "site": {"contentUrl": SITE_NAME}
    }
}

response = requests.post(signin_url, json=payload, headers=headers)
response.raise_for_status()
data = response.json()
token = data['credentials']['token']
site_id = data['credentials']['site']['id']

# ---- GET VIEW BY PATH ----
view_by_path_url = f"{TABLEAU_SERVER}/api/3.22/sites/{site_id}/views/by-path"
headers['X-Tableau-Auth'] = token
params = {'path': VIEW_PATH}

view_resp = requests.get(view_by_path_url, headers=headers, params=params)
view_resp.raise_for_status()
view_data = view_resp.json()['view']

# ---- PRINT RESULT ----
view_id = view_data['id']
workbook_id = view_data['workbook']['id']
view_name = view_data['name']
print(f"✅ View ID: {view_id}")
print(f"✅ View Name: {view_name}")
print(f"✅ Workbook ID: {workbook_id}")

# ---- RECONSTRUCT VIEW URL (Optional) ----
final_url = f"{TABLEAU_SERVER}/#/site/{SITE_NAME}/views/{VIEW_PATH}"
print(f"🌐 URL: {final_url}")
```

---

### 🔐 Notes

* Replace `USERNAME`/`PASSWORD` with your real Tableau credentials or use a **Personal Access Token** if preferred.
* API version `3.22` is for Tableau 2024.2 — adjust according to your server version.

---

Want a version using **personal access token** (PAT) instead of username/password?
