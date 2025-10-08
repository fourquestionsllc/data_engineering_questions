Here’s the updated version of your function — it now returns **all fields** for `Document` nodes in **CSV format**, preserving the original column names from the graph instead of only using `["FILE NAME", "FILE TYPE", "SOURCE", "REVISION", "VERSION"]`.

```python
import pandas

def search_nodes_by_fields(
    node_type: str,
    search_params: dict,
    exact_match: bool = False,
) -> str:
    """
    Query the graph DB for nodes of a given type, matching on multiple fields.

    Supports exact and partial ("contains") matching.

    Args:
        node_type (str): The node type (Document or Project).
        search_params (dict): Field-value mapping to search by.
                              Example: {"id": "123", "doc_title": "design"}
        exact_match (bool): Whether to use exact matching (==) or partial matching (contains).

    Returns:
        str: For Document nodes, CSV-formatted string containing all fields.
             For other node types, list of flattened node dictionaries.
    """

    # Allowed searchable fields
    NODE_SEARCHABLE_FIELDS = {
        "Document": ["id", "doc_title", "file_name"],
        "Project": ["id", "title"],
    }

    if node_type not in NODE_SEARCHABLE_FIELDS:
        raise ValueError(f"Unsupported node_type: {node_type}")

    allowed_fields = NODE_SEARCHABLE_FIELDS[node_type]
    invalid_fields = [f for f in search_params if f not in allowed_fields]
    if invalid_fields:
        raise ValueError(
            f"Invalid fields {invalid_fields} for node_type {node_type}. "
            f"Allowed fields: {allowed_fields}"
        )

    # Build Gremlin traversal filters
    filter_clauses = []
    for field, value in search_params.items():
        if exact_match:
            clause = f'.has("{field}", {field})'
        else:
            clause = f'.has("{field}", TextP.containing({field}))'
        filter_clauses.append(clause)

    filters_str = "\n".join(filter_clauses)

    query = f"""
    g.V()
     .hasLabel(node_type)
     {filters_str}
     .valueMap(true)
    """

    bindings = {"node_type": node_type}
    bindings.update(search_params)

    query_results = (
        gremlin_utils.query_gremlin(query=query, bindings=bindings).all().result()
    )

    # Flatten attributes
    flattened = []
    for r in query_results:
        node_details = {}
        for k, v in r.items():
            if isinstance(v, list) and len(v) == 1:
                node_details[k] = v[0]
            else:
                node_details[k] = v

        # If Project, attach AssociatedPSKUTable
        if node_type == "Project" and "id" in node_details:
            node_details["AssociatedPSKUTable"] = get_project_pskus_with_gtin_salesorg(
                project_id=node_details["id"]
            )

        flattened.append(node_details)

    # For Document nodes — return all available fields as CSV
    if node_type == "Document":
        df = pandas.DataFrame(flattened)
        return df.to_csv(index=False)

    # For non-Document nodes — return list of dicts
    return flattened
```

### ✅ Key Changes:

* Returns **all available fields** for `Document` nodes (no custom column filtering).
* Uses `pandas.DataFrame(flattened)` directly — columns are inferred dynamically.
* Keeps `Project` logic intact (still returns Python list with associated PSKU table).
* Output for `Document` nodes is now **a CSV-formatted string** with all fields.

Would you like to keep clickable markdown `[file_name](doc_link)` formatting for CSV output, or prefer clean raw values (good for data exports)?
