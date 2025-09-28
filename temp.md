Great question — I see exactly what you’re trying to do. Right now your pipeline **always loads and passes the full history into `_CHAT_GRAPH`** via `set_graph_chat_state`, and that means every past `HumanMessage`, `AIMessage`, `ToolMessage`, etc. goes into the LLM context.

You want to keep full history in CosmosDB but **truncate to the last N human/AI messages** before each LLM call. Tool messages should not be counted, and truncation should only happen when the user initiates a new turn.

Here’s where and how to change things:

---

### **Where to change**

1. **`set_graph_chat_state` in `chat_graph_agent.py`**
   This is where you load message history (`message_history = graph_memory_utils.load_user_chat_history_by_id(...)`) and convert it to `convert_to_messages(message_history)`. Right now it takes *all* past messages.
   👉 This is the place to truncate.

2. Optionally, also review **`stream_graph_updates`** — but since that just streams from `_CHAT_GRAPH` once input is given, you don’t want to truncate here. You want truncation *before* the LLM gets state (i.e., in `set_graph_chat_state`).

---

### **How to change**

* Implement a helper function, e.g. `_truncate_messages`, that:

  * Filters to only `HumanMessage` and `AIMessage`
  * Keeps the last **N** of them (say `N=10` for 5 human + 5 ai, but configurable)
  * Leaves all other message types untouched
* Apply this truncation inside `set_graph_chat_state`, **after** you’ve loaded from Cosmos and converted to messages.

---

### **Code change**

In **`chat_graph_agent.py`**, add this helper:

```python
def _truncate_messages(messages, max_messages: int = 10):
    """Keep only the last `max_messages` Human/AI messages, 
    but retain all Tool/System messages.
    """
    # Separate human/ai from tool/system
    human_ai_msgs = [m for m in messages if isinstance(m, (HumanMessage, AIMessage))]
    tool_sys_msgs = [m for m in messages if not isinstance(m, (HumanMessage, AIMessage))]

    # Take only last N human/ai
    truncated_human_ai = human_ai_msgs[-max_messages:]

    # Recombine (keep chronological order)
    truncated = []
    idx = 0
    for m in messages:
        if isinstance(m, (HumanMessage, AIMessage)):
            if m in truncated_human_ai:
                truncated.append(m)
                # mark so we don't duplicate if multiple references
                truncated_human_ai.remove(m)
        else:
            truncated.append(m)

    return truncated
```

Then update **`set_graph_chat_state`**:

```python
def set_graph_chat_state(user_wwid: str, conversation_id: str):
    """Set the graph state based on convo history."""
    message_history = graph_memory_utils.load_user_chat_history_by_id(
        user_wwid=user_wwid, conversation_id=conversation_id, for_ui=False
    )
    graph_state = graph_memory_utils.load_graph_state_by_convo_id(
        convo_id=conversation_id
    )
    new_state = {
        graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY: convert_to_messages(
            message_history
        ),
        graph_memory_utils._COSMOSDB_MSG_USER_WWID_KEY: user_wwid,
        graph_memory_utils._COSMOSDB_MSG_CONVO_ID_KEY: conversation_id,
        _DIALOG_STATE_KEY: AssistantNames.primary_assistant.value,
    }

    # ✅ Truncate here
    msgs = new_state[graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY]
    new_state[graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY] = _truncate_messages(
        msgs, max_messages=12   # pick a number between 4–20
    )

    for msg in new_state[graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY]:
        del msg.additional_kwargs

    global _CHAT_GRAPH
    _CHAT_GRAPH = None
    init_graph()
    _CHAT_GRAPH.update_state(_DEFAULT_GRAPH_CONFIG, new_state)
```

---

### ✅ What this achieves

* Only last **N human+AI** messages are sent to the LLM each turn
* Tool/system messages still flow as needed (not counted in truncation)
* Full chat history is still stored in CosmosDB (`save_graph_chat_state` remains unchanged)
* No more ballooning context window or wasted tokens

---

Do you want me to also update the truncation logic so that the limit is **per role** (e.g., last 5 human + last 5 AI), instead of total N combined?
