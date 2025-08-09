Got it — you want to:

1. Loop through a directory with many `.csv` files.
2. For each file:

   * Get the file name without `.csv` → `view_id`.
   * Read the file’s entire **content as a string** → `view_csv_data_content`.
3. Create **one DataFrame** with two columns: `view_id` and `view_csv_data_content`.

Here’s a Python program to do that:

```python
import os
import pandas as pd

# Path to your directory with CSV files
csv_dir = "/path/to/your/csv_folder"

# Store results here
data = []

# Loop through all files in the directory
for file_name in os.listdir(csv_dir):
    if file_name.lower().endswith(".csv"):
        view_id = os.path.splitext(file_name)[0]  # file name without .csv
        
        # Read file content as string
        file_path = os.path.join(csv_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        data.append({
            "view_id": view_id,
            "view_csv_data_content": content
        })

# Create DataFrame
df = pd.DataFrame(data)

print(df.head())
```

---

### Example output

If your folder has:

```
sales.csv
inventory.csv
```

Then `df` will look like:

| view\_id  | view\_csv\_data\_content       |
| --------- | ------------------------------ |
| sales     | "col1,col2\n1,2\n3,4\n..."     |
| inventory | "item,qty\napple,10\nbanana,5" |

---

Do you also want me to make the program **automatically save this DataFrame into PostgreSQL** after loading? That would combine your earlier request with this one.
