import pandas as pd

# Step 1: Select the row with the max score for each (keyword, doc) pair
df_max = df.sort_values('score', ascending=False).drop_duplicates(subset=['keyword', 'doc'])

# Step 2: Group by doc, aggregate keywords as list, and sum the scores
df_result = df_max.groupby('doc').agg({
    'keyword': list,        # collect keywords
    'score': 'sum'          # sum of scores
}).reset_index()

# Optional: rename columns
df_result.rename(columns={'keyword': 'keywords', 'score': 'total_score'}, inplace=True)

print(df_result)
