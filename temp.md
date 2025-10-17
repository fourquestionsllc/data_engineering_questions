Got it ✅ — you want to modify `get_project_attributes_to_correct()` so that:

1. It **first checks if the project is approved** using the existing `is_project_approved()` helper. If not approved → immediately return `None`.
2. It returns a **simplified table** with the following columns:

   ```
   PSKU | Attribute Category | Attribute Name | Original Value | Final Value
   ```

   * `Attribute Category` should be derived from the attribute name prefix or index if available (e.g., `verified_attr_index` or from the name).
   * `Original Value` comes from `orig_attr_value`
   * `Final Value` comes from `verified_attr_value`

Here’s the updated function implementation:

```python
def get_project_attributes_to_correct(project_id: str) -> pandas.DataFrame:
    """
    Identify all updated attributes and their original values for a given approved Project ID.

    Only runs if the Project is approved (has associated ProjectApproval node).

    Traverses:
    Project -> PSKU -> VerifiedDocAttribute (where overwritten_by_user == true)
             -> FromOrigAttr -> DocAttribute

    Args:
        project_id (str): The Project node ID.

    Returns:
        pandas.DataFrame: DataFrame with columns [PSKU, Attribute Category, Attribute Name, Original Value, Final Value]
                          or None if the project is not approved.
    """
    # --- 1️⃣ Check approval status ---
    if not is_project_approved(project_id):
        return None

    # --- 2️⃣ Run Gremlin query ---
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
     .select("psku", "verified_attr", "orig_attr")
     .by(valueMap(true))
    """

    bindings = {"project_id": project_id}
    query_results = (
        gremlin_utils.query_gremlin(query=query, bindings=bindings).all().result()
    )

    if not query_results:
        return pandas.DataFrame(
            columns=["PSKU", "Attribute Category", "Attribute Name", "Original Value", "Final Value"]
        )

    # --- 3️⃣ Flatten and extract relevant fields ---
    rows = []
    for r in query_results:
        # Flatten PSKU info
        psku_data = r.get("psku", {})
        verified_attr = r.get("verified_attr", {})
        orig_attr = r.get("orig_attr", {})

        def flatten(d):
            return {
                k: v[0] if isinstance(v, list) and len(v) == 1 else v
                for k, v in d.items()
            }

        psku_flat = flatten(psku_data)
        verified_flat = flatten(verified_attr)
        orig_flat = flatten(orig_attr)

        # Extract attribute category — use verified_attr_index if exists
        attr_category = verified_flat.get("index") or verified_flat.get("verified_attr_index") or "N/A"

        # Extract attribute name/value
        attr_name = (
            verified_flat.get("name")
            or verified_flat.get("verified_attr_name")
            or orig_flat.get("name")
            or orig_flat.get("orig_attr_name")
        )
        original_value = orig_flat.get("value") or orig_flat.get("orig_attr_value", "")
        final_value = verified_flat.get("value") or verified_flat.get("verified_attr_value", "")

        rows.append(
            {
                "PSKU": psku_flat.get("id") or psku_flat.get("pdr_part_number"),
                "Attribute Category": attr_category,
                "Attribute Name": attr_name,
                "Original Value": original_value,
                "Final Value": final_value,
            }
        )

    # --- 4️⃣ Return clean DataFrame ---
    df = pandas.DataFrame(
        rows,
        columns=["PSKU", "Attribute Category", "Attribute Name", "Original Value", "Final Value"],
    )
    return df
```

---

### ✅ Summary of Changes

* **Approval check:** Added at the start → if not approved, returns `None`.
* **Simplified output:** Only the required 5 columns.
* **Flattening logic simplified:** Clean extraction of nested fields.
* **Handles missing values gracefully:** Defaults to empty string or “N/A”.
* **Compatible with existing Gremlin query structure.**

---

Would you like me to also include an optional flag (e.g., `include_unapproved=False`) so you can toggle whether to skip the approval check or not? That can help with debugging and testing.
