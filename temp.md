Here's a Python function that parses a Tableau view URL of the format:

```
https://<server_url>/#/site/<site_id>/views/<workbook_url_name>/<view_url_name>?::iid=1
```

and returns the components as a JSON object (Python dictionary):

```python
import re
from urllib.parse import urlparse

def parse_tableau_view_url(url: str) -> dict:
    pattern = re.compile(
        r"https://(?P<server_url>[^/]+)/#/site/(?P<site_id>[^/]+)/views/(?P<workbook_url_name>[^/]+)/(?P<view_url_name>[^?]+)(\?::iid=(?P<iid>\d+))?"
    )

    match = pattern.match(url)
    if not match:
        raise ValueError("URL does not match the expected Tableau view format")

    result = match.groupdict()
    # Ensure 'iid' key is always present
    if result["iid"] is None:
        result["iid"] = ""

    return result
```

### Example usage:

```python
url1 = "https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash?::iid=1"
url2 = "https://dev.forecastvisualanalytics.citigroup.net/#/site/FPNA/views/EMEAExpenseDashboard/ExpenseDash"

print(parse_tableau_view_url(url1))
# Output:
# {
#     'server_url': 'dev.forecastvisualanalytics.citigroup.net',
#     'site_id': 'FPNA',
#     'workbook_url_name': 'EMEAExpenseDashboard',
#     'view_url_name': 'ExpenseDash',
#     'iid': '1'
# }

print(parse_tableau_view_url(url2))
# Output:
# {
#     'server_url': 'dev.forecastvisualanalytics.citigroup.net',
#     'site_id': 'FPNA',
#     'workbook_url_name': 'EMEAExpenseDashboard',
#     'view_url_name': 'ExpenseDash',
#     'iid': ''
# }
```

Let me know if you want this to support optional `/site/<site_id>` (some Tableau URLs omit the site part).
