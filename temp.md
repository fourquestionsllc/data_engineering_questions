Got it ✅ — you want to:

* Run something like `b = query_engine.documents_content_entity_extraction(b)` where both `a` and `b` are pandas DataFrames.
* Show a **progress bar** in Jupyter Notebook.
* **Disable INFO-level log messages** during the process.

Here’s how you can do it cleanly 👇

---

### ✅ **Option 1: Wrap the operation in a progress bar loop**

If `query_engine.documents_content_entity_extraction()` processes rows of `b`, you can iterate row by row and show progress:

```python
from tqdm.notebook import tqdm
import logging

# Disable INFO logs
logging.getLogger().setLevel(logging.WARNING)

# Apply with progress bar
results = []
for _, row in tqdm(b.iterrows(), total=len(b), desc="Extracting entities"):
    result = query_engine.documents_content_entity_extraction(row)
    results.append(result)

b = pd.DataFrame(results)
```

---

### ✅ **Option 2: If the function processes the whole DataFrame once**

If your `query_engine.documents_content_entity_extraction(b)` runs once on the full DataFrame (not per-row),
you can use `tqdm` just for **visual feedback** during long processing:

```python
from tqdm.notebook import tqdm
import time
import logging

# Disable INFO logs globally
logging.getLogger().setLevel(logging.WARNING)

# Show pseudo progress while waiting
with tqdm(total=100, desc="Processing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    for i in range(10):
        time.sleep(0.1)  # simulate progress
        pbar.update(10)
    
b = query_engine.documents_content_entity_extraction(b)
```

This gives a smooth visual progress even if the function itself is a single call.

---

### ✅ **Option 3: Patch tqdm inside the query_engine**

If you can modify or wrap `query_engine.documents_content_entity_extraction`, you can decorate it like this:

```python
from tqdm.notebook import tqdm
import logging

logging.getLogger().setLevel(logging.WARNING)

def extract_with_progress(df):
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Extracting entities"):
        results.append(query_engine.documents_content_entity_extraction(row))
    return pd.DataFrame(results)

b = extract_with_progress(b)
```

---

### ✅ Bonus: if `query_engine` uses Python’s `logging` module internally

You can disable its own logger too:

```python
import logging

logging.getLogger('query_engine').setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)
```

---

Would you like me to detect automatically whether `documents_content_entity_extraction` supports batch (whole DataFrame) or row-wise processing and wrap it accordingly?
I can give you a smart wrapper that auto-selects the right progress style.
