Here's a full working example of a **Streamlit chatbot app** using the **OpenAI API** that supports **multi-round conversation**:

---

### ✅ Features:

* Maintains chat history
* Allows user to send multiple messages in a conversation
* Uses OpenAI ChatCompletion endpoint (`gpt-4o`, `gpt-4`, or `gpt-3.5-turbo`)

---

### 🔧 Prerequisites:

1. Install dependencies:

```bash
pip install streamlit openai
```

2. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-key-here'  # or use st.secrets
```

---

### 🧠 `app.py` — Streamlit Chatbot

```python
import streamlit as st
import openai
import os

# Set API key (use st.secrets for production)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="OpenAI Chatbot", page_icon="🤖")
st.title("🤖 OpenAI Chatbot with Multi-round Conversation")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call OpenAI API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # or "gpt-3.5-turbo"
                    messages=st.session_state.messages,
                )
                assistant_reply = response.choices[0].message["content"]
                st.markdown(assistant_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )
            except Exception as e:
                st.error(f"OpenAI API error: {e}")
```

---

### 🧪 To Run:

```bash
streamlit run app.py
```

---

### 📝 Notes:

* You can customize the system prompt (first message) to guide the chatbot’s behavior.
* For security, prefer storing secrets via `st.secrets["OPENAI_API_KEY"]`.
* This app supports a persistent multi-turn chat during a single Streamlit session.
