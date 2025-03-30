To retrieve **all views** from Tableau's REST API without the **100-item limit**, you need to use **pagination**.

---

### **Steps to Query Views Without the 100-Item Limit**

#### **1. Authenticate & Get Session Token**
First, authenticate to Tableau Server or Tableau Cloud to obtain a session token.

```bash
POST /api/3.18/auth/signin
```

---

#### **2. Use Pagination to Retrieve All Views**
The `pageSize` parameter limits the number of results (max **100**), and `pageNumber` allows you to navigate through results.

##### **Example API Request**
```bash
GET /api/3.18/sites/{site_id}/views?pageSize=100&pageNumber=1
```

---

#### **3. Loop Until No More Results**
Since you can only retrieve up to **100** views per request, you need to iterate through pages.

##### **Python Example**
```python
import requests

# Tableau Server Info
server = "https://your-tableau-server"
site_id = "your-site-id"
auth_token = "your-auth-token"

views = []
page_number = 1
page_size = 100  # Max limit per request

while True:
    url = f"{server}/api/3.18/sites/{site_id}/views?pageSize={page_size}&pageNumber={page_number}"
    headers = {"X-Tableau-Auth": auth_token}
    
    response = requests.get(url, headers=headers)
    data = response.json()

    views_batch = data.get("views", {}).get("view", [])
    
    if not views_batch:
        break  # Stop if no more views

    views.extend(views_batch)
    page_number += 1

print(f"Total Views Retrieved: {len(views)}")
```

---

### **4. Optimize the Query**
- **Use the `fields` parameter** to retrieve only necessary fields and reduce response size.
- **Use filtering** if needed to fetch views for a specific workbook.

##### **Example Filtering by Workbook ID**
```bash
GET /api/3.18/sites/{site_id}/workbooks/{workbook_id}/views?pageSize=100&pageNumber=1
```
