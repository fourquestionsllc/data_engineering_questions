When applying a filter in a Tableau REST API call using Python's `requests` module, you need to **URL encode** the query parameters to handle spaces and special characters properly.

---

## **Solution: URL Encoding the Parameters**
You can use Python's `urllib.parse.quote` or `urllib.parse.urlencode` to properly format the filter query.

### **Example: Applying a Filter Where `a = b`**
- If **`a`** contains spaces (e.g., `"Product Category"` → `"Product%20Category"`)
- If **`b`** is a string (e.g., `"Office Supplies"` → `"Office%20Supplies"`)

Use `urllib.parse.quote` to encode individual values:

```python
import requests
import urllib.parse

# Define variables
server = "https://your-tableau-server"
site_id = "your-site-id"
view_id = "your-view-id"
auth_token = "your-auth-token"

# Define filter key-value pair
filter_key = "Product Category"  # Key with spaces
filter_value = "Office Supplies"  # Value with spaces

# URL encode both key and value
encoded_key = urllib.parse.quote(filter_key)
encoded_value = urllib.parse.quote(filter_value)

# Construct the filter parameter
filter_param = f"{encoded_key}={encoded_value}"

# Make API request with filter
headers = {"X-Tableau-Auth": auth_token}
url = f"{server}/api/3.17/sites/{site_id}/views/{view_id}/image?filter={filter_param}"

response = requests.get(url, headers=headers)

# Save the filtered image
if response.status_code == 200:
    with open("filtered_view_image.png", "wb") as file:
        file.write(response.content)
    print("Filtered view image saved successfully!")
else:
    print("Error:", response.text)
```

---

## **Alternative: Using `urllib.parse.urlencode` for Multiple Filters**
If you have **multiple filters**, use `urllib.parse.urlencode({})` to encode them automatically:

```python
import requests
import urllib.parse

# Define multiple filters
filters = {
    "Product Category": "Office Supplies",
    "Region": "West"
}

# Encode the filters
encoded_filters = urllib.parse.urlencode(filters)

# Construct the API URL
url = f"{server}/api/3.17/sites/{site_id}/views/{view_id}/image?{encoded_filters}"

headers = {"X-Tableau-Auth": auth_token}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("filtered_view_image.png", "wb") as file:
        file.write(response.content)
    print("Filtered view image saved successfully!")
else:
    print("Error:", response.text)
```

---

## **Key Takeaways**
✅ Use `urllib.parse.quote()` to encode individual query parameters.  
✅ Use `urllib.parse.urlencode({})` for encoding multiple parameters at once.  
✅ Encoded spaces become `%20` (e.g., `"Product Category"` → `"Product%20Category"`).  
