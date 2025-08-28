Got it 👍 — you want to query Cosmos DB **Graph API (Gremlin)** from Python **without using `gremlinpython`**, since it often fails on Cosmos due to the `GraphSONSerializersV2d` incompatibility.

The alternative is to use **`requests`** (or `aiohttp`) to send Gremlin queries directly to the Cosmos DB Gremlin endpoint over HTTPS REST.

Here’s a clean Python example using `requests`:

```python
import os
import requests
import base64
import hmac
import hashlib
import datetime
from urllib.parse import quote
from dotenv import load_dotenv

# Load .env
load_dotenv(".env")

# Read env vars
endpoint = os.getenv("COSMOSDB_GREMLIN_ENDPOINT").replace("wss://", "https://")  # REST requires https
database = os.getenv("COSMOSDB_GREMLIN_DB")
graph = os.getenv("COSMOSDB_GREMLIN_GRAPH")
key = os.getenv("COSMOSDB_GREMLIN_KEY")

# Prepare REST API URL
url = f"{endpoint}dbs/{database}/colls/{graph}"

# Helper to build auth header (HMAC-SHA256)
def build_auth_token(verb, resource_type, resource_link, date, key):
    key_bytes = base64.b64decode(key)
    text = f"{verb.lower()}\n{resource_type.lower()}\n{resource_link}\n{date.lower()}\n\n"
    body = text.encode("utf-8")
    sig = base64.b64encode(hmac.new(key_bytes, body, hashlib.sha256).digest()).decode()
    return f"type=master&ver=1.0&sig={sig}"

# Build request
verb = "POST"
resource_type = "docs"
resource_link = f"dbs/{database}/colls/{graph}"
utc_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
auth_token = build_auth_token(verb, resource_type, resource_link, utc_date, key)

headers = {
    "Authorization": auth_token,
    "x-ms-date": utc_date,
    "x-ms-version": "2018-12-31",
    "Content-Type": "application/query+json"
}

# Example Gremlin query (get 5 vertices)
query = {"query": "g.V().limit(5)"}

# Send request
response = requests.post(url, headers=headers, json=query)

# Show results
if response.status_code == 200:
    data = response.json()
    print("Query results:")
    for item in data.get("Documents", []):
        print(item)
else:
    print(f"Error {response.status_code}: {response.text}")
```

### Explanation:

* Cosmos Graph API supports **REST queries** with the header `application/query+json`.
* We generate a **master key auth token** manually (HMAC-SHA256).
* The query payload is simply JSON:

  ```json
  {"query": "g.V().limit(5)"}
  ```
* This returns the first 5 vertices from your graph.

---

⚠️ Note:

* This bypasses `gremlinpython` completely, so no `GraphSONSerializersV2d` issue.
* The **REST API is slower** than WebSocket (`wss`), but stable for scripting/testing.

---

👉 Do you want me to also give you an **async `aiohttp` version** so you can run multiple Gremlin queries in parallel?
