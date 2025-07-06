Here's the complete Python `requests`-based POST code for the given API information. This example assumes you already have a valid JWT token (e.g., `jwt_token`) obtained after login.

```python
import requests

# Endpoint URL
url = "https://sit.fpnavisualanalyticsreporting.citigroup.net/var/api/v1/monitoring/tableau/createJob?isRuntimeRequest=true"

# JWT token (replace with actual token)
jwt_token = "your_jwt_token_here"

# Headers
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}

# Payload
payload = {
    "tableauDownloadJob": {
        "id": "chatbot1",
        "name": "chatbot1",
        "fileName": "chatbot1",
        "fileType": "PDF",
        "tableausource": "y",
        "actvInd": "A",
        "scheduleId": None,
        "effectivestartot": None,
        "effectiveEndot": None,
        "jobGroUp": "TABLEAU DOWNLOAD",
        "jObTypE": "TABLEAU DOWNLOAD",
        "sla": 8,
        "retriggerFlag": None,
        "successAlertEmail": None,
        "slaBreachMail": None,
        "failureAlertMail": None,
        "channel": "chatbot"  # added to identify source
    },
    "workbooksViewscustomviewsMap": {
        "1W COGNOS": "98e5f82f-cc98-4195-ae31-f68a74d1e68b",
        "2cvQBR customview": "QBR customview",
        "3vNavigation": "efb58cd3-4dc8-488d-8ed9-c6ccf73a484b",
        "4cvvLoans summary": "b400f4f0-abab-4dd7-a858-15c3e58d4651"
    },
    "subscribers": [
        "AK89626",
        "MM63148"
    ],
    "pipelineId": "881"
}

# Make POST request
response = requests.post(url, json=payload, headers=headers, verify=False)  # Set verify=True if SSL cert is valid

# Check response
if response.status_code == 201:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
```

### Notes:

* Replace `"your_jwt_token_here"` with your actual JWT token.
* `verify=False` is used to bypass SSL certificate checks (typical in internal staging environments); remove it in production.
* Ensure all required fields are filled and field names are **case-sensitive**.
* The malformed quotes and commas in your sample were corrected for proper JSON.

