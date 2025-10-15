Here’s the **newly added code only** that integrates the `is_project_approved` tool into your `project_info_assistant.py` file 👇

```python
@tool
def check_if_project_is_approved(project_id: str) -> bool:
    """
    Check if a given Project is approved.

    A Project is considered approved if it has at least one connected node
    with node_type == "ProjectApproval" (via either incoming or outgoing edge).

    Args:
        project_id (str): The Project node identifier.

    Returns:
        bool: True if approved, else False.
    """
    return query_project_hierarchy_utils.is_project_approved(project_id)


# Add the tool to the list of available tools
PROJECT_INFORMATION_ASSISTANT_TOOLS.append(check_if_project_is_approved)


# Update SYSTEM_PROMPT to include tool description
SYSTEM_PROMPT += """

Additional available tool:
- check_if_project_is_approved: Use this tool when the user asks whether a Project has been approved or if it has any associated ProjectApproval nodes.
"""
```
