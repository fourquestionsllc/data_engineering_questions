Got it — if you already have `top5_indices` from the cosine similarity calculation and a DataFrame named `view_pdf_embeddings`, you can select those rows like this:

```python
# Select rows by index
top5_rows = view_pdf_embeddings.iloc[top5_indices]

print(top5_rows)
```

If you also want to **add the cosine similarity scores** from the earlier calculation:

```python
import pandas as pd

# Make a copy to avoid modifying the original
top5_rows = view_pdf_embeddings.iloc[top5_indices].copy()

# Add similarity scores
top5_rows["cosine_similarity"] = cosine_similarities[top5_indices]

# Sort by similarity in descending order (just in case)
top5_rows = top5_rows.sort_values(by="cosine_similarity", ascending=False)

print(top5_rows)
```

This way, you keep the top 5 rows along with their similarity values.

Do you want me to combine **the similarity calculation and DataFrame selection** into one function so you can reuse it? That would make it one call.
