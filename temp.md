Here’s a clean, production-ready Python script that will:
✅ Load all PDF files from a given folder
✅ Extract **text from each page**
✅ Build a DataFrame with columns: `file_name`, `page_number`, `text_content`
✅ Save the combined data to a `.parquet` file

---

### 🧠 Requirements

Make sure to install the following packages:

```bash
pip install PyPDF2 pandas pyarrow
```

---

### 📄 Python Code

```python
import os
import pandas as pd
from PyPDF2 import PdfReader

# === CONFIGURATION ===
folder_path = r"C:\path\to\your\pdf_folder"   # <-- change this to your folder path
output_file = r"C:\path\to\output\pdf_texts.parquet"

# === PROCESSING ===
records = []

for file_name in os.listdir(folder_path):
    if file_name.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, file_name)
        try:
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                records.append({
                    "file_name": file_name,
                    "page_number": page_num,
                    "text_content": text.strip()
                })
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

# === SAVE TO PARQUET ===
df = pd.DataFrame(records)
df.to_parquet(output_file, engine="pyarrow", index=False)

print(f"✅ Done! Extracted {len(df)} pages from {len(os.listdir(folder_path))} PDFs.")
print(f"Saved to: {output_file}")
```

---

### 💡 Notes

* If you want to include **subfolders**, replace the loop with:

  ```python
  for root, _, files in os.walk(folder_path):
      for file_name in files:
          ...
  ```
* You can later load your `.parquet` file easily:

  ```python
  df = pd.read_parquet(r"C:\path\to\output\pdf_texts.parquet")
  ```

Would you like me to modify it to use **multithreading** for faster extraction (useful if PDFs are large)?
