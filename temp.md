Here’s how you can **add the `get_project_attributes_to_correct` function as a LangChain tool** in your assistant file — so it can be called like the other graph tools.

Add the following code snippet **after** the existing tools (e.g., right after `check_if_project_is_approved` if it exists, or near `search_graph_db_for_project_info`) and **make sure to import pandas** if not already.

---

### ✅ Code Addition

```python
@tool
def get_project_attributes_to_correct_tool(project_id: str) -> str:
    """
    Retrieve all updated attributes and their original values for an approved Project.

    This tool uses query_project_hierarchy_utils.get_project_attributes_to_correct(project_id)
    to identify VerifiedDocAttributes that were overwritten by users and their original values.

    Args:
        project_id (str): The Project node identifier.

    Returns:
        str: CSV-formatted string containing PSKU, Attribute Category, Attribute Name,
             Original Value, and Final Value. Returns a message if project not approved
             or no attributes to correct.
    """
    df = query_project_hierarchy_utils.get_project_attributes_to_correct(project_id)

    if df is None:
        return f"Project {project_id} is not approved or has no ProjectApproval node."

    if df.empty:
        return f"No updated attributes found for Project {project_id}."

    return df.to_csv(index=False)
```

---

### ✅ Make sure imports are present at the top:

If not already imported, add:

```python
import pandas
from skybound_knowledge_graph import query_project_hierarchy_utils
```

---

### ✅ Tool behavior

* Checks if the project is approved via `is_project_approved`.
* Returns CSV-formatted results (for readability in chat or export).
* Gracefully handles cases where no updates or approval exist.

---

Would you like me to also update the `SYSTEM_PROMPT` section to mention this new tool (so the assistant can autonomously choose it when appropriate)?
