To convert a JSON **string column** in Databricks SQL to an **array of maps** with each map containing `key` and `value` fields, you can follow these steps:

---

### ✅ **Databricks SQL Solution**

```sql
SELECT
  TRANSFORM(
    MAP_ENTRIES(
      FROM_JSON(json_col, 'map<string,string>')
    ),
    entry -> NAMED_STRUCT('key', entry.key, 'value', entry.value)
  ) AS key_value_array
FROM your_table;
```

---

### 🔍 **Explanation**
- `FROM_JSON(json_col, 'map<string,string>')`: Parses the JSON string to a `Map<String, String>`.
- `MAP_ENTRIES(...)`: Converts the map to an array of structs with `key` and `value`.
- `TRANSFORM(..., entry -> NAMED_STRUCT(...))`: Ensures the structure is explicitly named as `key` and `value`.

---

### 🧪 Example Output
Given your JSON, the resulting array will look like:

```json
[
  {"key":"addr:city", "value":"Chicago"},
  {"key":"addr:housenumber", "value":"1258"},
  ...
]
```

