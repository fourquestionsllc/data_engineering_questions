Here’s the **newly added function** to identify attributes to correct for a project by its ID — based on your provided Gremlin query logic:

```python
def get_project_attributes_to_correct(project_id: str) -> pandas.DataFrame:
    """
    Identify all updated attributes and their original values for a given Project ID.

    Traverses:
    Project -> PSKU -> VerifiedDocAttribute (where overwritten_by_user == true)
             -> FromOrigAttr -> DocAttribute

    Args:
        project_id (str): The Project node ID.

    Returns:
        pandas.DataFrame: DataFrame containing project, psku, verified_attr, and orig_attr details.
    """
    query = """
    g.V()
     .has("label", "Project")
     .has("id", project_id)
     .as("project")
     .out()
     .has("label", "PSKU")
     .as("psku")
     .out()
     .has("label", "VerifiedDocAttribute")
     .where(__.has("overwritten_by_user", true))
     .as("verified_attr")
     .out("FromOrigAttr")
     .has("label", "DocAttribute")
     .as("orig_attr")
     .select("project", "psku", "verified_attr", "orig_attr")
     .by(valueMap(true))
    """

    bindings = {"project_id": project_id}

    query_results = (
        gremlin_utils.query_gremlin(query=query, bindings=bindings).all().result()
    )

    # Flatten nested valueMaps and structure as tabular data
    rows = []
    for r in query_results:
        row = {}
        for key in ["project", "psku", "verified_attr", "orig_attr"]:
            node_data = r.get(key, {})
            flat_node = {}
            for k, v in node_data.items():
                flat_node[k] = v[0] if isinstance(v, list) and len(v) == 1 else v
            # Prefix to avoid column name clashes
            for attr, val in flat_node.items():
                row[f"{key}_{attr}"] = val
        rows.append(row)

    return pandas.DataFrame(rows)
```
