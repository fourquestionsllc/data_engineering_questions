Here’s the **Gremlin query** to update a boolean property (field) from `false` to `true` for a specific node by ID 👇

---

### ✅ **If the ID is the system vertex ID**

```groovy
g.V("123").
  property("your_field_name", true)
```

---

### ✅ **If the ID is stored as a property (e.g., `node_id`)**

```groovy
g.V().
  has("node_id", "123").
  property("your_field_name", true)
```

---

### 🧠 **Explanation**

* `g.V("123")`: finds the vertex by its system ID.
* `has("node_id", "123")`: finds the vertex by a property ID (if your graph uses custom IDs).
* `property("your_field_name", true)`: updates or creates the property with value `true`.

---

### ✅ **Optional – Only update if currently false**

If you want to **change it only if it’s currently `false`**, you can add a conditional check:

```groovy
g.V().
  has("node_id", "123").
  has("your_field_name", false).
  property("your_field_name", true)
```

This ensures it only updates nodes where the field explicitly equals `false`.

---

Would you like me to extend this query so it updates **multiple node IDs in a list** at once?
