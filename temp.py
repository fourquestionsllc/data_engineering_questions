import pandas as pd

# Step 1: Keep only the row with the maximum score for each (keyword, doc) pair
df_max = df.sort_values('score', ascending=False).drop_duplicates(subset=['keyword', 'doc'])

# Step 2: Group by doc and aggregate keywords and sum scores
result = df_max.groupby('doc').agg({
    'keyword': lambda x: list(x),   # aggregate keywords into a list
    'score': 'sum'                  # sum of scores
}).reset_index()

# Step 3: Sort by sum of scores in descending order
result = result.sort_values('score', ascending=False).reset_index(drop=True)

# Rename columns if desired
result.columns = ['doc', 'keywords', 'total_score']

print(result)
