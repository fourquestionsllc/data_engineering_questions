Got it 👍. Since you’re connecting to **Azure CosmosDB Gremlin API**, the Python SDK you’ll want to use is `gremlinpython`. CosmosDB requires **GraphSON v3** serializer (v2 will break, as you noted).

Here’s a clean example showing how to load credentials from your `.env` file, create a connection, and run a simple query to fetch nodes:

```python
import os
from gremlin_python.driver import client, serializer
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")   # update filename if not named .env

# Read values
COSMOSDB_GREMLIN_DB = os.getenv("COSMOSDB_GREMLIN_DB")
COSMOSDB_GREMLIN_GRAPH = os.getenv("COSMOSDB_GREMLIN_GRAPH")
COSMOSDB_GREMLIN_ENDPOINT = os.getenv("COSMOSDB_GREMLIN_ENDPOINT")
COSMOSDB_GREMLIN_KEY = os.getenv("COSMOSDB_GREMLIN_KEY")

# CosmosDB requires database and collection info in the path
HOST = COSMOSDB_GREMLIN_ENDPOINT
DATABASE = COSMOSDB_GREMLIN_DB
GRAPH = COSMOSDB_GREMLIN_GRAPH
USERNAME = f"/dbs/{DATABASE}/colls/{GRAPH}"
PASSWORD = COSMOSDB_GREMLIN_KEY

# Create Gremlin client (GraphSON v3 to avoid v2 errors)
gremlin_client = client.Client(
    HOST,
    "g",
    username=USERNAME,
    password=PASSWORD,
    message_serializer=serializer.GraphSONSerializersV3d()
)

# Example query: fetch first 5 vertices
query = "g.V().limit(5)"

try:
    print(f"Running query: {query}")
    callback = gremlin_client.submitAsync(query)
    if callback.result() is not None:
        for result in callback.result():
            print(result)
    else:
        print("No results found.")
finally:
    gremlin_client.close()
```

### Key Points:

* ✅ Uses `GraphSONSerializersV3d()` (required by CosmosDB Gremlin API).
* ✅ Reads from `.env` so secrets stay out of your code.
* ✅ Example query `g.V().limit(5)` fetches sample nodes.
* ✅ Avoids `GraphSONSerializersV2d` (which causes Cosmos errors).

---

Do you want me to also show you how to **query edges** (e.g., `g.E().limit(5)`) and traverse relationships in CosmosDB, or just fetching vertices is enough for your use case?
