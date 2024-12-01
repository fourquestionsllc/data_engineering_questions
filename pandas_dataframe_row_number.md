You can use the Pandas library to count the number of rows and unique values in a column of a DataFrame. Here's how you can do it:

```python
import pandas as pd

# Sample DataFrame
data = {'Column1': [1, 2, 3, 4, 2, 3, 4, 4]}
df = pd.DataFrame(data)

# Count the number of rows in the DataFrame
num_rows = len(df)

# Count the number of unique values in a specific column
unique_values_count = df['Column1'].nunique()

print("Number of rows:", num_rows)
print("Number of unique values in 'Column1':", unique_values_count)
```

### Explanation:
1. **`len(df)`**: Returns the total number of rows in the DataFrame.
2. **`df['Column1'].nunique()`**: Returns the count of unique values in the specified column. This ignores `NaN` values by default.

If you want to include `NaN` values in the unique count, you can pass the `dropna=False` argument to `nunique`:
```python
unique_values_count_with_nan = df['Column1'].nunique(dropna=False)
```
