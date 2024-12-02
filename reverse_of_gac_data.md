To define the **GAC date** (`gac_dt`) from the output of the `agg_po_and_filter_products` function, we need to reverse-engineer the `arr_wk` and `start_dt` fields to map back to the original calendar dates. Here's a step-by-step solution:

---

### **Proposed Solution**
1. **Understand Available Information**:
   - `arr_wk`: A list of indices representing the weeks in the simulation period where purchase orders occur.
   - `start_dt`: The earliest observed week date in the simulation period.
   - `n_per`: The total number of weeks in the simulation period.
   - The offset logic (e.g., 13-week lead time) used to compute `arr_wk`.

2. **Define the Reverse Mapping**:
   - Each index in `arr_wk` corresponds to a specific calendar week. To compute the GAC date:
     - Use the formula:
       \[
       \text{gac\_dt} = \text{start\_dt} + (\text{arr\_wk} - 13) \times 7 \, \text{days}
       \]
     - The subtraction of 13 accounts for the hardcoded lead time added during the calculation of `arr_wk`.

3. **Integrate into a New Column**:
   - Add a new column, `gac_dates`, to store the computed GAC dates for each row.
   - This column can be populated using a lambda function that applies the formula for each row.

---

### **Implementation Example**
Here’s how to implement this logic in Python:

```python
import pandas as pd

# Add a new column to compute GAC dates for each product and size combination
ep_po = ep_po.assign(
    gac_dates=lambda df: df.apply(
        lambda row: [row["start_dt"] + pd.Timedelta(days=(wk - 13) * 7) for wk in row["po_qty"].nonzero()[0]],
        axis=1
    )
)
```

---

### **Explanation of Code**
- **`row["start_dt"]`**: The starting date of the simulation period for the product/size.
- **`wk - 13`**: Adjusts the week index back to the GAC calendar date using the lead time.
- **`* 7`**: Converts weeks to days.
- **`row["po_qty"].nonzero()[0]`**: Identifies indices in the `po_qty` array with non-zero quantities, corresponding to arrival weeks.

---

### **Output**
The new column, `gac_dates`, will contain a list of GAC dates corresponding to the purchase orders in the `po_qty` array.

For example:
- If `start_dt = "2024-01-01"`, `arr_wk = [14, 16]`, and `n_per = 20`:
  - GAC dates are:
    - \( \text{start\_dt} + (14 - 13) \times 7 = "2024-01-08" \)
    - \( \text{start\_dt} + (16 - 13) \times 7 = "2024-01-22" \)
- Result: `gac_dates = ["2024-01-08", "2024-01-22"]`.

---

### **Summary**
The GAC dates can be derived from `arr_wk` and `start_dt` using a reverse mapping that accounts for the lead time and week-to-date conversion. The proposed solution computes this efficiently and integrates the results into the output DataFrame.
