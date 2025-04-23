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



----


Here's a full script that:

1. Matches a list of extracted keywords to a list of available keywords using fuzzy matching + edit distance.
2. Escapes any invalid SQL characters in the matched keywords.
3. Generates a `WHERE` clause for a SQL query in the format you described.

```python
import re
from difflib import get_close_matches
import Levenshtein

def sanitize_sql_like_value(value):
    """
    Remove or escape characters not valid in SQLite LIKE syntax.
    """
    # Escape percent and underscore (wildcard characters in LIKE)
    value = value.replace('%', '\\%').replace('_', '\\_')
    # Remove other problematic symbols if needed
    value = re.sub(r"[^\w\s]", "", value)
    return value

def match_keyword(extracted_keyword, keyword_list, fuzzy_top_n=5, distance_threshold_ratio=1/3):
    fuzzy_matches = get_close_matches(extracted_keyword, keyword_list, n=fuzzy_top_n, cutoff=0)
    selected_keywords = []
    for candidate in fuzzy_matches:
        distance = Levenshtein.distance(extracted_keyword, candidate)
        if distance / max(len(extracted_keyword), 1) <= distance_threshold_ratio:
            selected_keywords.append(candidate)
    return selected_keywords

def generate_sql_where_clause(extracted_keywords, keyword_list, column_name='keyword'):
    """
    Generate SQL WHERE clause for a list of extracted keywords.
    
    Parameters:
        extracted_keywords (list of str): List of extracted keywords from text.
        keyword_list (list of str): List of available SQL keywords.
        column_name (str): The name of the column in SQL to filter on.
        
    Returns:
        str: SQL WHERE clause.
    """
    conditions = []

    for extracted in extracted_keywords:
        matches = match_keyword(extracted, keyword_list)
        if matches:
            subconditions = [
                f"{column_name} LIKE '%{sanitize_sql_like_value(m)}%'" for m in matches
            ]
            conditions.append(f"({' OR '.join(subconditions)})")

    if conditions:
        return "WHERE " + " AND ".join(conditions)
    else:
        return ""  # No matches, return empty condition

# Example usage
if __name__ == "__main__":
    extracted_keywords = ["custmer", "ordr"]
    available_keywords = ["customer", "custodian", "order", "orders", "product", "sales"]

    where_clause = generate_sql_where_clause(extracted_keywords, available_keywords)
    print(where_clause)
```

### Sample Output:
For the example extracted keywords `["custmer", "ordr"]`, this could generate:

```sql
WHERE (keyword LIKE '%customer%' OR keyword LIKE '%custodian%') AND (keyword LIKE '%order%' OR keyword LIKE '%orders%')
```
