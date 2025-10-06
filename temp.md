Perfect — here’s exactly what you need to **change and add** inside the `search_nodes_by_fields()` function.

---

### ✅ Step 1: Replace the **return block** at the end of `search_nodes_by_fields()`

Find this section:

```python
    return flattened
```

---

### 🚀 Replace it with:

```python
    if node_type == "Document":
        # Extract relevant columns and format into a DataFrame
        docs_data = []
        for node in flattened:
            file_name = node.get("file_name")
            doc_link = node.get("doc_link")
            source = node.get("source_system")
            revision = node.get("mdv_version")
            file_type = None
            if file_name:
                if file_name.lower().endswith(".pdf"):
                    file_type = "pdf"
                elif file_name.lower().endswith(".zip"):
                    file_type = "zip"

            docs_data.append({
                "FILE NAME": f"[{file_name}]({doc_link})" if file_name and doc_link else file_name,
                "FILE TYPE": file_type,
                "SOURCE": source,
                "REVISION": revision,
                "VERSION": node.get("mdv_doc_number"),
            })

        df = pandas.DataFrame(docs_data, columns=["FILE NAME", "FILE TYPE", "SOURCE", "REVISION", "VERSION"])
        return df.to_csv(index=False)

    return flattened
```

---

### ✅ Summary of what this change does

* If the search is for `Document` nodes, it:

  * Converts results into a DataFrame.
  * Includes only the specified columns:
    **FILE NAME (as link), FILE TYPE, SOURCE, REVISION, VERSION.**
  * Returns the result as a **CSV-formatted string** (`to_csv(index=False)`).
* Keeps the old behavior (`return flattened`) for all other node types.

---

### 🧩 You don’t need to modify any other part of the code.

Only this replacement at the end of `search_nodes_by_fields()` is required.
