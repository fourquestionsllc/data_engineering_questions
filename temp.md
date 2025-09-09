Got it 👍 You have a string that looks like:

```
"some text before { 'a': 1, 'b': 2 } some text after"
```

and you want to:

1. Extract the `{ ... }` portion.
2. Convert it into a real Python dictionary.

Here’s a safe function for that:

```python
import re
import ast

def extract_dict(text):
    """
    Extract the first {...} dictionary from a string and convert it to a Python dict.

    Args:
        text (str): Input string containing a dictionary inside { }.

    Returns:
        dict: Parsed dictionary, or None if not found/invalid.
    """
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        return None
    
    dict_str = match.group(0)
    try:
        return ast.literal_eval(dict_str)
    except (SyntaxError, ValueError):
        return None


# Example usage
s = "extra text { 'x': 10, 'y': 20 } more text"
print(extract_dict(s))  # {'x': 10, 'y': 20}
```

✅ `ast.literal_eval` is safer than `eval` because it only parses literals (dicts, lists, numbers, strings).
✅ The regex `\{.*?\}` grabs the first `{...}` block (non-greedy).

Do you want this function to handle **multiple `{}` blocks** in the same string (and return a list of dicts), or always just the first one?
