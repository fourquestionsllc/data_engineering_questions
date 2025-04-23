Here's a Python function that implements the two-step keyword matching logic using:

1. **Fuzzy matching** to filter top similar keywords.
2. **Edit distance** to finalize the selection based on a threshold.

We'll use `fuzzywuzzy` for similarity scoring and `Levenshtein` for edit distance:

### 🔧 Required packages:
Install them via pip:
```bash
pip install fuzzywuzzy python-Levenshtein
```

### ✅ Function Code:
```python
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def match_keyword(extracted_keyword, keyword_list, top_n=5):
    # Step 1: Fuzzy match to get top N similar keywords
    top_matches = process.extract(extracted_keyword, keyword_list, scorer=fuzz.ratio, limit=top_n)
    
    # Step 2: Select keyword based on edit distance threshold
    for match, score in top_matches:
        distance = Levenshtein.distance(extracted_keyword.lower(), match.lower())
        if distance / max(1, len(extracted_keyword)) <= 1/3:
            return match
    
    return None  # No match passed the edit distance check
```

### 🧪 Example usage:
```python
extracted = "reciept"
available_keywords = ["receipt", "invoice", "bill", "payment", "statement"]

result = match_keyword(extracted, available_keywords)
print("Matched keyword:", result)
```

Let me know if you'd like to match multiple extracted keywords or hook it up to your SQL database!
