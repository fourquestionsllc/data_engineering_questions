Got it ✅ — you want a new function to fetch all **documents linked to a PSKU** (via both incoming and outgoing edges), and return them as a **CSV-formatted table** with the same formatting you already use for `search_nodes_by_fields` (for Documents).

Here’s the function you can add:

```python
def get_documents_for_psku(psku_id: str) -> str:
    """
    Query all Document nodes associated with a given PSKU (both incoming and outgoing edges).
    Return the results as a CSV-formatted string.

    Args:
        psku_id (str): The PSKU node identifier.

    Returns:
        str: CSV-formatted string with columns [FILE NAME, FILE TYPE, SOURCE, REVISION, VERSION].
    """

    query = """
    g.V()
     .hasLabel("PSKU")
     .has("id", psku_id)
     .both()
     .hasLabel("Document")
     .valueMap(true)
    """

    bindings = {"psku_id": psku_id}

    query_results = (
        gremlin_utils.query_gremlin(query=query, bindings=bindings).all().result()
    )

    docs_data = []
    for record in query_results:
        # Flatten attributes
        node_details = {}
        for k, v in record.items():
            if isinstance(v, list) and len(v) == 1:
                node_details[k] = v[0]
            else:
                node_details[k] = v

        file_name = node_details.get("file_name")
        doc_link = node_details.get("doc_link")
        source = node_details.get("source_system")
        revision = node_details.get("mdv_version")
        version = node_details.get("mdv_doc_number")

        # Detect file type
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
            "VERSION": version,
        })

    df = pandas.DataFrame(docs_data, columns=["FILE NAME", "FILE TYPE", "SOURCE", "REVISION", "VERSION"])
    return df.to_csv(index=False)
```

---

Would you also like me to make this **generalizable** (e.g., `get_documents_for_node(node_type, node_id)`) so you could reuse it for **Projects** or other node types too, instead of just hardcoding for PSKU?
