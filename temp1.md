To **display a PDF file in Streamlit from a file path**, the best way depends on your use case. Here are the **most practical and reliable options**:

---

### ✅ Option 1: Embed the PDF in an `st.components.v1.html` iframe

> **Best for:** Displaying the full PDF document (scrollable, zoomable, multi-page)

```python
import streamlit as st
import base64

# PDF file path
pdf_path = "example.pdf"

# Read the PDF file and encode in base64
with open(pdf_path, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

# Embed PDF in HTML
pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>
    """
st.components.v1.html(pdf_display, height=1000, scrolling=True)
```

---

### ✅ Option 2: Show PDF as images (e.g., first page as preview)

> **Best for:** Previewing one or a few pages (e.g., chatbot response)

```python
import streamlit as st
from pdf2image import convert_from_path

# Path to your PDF
pdf_path = "example.pdf"

# Convert first page to image
images = convert_from_path(pdf_path, first_page=1, last_page=1)

# Show image
st.image(images[0], caption="First page of PDF", use_column_width=True)
```

> ⚠️ **Note:** `pdf2image` needs `poppler` installed. If you're on Windows and can't install it, you can ask me for an alternative using `PyMuPDF`.

---

### ✅ Option 3: Provide a download button

> Good to pair with either of the above

```python
with open("example.pdf", "rb") as f:
    st.download_button("Download PDF", f, file_name="example.pdf")
```

---

Let me know your target use case (e.g., preview in chatbot, multi-page viewer, annotation), and I can suggest the ideal setup.
