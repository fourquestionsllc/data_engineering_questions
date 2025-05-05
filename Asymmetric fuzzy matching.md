To perform **asymmetric fuzzy matching** — where you want to check if a **keyword is (approximately) contained within a document**, but **not the other way around** — the cleanest way is to use a **sliding window search** of the keyword against substrings of the document.

Here’s how you can **enforce true one-directional fuzzy containment**, using `RapidFuzz`'s `process.extract` or `fuzz.ratio` over sliding substrings of the document.

---

### ✅ Method: Fuzzy substring search (sliding window)

```python
from rapidfuzz.fuzz import ratio

def fuzzy_substring_match(keyword, document, threshold=90):
    keyword = keyword.lower()
    document = document.lower()

    k_len = len(keyword)
    max_score = 0

    # Slide over the document with a window the size of the keyword
    for i in range(0, len(document) - k_len + 1):
        window = document[i:i + k_len]
        score = ratio(keyword, window)
        if score > max_score:
            max_score = score
            if max_score >= threshold:
                return True  # early exit

    return False
```

---

### 💡 Why this is *truly* asymmetric:

* You're only comparing the `keyword` to substrings of the `document` (never the document to the keyword).
* This avoids the default behavior of `fuzz.partial_ratio`, which is symmetric (chooses the shorter string and finds best match in longer one).

---

### 🧪 Example:

```python
doc = "This is a document about optimiation techniques."
keyword = "optimization"

print(fuzzy_substring_match(keyword, doc, threshold=85))  # True, due to typo tolerance
```

---
