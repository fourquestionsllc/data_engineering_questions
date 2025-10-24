Perfect — that’s a clean way to test your **Knowledge Assistant** in batch mode, without Streamlit.

Below is a ready-to-use Python function that takes a list of user queries, runs them sequentially through your assistant (`chat_graph_agent`), and returns a full list of message dicts containing `"role"` and `"content"` — including both the human and AI messages in chronological order.

---

### ✅ **Function: `run_chat_sequence`**

```python
from skybound_knowledge_assistant import chat_graph_agent, graph_memory_utils

def run_chat_sequence(user_queries: list[str], user_id: str = "KA-DEVS-DEFAULT-USER"):
    """
    Test a sequence of user queries with the Knowledge Assistant and return the full chat history.
    
    Args:
        user_queries (list[str]): List of user messages to send in order.
        user_id (str): Optional user ID (default = KA-DEVS-DEFAULT-USER).

    Returns:
        list[dict]: Ordered list of messages including both user and assistant responses.
                    Each element looks like {"role": "human"|"ai", "content": "message text"}.
    """

    # Initialize graph and start a new conversation
    chat_graph_agent.init_graph()
    new_convo = graph_memory_utils.create_new_user_chat(user_wwid=user_id)
    conversation_id = new_convo.conversation_id

    # Store full conversation history locally
    conversation_log = []

    for user_input in user_queries:
        # Add human message
        conversation_log.append({"role": "human", "content": user_input})

        # Get assistant response
        ai_response = chat_graph_agent.get_response(user_input=user_input)

        # Add AI message
        conversation_log.append({"role": "ai", "content": ai_response.content})

        # (Optional) Print each round
        print(f"\n👤 User: {user_input}\n🤖 Assistant: {ai_response.content}\n")

    # Save the conversation to memory graph (optional)
    graph_memory_utils.save_user_chat_history_by_id(
        user_wwid=user_id,
        conversation_id=conversation_id,
        messages=[
            type("Msg", (), msg) for msg in conversation_log  # mock objects if needed
        ],
    )

    return conversation_log
```

---

### 💡 **Example Usage**

```python
queries = [
    "Show me all projects updated last week.",
    "Filter only those related to documentation.",
    "Give me their owners and deadlines.",
]

history = run_chat_sequence(queries)

for msg in history:
    print(f"{msg['role'].upper()}: {msg['content']}")
```

---

### 🧠 **What This Function Does**

1. Initializes your assistant’s LangGraph (`init_graph()`).
2. Creates a fresh conversation via `graph_memory_utils.create_new_user_chat()`.
3. Iterates over each human query:

   * Logs the human message.
   * Calls `chat_graph_agent.get_response()` for the AI reply.
   * Logs the AI’s response.
4. Optionally saves the conversation to the persistent memory graph.
5. Returns the full chat log as a Python list.

---

Would you like me to modify it so it can also use the **endpoint version** (Feature or Dev API) instead of local `chat_graph_agent.get_response()`?
