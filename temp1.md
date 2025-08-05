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
