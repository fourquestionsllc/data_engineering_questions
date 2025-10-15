Perfect — since your project’s graph structure already uses consistent Gremlin patterns and utility helpers (like `gremlin_utils.query_gremlin`), we can **add a clean function** called `is_project_approved(project_id: str) -> bool` that checks whether a Project node has any associated node with `node_type="ProjectApproval"`.

Here’s the function you should append to your module 👇

---

```python
def is_project_approved(project_id: str) -> bool:
    """
    Check if a Project node is approved.

    A Project is considered approved if it has at least one connected node
    with node_type == "ProjectApproval" (via either incoming or outgoing edge).

    Args:
        project_id (str): The Project node identifier.

    Returns:
        bool: True if approved (has associated ProjectApproval node), else False.
    """
    query = """
    g.V()
     .hasLabel("Project")
     .has("id", project_id)
     .both()
     .has("node_type", "ProjectApproval")
     .limit(1)
     .count()
    """

    bindings = {"project_id": project_id}

    query_results = (
        gremlin_utils.query_gremlin(query=query, bindings=bindings).all().result()
    )

    # Cosmos Gremlin returns a list like [{'count': 1}] or [1]
    count_value = 0
    if query_results:
        result = query_results[0]
        if isinstance(result, dict) and "count" in result:
            count_value = result["count"]
        elif isinstance(result, (int, float)):
            count_value = result

    return count_value > 0
```

---

### ✅ Explanation

* It starts from the `Project` vertex that matches the given `id`.
* `.both()` explores **both incoming and outgoing** connections (you can replace with `.out()` if the relationship is always directed out of the Project).
* `.has("node_type", "ProjectApproval")` filters only the approval node.
* `.limit(1).count()` ensures we don’t traverse unnecessary connections — we only care whether at least one exists.
* Returns `True` if at least one exists, otherwise `False`.

---

### 🔍 Example Usage

```python
if is_project_approved("PRJ-12345"):
    print("✅ Project PRJ-12345 is approved.")
else:
    print("❌ Project PRJ-12345 is not approved.")
```

---

Would you like me to extend this function to optionally **return the approval node’s details** (instead of just True/False)? That’s useful if you later want to show who approved it or when it was approved.
