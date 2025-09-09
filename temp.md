Python function that:

* Takes a list of dictionaries, each containing `keyword_type` and `keyword_value`.
* Takes a mapping dictionary (e.g. `{"typeA": "mappedA"}`) to replace `keyword_type` with another string.
* Returns a new list where `keyword_type` is replaced according to the mapping.

Here’s a clean implementation:

```python
def remap_keywords(data, type_map):
    """
    Replace 'keyword_type' in a list of dicts based on a mapping.

    Args:
        data (list[dict]): List of dicts with keys 'keyword_type' and 'keyword_value'.
        type_map (dict): Mapping from old keyword_type to new string.

    Returns:
        list[dict]: New list with keyword_type replaced.
    """
    result = []
    for item in data:
        mapped_type = type_map.get(item["keyword_type"], item["keyword_type"])  # fallback to original
        result.append({
            "keyword_type": mapped_type,
            "keyword_value": item["keyword_value"]
        })
    return result


# Example usage
data = [
    {"keyword_type": "A", "keyword_value": "apple"},
    {"keyword_type": "B", "keyword_value": "banana"},
    {"keyword_type": "C", "keyword_value": "cherry"},
]

type_map = {
    "A": "FruitA",
    "B": "FruitB"
}

print(remap_keywords(data, type_map))
# Output:
# [{'keyword_type': 'FruitA', 'keyword_value': 'apple'},
#  {'keyword_type': 'FruitB', 'keyword_value': 'banana'},
#  {'keyword_type': 'C', 'keyword_value': 'cherry'}]
```

👉 This keeps unmapped types unchanged.
