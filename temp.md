Here’s the **Gremlin query** to search for nodes whose `node_type` **contains** the word `"Approval"` (i.e., a fuzzy/partial match like SQL’s `%Approval%`):

```groovy
g.V().
  hasLabel("Node").          // Optional — remove if your graph has multiple labels
  has("node_type", textRegex("(?i).*Approval.*")). // case-insensitive partial match
  valueMap(true)
```

### Explanation:

* `has("node_type", textRegex("(?i).*Approval.*"))`:

  * Uses a **regular expression** for partial match (`.*Approval.*` = contains “Approval”).
  * `(?i)` makes it **case-insensitive**.
* `valueMap(true)` returns **all properties**, including the ID and label.

If you’re using **Azure Cosmos DB Gremlin API**, the same query works — just note that:

* Cosmos supports **`textRegex()`** for string property regex filters.
* You can omit the label if you don’t have a specific vertex label.

---

✅ **Cosmos DB Compatible Example:**

```groovy
g.V().
  has("node_type", textRegex("(?i).*Approval.*")).
  valueMap(true)
```

Would you like me to modify this query to **return the result in JSON format** (e.g., for API use or Python client integration)?
