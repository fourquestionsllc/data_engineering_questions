Here’s a **Gremlin query** to list all **unique `node_type` values** in your graph:

```groovy
g.V().
  values("node_type").
  dedup().
  order().
  toList()
```

### 🧠 Explanation:

* `values("node_type")` → extracts the value of the `node_type` property from each vertex.
* `dedup()` → removes duplicates (returns only unique values).
* `order()` → sorts the results alphabetically.
* `toList()` → materializes the results as a list (useful when running the query in most Gremlin clients).

---

✅ **Azure Cosmos DB compatible version:**

```groovy
g.V().
  values("node_type").
  dedup().
  order()
```

(Cosmos automatically returns the list format when queried through SDKs or Data Explorer.)

Would you like me to modify this to also **count how many nodes exist per `node_type`** (i.e., return a frequency table)?
