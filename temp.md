Excellent question — this `streamlit_app.py` is a *UI entrypoint* for your **Knowledge Assistant (KA)** built on top of LangGraph and the `skybound_knowledge_assistant` module.

Let’s unpack **how messages flow** in this system step-by-step, and how you can **bypass Streamlit** to directly test the assistant with your own message inputs using the underlying functions (`chat_graph_agent`, `graph_memory_utils`, and `ka_main`).

---

## 🧩 Step-by-step Message Flow

Here’s the full lifecycle when a user chats for the first time and continues a conversation.

---

### **1️⃣ Initial Setup**

When `knowledge_assistant_page()` runs:

* The app calls `chat_graph_agent.init_graph()`
  → This initializes the LangGraph workflow used to orchestrate the assistant (tools, memory, etc).

* Then Streamlit checks session variables:

  ```python
  st.session_state.messages = []  # if first time
  st.session_state.conversation_id = None
  ```

So, the system starts with an *empty* conversation.

---

### **2️⃣ User sends the first message**

When a user enters something in the chat input:

```python
user_input = st.chat_input("Enter your message")
```

→ The message is added to `st.session_state.messages`:

```python
st.session_state.messages.append({"type": "human", "content": user_input})
st.session_state.messages.append({"type": "typing", "content": ""})
```

→ Then `st.session_state.awaiting_response = True`, and the app reruns.

---

### **3️⃣ Assistant processes the message**

On the next rerun, since:

```python
if st.session_state.awaiting_response:
```

the app enters the “response processing” phase.

Then it:

1. Removes the `"typing"` message.

2. Finds the last `"human"` message (`last_user_message`).

3. Chooses whether to run **locally** or call the **feature/dev endpoint**:

   * **Local** → `chat_graph_agent.get_response(user_input=last_user_message)`
   * **Remote** → `requests.post()` to `/ka/message` endpoint.

4. The local function returns an `AIResponse` object:

   ```python
   ai_response = chat_graph_agent.get_response(user_input=last_user_message)
   ```

   containing:

   ```python
   ai_response.content  # text reply from the assistant
   ai_response.tools    # tools triggered (if any)
   ai_response.memory   # graph/memory updates
   ```

5. This response is appended to session state:

   ```python
   st.session_state.messages.append({"type": "ai", "content": ai_response.content})
   ```

Then Streamlit reruns to display it.

---

### **4️⃣ History persistence**

The functions from `graph_memory_utils` are responsible for **storing, loading, and deleting** conversation history in your knowledge graph database.

Key functions:

* `create_new_user_chat(user_wwid)` → starts a new conversation and returns a conversation_id.
* `load_user_chat_history_by_id(user_wwid, conversation_id, for_ui=False)` → loads all historical messages.
* `save_user_chat_history_by_id(...)` → saves a list of messages (used for rollback, etc.)
* `get_user_conversations(user_wwid)` → lists past conversation IDs for dropdown.

So the messages from both user and assistant are **stored in the graph memory** and can be reloaded later.

---

## 🧠 Summary of Data Flow

| Step     | Function                                            | Purpose                        |
| -------- | --------------------------------------------------- | ------------------------------ |
| Init     | `chat_graph_agent.init_graph()`                     | Builds the LangGraph agent     |
| New Chat | `graph_memory_utils.create_new_user_chat()`         | Creates new conversation_id    |
| Send Msg | `chat_graph_agent.get_response(user_input=...)`     | Runs the LLM + tools + graph   |
| Save     | `graph_memory_utils.save_user_chat_history_by_id()` | Persists conversation messages |
| Load     | `graph_memory_utils.load_user_chat_history_by_id()` | Fetches prior history          |

---

## 💻 How to Call These Functions Yourself (without Streamlit)

You can replicate the exact chat cycle from a Python shell or notebook:

```python
from skybound_knowledge_assistant import chat_graph_agent, graph_memory_utils, main as ka_main

# 1. Initialize the graph (must do once)
chat_graph_agent.init_graph()

# 2. Create a new conversation
user_id = "KA-DEVS-DEFAULT-USER"
new_convo = graph_memory_utils.create_new_user_chat(user_wwid=user_id)
conversation_id = new_convo.conversation_id

# 3. Send first human message
user_input = "Show me all projects updated last week."
ai_response = chat_graph_agent.get_response(user_input=user_input)

print("AI:", ai_response.content)
```

---

### To Continue the Conversation

Each new message uses the **same conversation_id**, which the graph tracks internally.

```python
# Continue with another user message
next_user_input = "Filter only those with incomplete documentation."
ai_response = chat_graph_agent.get_response(user_input=next_user_input)

print("AI:", ai_response.content)
```

If your system is using persistent memory (through `graph_memory_utils`), the conversation context will automatically be maintained between messages.

---

### To Load Historical Messages

```python
history = graph_memory_utils.load_user_chat_history_by_id(
    user_wwid=user_id,
    conversation_id=conversation_id,
    for_ui=True
)

for msg in history.messages:
    print(msg.type, ":", msg.content)
```

---

### To Delete or Roll Back a Conversation

```python
graph_memory_utils.delete_user_chat_history_by_id(
    user_wwid=user_id,
    conversation_id=conversation_id,
)
```

or rollback:

```python
current_convo_raw = graph_memory_utils.load_user_chat_history_by_id(
    user_wwid=user_id,
    conversation_id=conversation_id,
    for_ui=False,
)
truncated_msgs = current_convo_raw.messages[:-2]
graph_memory_utils.save_user_chat_history_by_id(
    user_wwid=user_id,
    conversation_id=conversation_id,
    messages=truncated_msgs,
)
```

---

## 🧪 Testing Summary

If your goal is to test the assistant without Streamlit:

1. Call `chat_graph_agent.init_graph()`.
2. Create or pick a `conversation_id`.
3. Call `chat_graph_agent.get_response(user_input="...")` repeatedly with your text.
4. Optionally manage conversation state with `graph_memory_utils`.

---

Would you like me to give you a **ready-to-run Python test script** that simulates a full conversation (human → AI → human → AI) using these functions directly?
