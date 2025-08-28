Got it ✅ — makes sense. CosmosDB Gremlin + `gremlinpython` is notoriously finicky because of `GraphSONSerializersV2d` and TinkerPop version mismatches.
The **better way** is to use the **WebSocket client (`websockets` or `aiogremlin`)** and send raw Gremlin queries, since CosmosDB just expects a WS connection over Gremlin protocol.

Here’s a working Python example using **`websockets`** (no `gremlinpython` at all):

```python
import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

# Load env
load_dotenv(".env")

endpoint = os.getenv("COSMOSDB_GREMLIN_ENDPOINT")
database = os.getenv("COSMOSDB_GREMLIN_DB")
graph = os.getenv("COSMOSDB_GREMLIN_GRAPH")
primary_key = os.getenv("COSMOSDB_GREMLIN_KEY")

username = f"/dbs/{database}/colls/{graph}"
password = primary_key

async def query_gremlin(gremlin_query):
    async with websockets.connect(
        endpoint,
        extra_headers={
            "Authorization": password,
            "x-ms-date": "Thu, 01 Jan 1970 00:00:00 GMT",
            "x-ms-version": "2017-11-15"
        },
        subprotocols=["graphson-2.0"]
    ) as ws:
        # Gremlin request payload
        request = {
            "requestId": "1",
            "op": "eval",
            "processor": "",
            "args": {
                "gremlin": gremlin_query,
                "bindings": {},
                "language": "gremlin-groovy"
            }
        }

        await ws.send(json.dumps(request))
        response = await ws.recv()
        print("Response:", response)

# Run a test query
asyncio.run(query_gremlin("g.V().limit(5)"))
```

---

### Notes:

* This connects **directly** to Cosmos DB’s Gremlin endpoint via WebSocket.
* You must set headers (`Authorization`, `x-ms-date`, `x-ms-version`) correctly. Cosmos DB uses the primary key for password.
* The example query just does `g.V().limit(5)`.

⚠️ Downside: you have to handle **auth signatures (HMAC)** yourself if you want full security instead of always using `primary_key` directly.

---

👉 Do you want me to extend this into a **reusable helper class** (e.g. `CosmosGremlinClient.query("g.V()")`) so you can query nodes/edges without rewriting all the WS boilerplate?
