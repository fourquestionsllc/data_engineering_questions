import os
from azure.cosmos import CosmosClient, exceptions

# Load env vars
from dotenv import load_dotenv
load_dotenv(".env")  # make sure this path matches your .env file name

# Get connection info from .env
connection_string = os.getenv("COSMOSDB_DOC_CONNECTION_STRING")
database_name = os.getenv("COSMOSDB_DOC_KA_CONVO_DATABASE")
container_name = os.getenv("COSMOSDB_DOC_KA_CONVO_CONTAINER")

# Initialize Cosmos client
client = CosmosClient.from_connection_string(connection_string)

# Get database and container references
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Example: query first 5 items
query = "SELECT TOP 5 * FROM c"

try:
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    print("Sample items from container:")
    for item in items:
        print(item)

except exceptions.CosmosHttpResponseError as e:
    print(f"Query failed: {e.message}")
