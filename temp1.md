Got it ✅ — since your `.env` contains both **Cosmos DB SQL API (DocumentDB)** and **Cosmos DB Gremlin API (Graph DB)** connections, I’ll give you working Python examples for each.

We’ll first load credentials from `.env` and then query the DB.

---

## 1. Setup

Install dependencies:

```bash
pip install python-dotenv azure-cosmos gremlinpython
```

Your project should have:

```
.env
main.py
```

---

## 2. Python Code

```python
import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey
from gremlin_python.driver import client, serializer

# Load environment variables
load_dotenv()

### -----------------------------
### Cosmos DB SQL API (DocumentDB)
### -----------------------------
def query_cosmos_sql():
    conn_str = os.getenv("COSMOSDB_DOC_CONNECTION_STRING")
    database_name = os.getenv("COSMOSDB_DOC_KA_CONVO_DATABASE")
    container_name = os.getenv("COSMOSDB_DOC_KA_CONVO_CONTAINER")

    # Parse connection string manually
    parts = dict(item.split("=", 1) for item in conn_str.strip(";").split(";") if item)
    endpoint = parts.get("AccountEndpoint")
    key = parts.get("AccountKey")

    client_sql = CosmosClient(endpoint, credential=key)
    db = client_sql.get_database_client(database_name)
    container = db.get_container_client(container_name)

    query = "SELECT TOP 5 * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    print("\n--- SQL API Query Result ---")
    for item in items:
        print(item)


### -----------------------------
### Cosmos DB Gremlin API (Graph)
### -----------------------------
def query_cosmos_gremlin():
    gremlin_endpoint = os.getenv("COSMOSDB_GREMLIN_ENDPOINT")
    gremlin_key = os.getenv("COSMOSDB_GREMLIN_KEY")
    database = os.getenv("COSMOSDB_GREMLIN_DB")
    graph = os.getenv("COSMOSDB_GREMLIN_GRAPH")

    gremlin_client = client.Client(
        gremlin_endpoint, "g",
        username=f"/dbs/{database}/colls/{graph}",
        password=gremlin_key,
        message_serializer=serializer.GraphSONSerializersV2d()
    )

    try:
        callback = gremlin_client.submitAsync("g.V().limit(5)")
        if callback.result() is not None:
            results = callback.result().all().result()
            print("\n--- Gremlin Query Result ---")
            for r in results:
                print(r)
    except Exception as e:
        print("Gremlin query error:", e)
    finally:
        gremlin_client.close()


if __name__ == "__main__":
    query_cosmos_sql()
    query_cosmos_gremlin()
```

---

## 3. What This Does

* **SQL API**: Queries the first 5 documents in `KAConvoHistory` container.
* **Gremlin API**: Queries the first 5 vertices in `skygraph_devsit`.

---

👉 Do you want me to also show how to **insert data** (both SQL and Gremlin), or just querying is enough for your case?
