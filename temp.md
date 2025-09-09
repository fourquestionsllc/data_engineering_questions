Got it 👍 You have a string with some extra text around it, but inside there’s a JSON-like list of dictionaries (surrounded by `[...]`). You want to extract that part and convert it into a real Python list of dictionaries.

Here’s a function:

```python
import re
import ast

def extract_dict_list(text):
    """
    Extracts the first [...] JSON-like list of dictionaries from a string
    and converts it to a Python list of dicts.

    Args:
        text (str): Input string containing a list of dictionaries.

    Returns:
        list[dict]: Parsed list of dictionaries.
    """
    # Find the first [...] block
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if not match:
        return []

    list_str = match.group(0)

    try:
        # Safely evaluate string into Python object
        return ast.literal_eval(list_str)
    except Exception as e:
        raise ValueError(f"Failed to parse dictionary list: {e}")

# Example usage
s = "Some random text before [ {'keyword_type': 'A', 'keyword_value': 'apple'}, {'keyword_type': 'B', 'keyword_value': 'banana'} ] and some text after"

result = extract_dict_list(s)
print(result)
# [{'keyword_type': 'A', 'keyword_value': 'apple'}, {'keyword_type': 'B', 'keyword_value': 'banana'}]
```

✅ This will:

* Use regex to extract the `[ ... ]` part.
* Use `ast.literal_eval` (safe) to convert it into a real Python list of dicts.

Do you expect the list inside to always be **Python-style** (`'single quotes'`) or sometimes **JSON-style** (`"double quotes"`) too?
