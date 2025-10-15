In Jupyter notebooks, you can add a **progress bar** to a `DataFrame.apply()` operation using `tqdm`.
Here’s the clean and recommended way 👇

---

### ✅ **Option 1: Using `tqdm.pandas()` (Easiest Way)**

`tqdm` integrates directly with pandas.

```python
from tqdm.notebook import tqdm
import pandas as pd

# Enable tqdm for pandas
tqdm.pandas()

# Example DataFrame
df = pd.DataFrame({'x': range(10)})

# Define your function
def square(x):
    return x ** 2

# Apply with progress bar
df['y'] = df['x'].progress_apply(square)
```

🟢 Output:
`tqdm` will show a nice progress bar in your notebook that updates as `apply()` runs.

---

### ✅ **Option 2: Manual loop with tqdm**

If you’re doing something more complex (e.g., applying across rows, or combining multiple columns), you can manually loop with `tqdm`:

```python
from tqdm.notebook import tqdm
import pandas as pd

df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})

results = []
for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    results.append(row['a'] + row['b'])

df['sum'] = results
```

This gives you full control over progress display, retries, batching, etc.

---

### ✅ **Option 3: Parallel apply with progress (for large datasets)**

You can use `swifter` for parallelism **and** progress bars:

```bash
pip install swifter
```

Then:

```python
import swifter
import pandas as pd

df = pd.DataFrame({'x': range(10000)})

df['y'] = df['x'].swifter.progress_bar(True).apply(lambda x: x ** 2)
```

🧠 `swifter` automatically parallelizes your apply across cores and shows progress.

---

### TL;DR

| Method           | Library | Best for                        |
| ---------------- | ------- | ------------------------------- |
| `tqdm.pandas()`  | tqdm    | Simple apply functions          |
| Manual tqdm loop | tqdm    | Complex row-wise operations     |
| `swifter`        | swifter | Large datasets with parallelism |

---

Would you like me to show a version that supports **apply across rows (`axis=1`)** with a tqdm progress bar too?
