Excellent — yes, you should update the **`SYSTEM_PROMPT`** (or whichever constant defines your assistant’s reasoning context, often something like `ASSISTANT_SYSTEM_PROMPT` or `AGENT_DESCRIPTION`) so the LLM knows that this tool exists, when to use it, and what it does.

Here’s how you can **append the description for the new tool** inside your existing system prompt.

---

### ✅ Example System Prompt Addition

Locate the section of your prompt where existing tools are described — for example:

```python
SYSTEM_PROMPT = """
You are an intelligent assistant that uses graph database tools to answer user questions.

Available tools include:
- search_nodes_by_fields_tool: searches for nodes in the graph matching certain field criteria.
- check_if_project_is_approved_tool: checks if a project has been approved.
...
```

Now **add this entry for the new tool**:

```python
- get_project_attributes_to_correct_tool: Given a Project ID, retrieves all updated (overwritten) attributes and their original values for an approved project. 
  Returns a CSV-formatted summary of PSKU, Attribute Category, Attribute Name, Original Value, and Final Value. 
  If the project is not approved or has no updated attributes, returns a message instead.
```

---

### ✅ Full example snippet

```python
SYSTEM_PROMPT = """
You are an intelligent assistant that uses graph database tools to query and summarize data about Projects, Documents, PSKUs, and their relationships.

Available tools include:
- search_nodes_by_fields_tool: searches for nodes in the graph matching specific fields.
- check_if_project_is_approved_tool: determines whether a project node has been approved.
- get_project_attributes_to_correct_tool: Given a Project ID, retrieves all updated (overwritten) attributes and their original values for an approved project. 
  Returns a CSV-formatted summary of PSKU, Attribute Category, Attribute Name, Original Value, and Final Value. 
  If the project is not approved or has no updated attributes, returns a message instead.

You should select the appropriate tool based on the user query.
"""
```

---

### ✅ Why this matters

This gives the LLM:

* A **semantic clue** (“updated attributes”, “original values”, “approved project”) to trigger this tool when users ask *“which attributes were corrected or modified in this project?”*
* Enough context to know the **expected format** of the return (CSV text).

---

Would you like me to make this more **task-oriented** (e.g., phrased so the LLM autonomously decides *when* to call it vs. *when* to summarize results*) — like a production prompt for LangGraph agents?
