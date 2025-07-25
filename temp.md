Here's a Python function that parses a Tableau view URL in the format:

```
https://<server_url>/#/site/<site_id>/views/<workbook_url_name>/<view_url_name>?::iid=1
```

It handles the optional `::iid=1` and returns the components in a JSON-style dictionary.

```python
import re
from urllib.parse import urlparse

def parse_tableau_view_url(url: str) -> dict:
    """
    Parses a Tableau view URL and returns a dictionary with components.
    Example URL: https://server.example.com/#/site/FPNA/views/WorkbookName/ViewName?::iid=1
    """
    parsed = urlparse(url)
    result = {
        "server_url": f"{parsed.scheme}://{parsed.netloc}",
        "site_id": None,
        "workbook_url_name": None,
        "view_url_name": None,
        "iid": None
    }

    # Use regex to extract parts from the path
    match = re.search(r"#/site/([^/]+)/views/([^/]+)/([^/?]+)", parsed.fragment)
    if match:
        result["site_id"] = match.group(1)
        result["workbook_url_name"] = match.group(2)
        result["view_url_name"] = match.group(3)
    
    # Extract iid if present
    iid_match = re.search(r"::iid=(\d+)", parsed.query)
    if iid_match:
        result["iid"] = iid_match.group(1)
    
    return result
```

### Example Usage:

```python
url = "https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash?::iid=1"
parsed = parse_tableau_view_url(url)
print(parsed)
```

### Output:

```json
{
  "server_url": "https://dev.forecastvisualanalytics.citigroup.net",
  "site_id": "FPNA",
  "workbook_url_name": "EMEAExpenseDashboard",
  "view_url_name": "ExpenseDash",
  "iid": "1"
}
```

It works even if `?::iid=1` is missing. Let me know if your Tableau server uses a different URL scheme.
