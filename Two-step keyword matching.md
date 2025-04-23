Here's a Python function that matches an extracted keyword to a list of available keywords from an SQL database using fuzzy matching followed by edit distance filtering:

```python
from difflib import get_close_matches
import Levenshtein

def match_keyword(extracted_keyword, keyword_list, fuzzy_top_n=5, distance_threshold_ratio=1/3):
    """
    Match an extracted keyword to the closest ones in the keyword list.
    
    Parameters:
        extracted_keyword (str): The keyword extracted from text.
        keyword_list (list of str): The list of available keywords from the SQL database.
        fuzzy_top_n (int): Number of top fuzzy matches to consider.
        distance_threshold_ratio (float): Max edit distance allowed as a fraction of keyword length.

    Returns:
        list of str: Selected matching keywords.
    """
    # Step 1: Use fuzzy matching to get top candidates
    fuzzy_matches = get_close_matches(extracted_keyword, keyword_list, n=fuzzy_top_n, cutoff=0)

    # Step 2: Filter using edit distance
    selected_keywords = []
    for candidate in fuzzy_matches:
        distance = Levenshtein.distance(extracted_keyword, candidate)
        if distance / max(len(extracted_keyword), 1) <= distance_threshold_ratio:
            selected_keywords.append(candidate)

    return selected_keywords

# Example usage
if __name__ == "__main__":
    extracted = "custmer"
    keywords = ["customer", "order", "product", "sales", "custodian"]
    matches = match_keyword(extracted, keywords)
    print("Matched Keywords:", matches)
```

### Notes:
- This function uses `difflib.get_close_matches` for fuzzy matching.
- Then it filters those matches based on edit distance from the `python-Levenshtein` package.
- Make sure to install the required library: `pip install python-Levenshtein`.

Let me know if you want a version without third-party libraries or tuned for large datasets.
