# 🐳 Deploy MongoDB with Docker and Access It Using Python: An End-to-End Tutorial

MongoDB is a popular NoSQL database often used in modern web and data applications. In this blog post, we'll show you how to:

1. Pull and run MongoDB using Docker.
2. Interact with it using Python (create a collection, insert documents, and query them).
3. Clean up the environment.

Let’s dive in!

---

## 🧰 Prerequisites

Before we start, ensure you have the following installed:

* Docker: [Install Docker](https://docs.docker.com/get-docker/)
* Python 3.7+ (with `pip`)
* `pymongo` library for MongoDB interaction:

  ```bash
  pip install pymongo
  ```

---

## 🐳 Step 1: Pull MongoDB Docker Image and Run the Container

Let’s start by pulling the latest MongoDB Docker image and running it as a container.

### 🔧 Action 1: Pull the MongoDB Image

```bash
docker pull mongo
```

### 🔧 Action 2: Run the MongoDB Container

```bash
docker run -d \
  --name mongodb-container \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo
```

✅ This will:

* Run MongoDB in detached mode (`-d`)
* Name the container `mongodb-container`
* Map host port `27017` to container port `27017`
* Set up root credentials (`admin` / `secret`)

You can check if the container is running:

```bash
docker ps
```

---

## 🐍 Step 2: Connect to MongoDB from Python

Create a new Python script (`mongo_demo.py`) and use `pymongo` to connect and interact with the MongoDB server.

### 📄 Code: `mongo_demo.py`

```python
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://admin:secret@localhost:27017/")

# Step 2: Create or access a database
db = client["test_database"]

# Step 3: Create or access a collection
collection = db["users"]

# Step 4: Insert documents
users = [
    {"name": "Alice", "age": 28, "email": "alice@example.com"},
    {"name": "Bob", "age": 34, "email": "bob@example.com"},
    {"name": "Charlie", "age": 25, "email": "charlie@example.com"}
]
result = collection.insert_many(users)
print(f"Inserted document IDs: {result.inserted_ids}")

# Step 5: Query documents
print("All users:")
for user in collection.find():
    print(user)

# Step 6: Query with filter
print("\nUsers older than 30:")
for user in collection.find({"age": {"$gt": 30}}):
    print(user)
```

### ▶️ Run It

```bash
python mongo_demo.py
```

---

## 🔍 Expected Output

```plaintext
Inserted document IDs: [ObjectId(...), ObjectId(...), ObjectId(...)]
All users:
{'_id': ObjectId(...), 'name': 'Alice', 'age': 28, 'email': 'alice@example.com'}
{'_id': ObjectId(...), 'name': 'Bob', 'age': 34, 'email': 'bob@example.com'}
{'_id': ObjectId(...), 'name': 'Charlie', 'age': 25, 'email': 'charlie@example.com'}

Users older than 30:
{'_id': ObjectId(...), 'name': 'Bob', 'age': 34, 'email': 'bob@example.com'}
```

---

## 🧼 Step 3: Clean Up (Optional)

To stop and remove the MongoDB container:

```bash
docker stop mongodb-container
docker rm mongodb-container
```

---

## 🧠 Recap

In this tutorial, you:

✅ Pulled and ran MongoDB in Docker
✅ Connected to it using Python via `pymongo`
✅ Created a database and collection
✅ Inserted and queried documents

This setup is perfect for development and testing. In production, consider using persistent volumes, authentication best practices, and replica sets.

---

## 🧩 Next Steps

* Explore MongoDB Atlas for cloud-hosted DBs
* Use ODMs like MongoEngine
* Learn MongoDB aggregation pipelines
* Add indexing and performance tuning

