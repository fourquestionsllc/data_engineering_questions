Sure! We can write a small test script using **dummy `HumanMessage`, `AIMessage`, and `ToolMessage`** objects to simulate a conversation and test `_truncate_message_history`.

Here’s a complete example:

```python
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Import your truncate function
# from chat_graph_agent import _truncate_message_history

def test_truncate_message_history():
    # Create a simulated conversation
    message_history = [
        HumanMessage(content="Hi"),
        AIMessage(content="Hello! How can I help?"),
        ToolMessage(content="Running tool 1"),
        HumanMessage(content="Tell me about project X"),
        AIMessage(content="Project X is in phase 2"),
        ToolMessage(content="Tool 2 result"),
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

### ✅ What this does

1. Original history contains **Human, AI, and Tool messages**.
2. `_truncate_message_history` keeps only **last 4 Human/AI messages** but also preserves **Tool messages** that occur after the earliest kept Human/AI message.
3. Prints messages **before and after truncation** so you can visually verify it works correctly.

---

If you want, I can also **write a version using `pytest`** that asserts the truncated history contains the right messages and right count automatically.

Do you want me to do that?
