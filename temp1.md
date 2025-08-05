To **extract text and tables from a PDF file in Python**, you can use different tools depending on your needs:

---

## ✅ 1. Extract Text: Use `PyMuPDF` (aka `fitz`) — Fast & Simple

```python
import fitz  # PyMuPDF

doc = fitz.open("example.pdf")
for page in doc:
    text = page.get_text()
    print(text)  # or store/save it
```

> This works for most PDFs, including scanned if OCR text is embedded.
> For scanned image PDFs with no embedded text, use OCR tools like `pytesseract`.

---

## ✅ 2. Extract Tables: Use `pdfplumber` — Best for native PDFs with tables

```python
import pdfplumber

with pdfplumber.open("example.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)  # or convert to DataFrame
```

> You can also convert `table` to a Pandas DataFrame easily:

```python
import pandas as pd
df = pd.DataFrame(table)
print(df)
```

---

## ✅ 3. Combine Text + Table Extraction with `pdfplumber`

```python
import pdfplumber

with pdfplumber.open("example.pdf") as pdf:
    for page in pdf.pages:
        print("--- Text ---")
        print(page.extract_text())

        print("--- Tables ---")
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

---

## ✅ 4. Bonus: OCR (if PDF is scanned) with `pytesseract`

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path("scanned.pdf")
for img in images:
    text = pytesseract.image_to_string(img)
    print(text)
```

> You’ll need to install [Tesseract OCR engine](https://github.com/tesseract-ocr/tesseract) and `pdf2image`.

---

### 📦 Installation Summary

```bash
pip install pymupdf pdfplumber pytesseract pdf2image
```

> And for OCR:

* Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (make sure it's in PATH)

---

Let me know the **type of PDF (native or scanned)** and your **output goal (plain text, structured table, dataframe)** — I can tailor the code for that.



To **make the sidebar in Streamlit wider than the default**, you can use **custom CSS** via `st.markdown()` with the `unsafe_allow_html=True` flag.

---

### ✅ Example: Set a Wider Sidebar

```python
import streamlit as st

# Custom CSS to widen the sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 400px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
st.sidebar.title("Custom Wide Sidebar")
st.sidebar.write("This sidebar is wider than the default.")
```

---

### 📝 Notes:

* Adjust `400px` to your desired width.
* The two selectors are needed to target both the collapsed and expanded sidebar.
* Works well with recent Streamlit versions (1.11+).

---

Let me know if you want a **responsive** width (e.g. \`% of screen size) or only for large displays!



Creating a **chatbot in Streamlit** is very doable using a combination of `st.chat_input` (for user input), `st.chat_message` (for displaying messages), and a language model like **OpenAI**, **LLamaIndex**, or even a simple rule-based bot.

---

### ✅ Minimal Working Chatbot Example (Using OpenAI)

```python
import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "your-api-key"

st.title("💬 Chatbot Example")
st.caption("Built with Streamlit + OpenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
if prompt := st.chat_input("Say something..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content

    # Show assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
```

---

### 🧠 No OpenAI Key? Use a Dummy Response

```python
reply = "You said: " + prompt
```

---

### 🛠 Install Required Packages

```bash
pip install streamlit openai
```

---

### ✅ Advanced Options

* Use **LangChain** or **LlamaIndex** for RAG-based chatbots.
* Add **file upload** and document-based QA.
* Track chat **state**, logs, or memory.
* Add **Streamlit sidebar** for chatbot config.

---

Let me know if you want:

* A **PDF/document-based** chatbot
* A chatbot with **memory** or **agent tools**
* To use **LLMs locally** (e.g., Llama, Mistral)
  I can tailor the code for your case.
