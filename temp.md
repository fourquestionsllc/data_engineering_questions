Ah — that error is coming from **`ToolMessage` creation**. In `langchain_core.messages.ToolMessage`, the **`tool_call_id` field is required**, so you **cannot create a ToolMessage without it**.

In your test code, we just did:

```python
ToolMessage(content="Running tool 1")
```

…which is missing the required `tool_call_id`.

---

### ✅ Fix

Just add a dummy `tool_call_id` when creating test ToolMessages:

```python
ToolMessage(content="Running tool 1", tool_call_id="tool_1")
ToolMessage(content="Tool 2 result", tool_call_id="tool_2")
```

---

### Updated Test Case

```python
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# from chat_graph_agent import _truncate_message_history

def test_truncate_message_history():
    # Create a simulated conversation
    message_history = [
        HumanMessage(content="Hi"),
        AIMessage(content="Hello! How can I help?"),
        ToolMessage(content="Running tool 1", tool_call_id="tool_1"),
        HumanMessage(content="Tell me about project X"),
        AIMessage(content="Project X is in phase 2"),
        ToolMessage(content="Tool 2 result", tool_call_id="tool_2"),
        HumanMessage(content="Any updates on project Y?"),
        AIMessage(content="Project Y is scheduled for Q4"),
        HumanMessage(content="Thanks"),
    ]

    print("Original Messages:")
    for i, m in enumerate(message_history):
        print(f"{i}: {type(m).__name__} - {m.content}")

    # Truncate to last 4 human+AI messages
    truncated = _truncate_message_history(message_history, max_messages=4)

    print("\nTruncated Messages:")
    for i, m in enumerate(truncated):
        print(f"{i}: {type(m).__name__} - {m.content}")


if __name__ == "__main__":
    test_truncate_message_history()
```

---

✅ Key point: **Every `ToolMessage` must have `tool_call_id`** or Pydantic will raise `ValidationError`.

---

If you want, I can also **update `_truncate_message_history` to handle a mixed list safely**, so it won’t crash even if some messages are missing `tool_call_id` (useful for testing).

Do you want me to do that?
