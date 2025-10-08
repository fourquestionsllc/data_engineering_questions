Here’s the modified version of your function — it now returns **all available fields** from the Gremlin query in CSV format, without restricting to the predefined column list.

```python
import pandas

def get_documents_for_psku(psku_id: str) -> str:
    """
    Query all Document nodes associated with a given PSKU (both incoming and outgoing edges).
    Return all fields as a CSV-formatted string.

    Args:
        psku_id (str): The PSKU node identifier.

    Returns:
        str: CSV-formatted string containing all available fields for Document nodes.
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
        docs_data.append(node_details)

    # Create a DataFrame with all keys (columns)
    df = pandas.DataFrame(docs_data)

    # Return the entire dataframe as CSV
    return df.to_csv(index=False)
```

✅ **What changed:**

* Removed the restriction to specific columns (`["FILE NAME", "FILE TYPE", "SOURCE", "REVISION", "VERSION"]`).
* Kept all available fields as-is from the Gremlin `valueMap(true)` result.
* Still flattens one-element lists for readability.
* Output remains a valid CSV string with **all node properties**.

Would you like me to keep the clickable markdown links (`[file_name](doc_link)`) for `file_name` + `doc_link` pairs, or remove those too for a clean raw CSV?
