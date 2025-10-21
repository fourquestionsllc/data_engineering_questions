Perfect — you only need to make **two small but clear edits**:

---

### ✅ 1️⃣ **Update `SYSTEM_PROMPT`**

Add this instruction so the LLM always formats document results as tables:

```python
SYSTEM_PROMPT = """
...
When returning document-related results (e.g., file names, file types, sources, revisions, versions), 
always present them in a clean table format with appropriate column headers, 
not as a list or plain text.
...
"""
```

📍You can insert that new paragraph right before **“Other Available tools:”** in the prompt.

---

### ✅ 2️⃣ **Modify `search_graph_db_for_documents_by_psku` tool**

Replace its `return` statement with a table-formatted string:

```python
@tool
def search_graph_db_for_documents_by_psku(psku_id: str) -> str:
    """
    Given a PSKU ID, return all connected Document nodes (both incoming and outgoing edges)
    as a table with columns:
    [FILE NAME, FILE TYPE, SOURCE, REVISION, VERSION].
    """
    df = query_project_hierarchy_utils.get_documents_for_psku(psku_id)

    if df is None or df.empty:
        return f"No documents found for PSKU {psku_id}."

    # ✅ Return as Markdown-style table for consistent rendering
    return df.to_markdown(index=False)
```

---

### ✅ Optional (for completeness)

If **any** other document-returning tools exist (like `search_graph_db_for_project_info` when `target_node_type == "Document"`), you can apply a similar pattern:

```python
if target_node_type.lower() == "document" and not hierarchy_search_results.empty:
    return hierarchy_search_results.to_markdown(index=False)
```

---

### 💡 Summary of changes

| File Section                            | Action                                             | Code             |
| --------------------------------------- | -------------------------------------------------- | ---------------- |
| `SYSTEM_PROMPT`                         | Add instruction to always show documents as tables | *see snippet #1* |
| `search_graph_db_for_documents_by_psku` | Return Markdown-formatted table                    | *see snippet #2* |

---

Would you like me to show the exact modified sections inline within your existing code (so you can copy-paste directly)?
