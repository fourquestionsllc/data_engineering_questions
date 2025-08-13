You can do this with **NumPy** and **cosine similarity** from vector normalization.
Here’s an example:

```python
import numpy as np

# Example arrays
query_vec = np.random.rand(1, 768)          # shape (1, 768)
embeddings = np.random.rand(204, 768)       # shape (204, 768)

# Normalize vectors for cosine similarity
query_norm = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# Compute cosine similarities
cosine_similarities = np.dot(embeddings_norm, query_norm.T).ravel()

# Get top 5 indices sorted by similarity (highest first)
top5_indices = np.argsort(cosine_similarities)[-5:][::-1]

print("Top 5 indices:", top5_indices)
print("Top 5 similarities:", cosine_similarities[top5_indices])
```

### How it works:

1. **Normalize** both the query and the dataset embeddings so that dot product = cosine similarity.
2. **Matrix multiply** (`np.dot`) to get similarities in one shot.
3. **`np.argsort`** gives sorted indices; we take last 5 and reverse to get descending order.

If your embeddings are large, this method is vectorized and **very fast**—no loops needed.

Do you want me to also make it **return both indices and their similarity scores as a sorted DataFrame**? That would make it easier to inspect.
