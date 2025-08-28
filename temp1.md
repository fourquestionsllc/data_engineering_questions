Perfect 👍 You’re using **Azure CosmosDB Gremlin API** (graph database). To query it, you can use the **Gremlin Python client** (`gremlinpython`).

Here’s an example script that connects and queries a few nodes from your graph:

```python
import os
from dotenv import load_dotenv
from gremlin_python.driver import client, serializer

# Load environment variables
load_dotenv(".env")

endpoint = os.getenv("COSMOSDB_GREMLIN_ENDPOINT")
database = os.getenv("COSMOSDB_GREMLIN_DB")
graph = os.getenv("COSMOSDB_GREMLIN_GRAPH")
primary_key = os.getenv("COSMOSDB_GREMLIN_KEY")

# Cosmos Gremlin client
gremlin_client = client.Client(
    endpoint,
    'g',
    username=f"/dbs/{database}/colls/{graph}",
    password=primary_key,
    message_serializer=serializer.GraphSONSerializersV2d()
)

def run_query(query):
    print(f"\nRunning: {query}")
    try:
        callback = gremlin_client.submitAsync(query)
        if callback.result() is not None:
            for result in callback.result():
                print(result)
        else:
            print("No results.")
    except Exception as e:
        print(f"Query failed: {e}")

# Example: get first 5 vertices
run_query("g.V().limit(5)")

# Example: get first 5 edges
run_query("g.E().limit(5)")

gremlin_client.close()
```

---

### Steps to run:

1. Install dependencies:

   ```bash
   pip install gremlinpython python-dotenv
   ```
2. Save your `.env` file with the values you posted.
3. Run the script → it should print up to 5 vertices and 5 edges from your Cosmos Gremlin graph.

---

👉 Do you want me to also include an **insert sample vertex/edge** snippet (in case your graph is empty, so queries return nothing)?
