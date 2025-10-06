Perfect — since your new function `get_documents_for_psku` is defined in `query_project_hierarchy_utils`, and you want it to be callable by the **Project Information Assistant**, here’s **exactly** what to add and where 👇

---

### ✅ Step 1: Wrap your new function with `@tool`

In the same file (where your other tools are defined), **after the existing tools**, add this:

```python
@tool
def search_graph_db_for_documents_by_psku(psku_id: str) -> str:
    """
    Given a PSKU ID, return all connected Document nodes (both incoming and outgoing edges)
    as a CSV-formatted string with columns:
    [FILE NAME, FILE TYPE, SOURCE, REVISION, VERSION].
    """
    return query_project_hierarchy_utils.get_documents_for_psku(psku_id)
```

---

### ✅ Step 2: Add it to the assistant’s tool list

Find the existing list named `PROJECT_INFORMATION_ASSISTANT_TOOLS`:

```python
PROJECT_INFORMATION_ASSISTANT_TOOLS = [
    search_graph_db_for_project_info,
    search_graph_db_for_node_details,
    search_graph_db_for_nodes_by_fields,
    search_graph_db_for_projects_and_pskus_by_gtin,
    CompleteOrEscalate,
]
```

Add your new tool (`search_graph_db_for_documents_by_psku`) **before `CompleteOrEscalate`**, like this:

```python
PROJECT_INFORMATION_ASSISTANT_TOOLS = [
    search_graph_db_for_project_info,
    search_graph_db_for_node_details,
    search_graph_db_for_nodes_by_fields,
    search_graph_db_for_projects_and_pskus_by_gtin,
    search_graph_db_for_documents_by_psku,  # 👈 new tool added here
    CompleteOrEscalate,
]
```

---

### ✅ Step 3: (Optional but recommended) Mention it in the system prompt

If you want the LLM to **automatically know** when to use it, update the `SYSTEM_PROMPT` section under “Other Available tools” by adding one line:

```
- search_graph_db_for_documents_by_psku: Use when the user provides a PSKU ID and requests to retrieve all associated Documents (labels, IFUs, etc.) for that PSKU.
```

---

### ✅ Summary

**You added:**

1. One new `@tool` wrapper function calling your `query_project_hierarchy_utils.get_documents_for_psku`.
2. One line in `PROJECT_INFORMATION_ASSISTANT_TOOLS` list.
3. (Optional) One line in the system prompt description.

---

That’s it.
Once done, your assistant will be able to handle user queries like:

> “Show me all documents related to PSKU 12345”

and it will automatically call `search_graph_db_for_documents_by_psku(psku_id="12345")`.
