Great question 👍 — I see exactly what you want:
Right now, your `chat_graph_agent.py` passes **all conversation history** to the LLM each time. You want to **truncate to the last *n* human+AI messages** (while still keeping the full history in Cosmos DB), and importantly you **don’t want tool messages to count toward the limit**.

Here’s how to do it:

---

### 🔍 Where to change

The part of the code where messages are actually **prepared and sent into the graph** is here:

```python
def set_graph_chat_state(user_wwid: str, conversation_id: str):
    message_history = graph_memory_utils.load_user_chat_history_by_id(
        user_wwid=user_wwid, conversation_id=conversation_id, for_ui=False
    )
    ...
    new_state = {
        graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY: convert_to_messages(
            message_history
        ),
        ...
    }
```

`convert_to_messages(message_history)` is converting the full history into `langchain_core.messages` format and injecting it into `_CHAT_GRAPH`.

That’s the choke point — you need to **truncate `message_history` before passing it in**.

---

### 🔧 How to change

1. Add a utility function to filter and truncate only **HumanMessage** and **AIMessage** types:

```python
from langchain_core.messages import HumanMessage, AIMessage

def _truncate_message_history(message_history, max_messages: int = 10):
    """
    Keep only the last `max_messages` human+AI messages.
    Tool messages are excluded from the count but still kept if they fall inside.
    """
    human_ai_msgs = [m for m in message_history if isinstance(m, (HumanMessage, AIMessage))]
    truncated_human_ai = human_ai_msgs[-max_messages:]  # last N human+AI
    
    # Collect tool/system messages that occur after the earliest kept human/AI
    if truncated_human_ai:
        cutoff_id = message_history.index(truncated_human_ai[0])
        truncated = message_history[cutoff_id:]
    else:
        truncated = message_history
    return truncated
```

2. Use this function in **`set_graph_chat_state`**:

```python
def set_graph_chat_state(user_wwid: str, conversation_id: str):
    message_history = graph_memory_utils.load_user_chat_history_by_id(
        user_wwid=user_wwid, conversation_id=conversation_id, for_ui=False
    )

    # Apply truncation (decide N here, e.g., 12)
    message_history = _truncate_message_history(message_history, max_messages=12)

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
    for msg in new_state[graph_memory_utils._COSMOSDB_MSG_MESSAGES_KEY]:
        del msg.additional_kwargs
    global _CHAT_GRAPH
    _CHAT_GRAPH = None
    init_graph()
    _CHAT_GRAPH.update_state(_DEFAULT_GRAPH_CONFIG, new_state)
```

---

### ✅ What this gives you

* **Context window control** → Only last `n` (say 12) Human/AI messages go into the LLM.
* **Tools excluded from count** → ToolMessages/SystemMessages don’t eat into the window.
* **Full history still saved** → `save_graph_chat_state()` still writes the entire conversation to Cosmos DB. Only truncation for LLM input, not storage.

---

👉 Next step: Do you want `n` (the context window) to be configurable via environment variable / settings (so ops can adjust it without code changes), or hardcoded in `_truncate_message_history`?
