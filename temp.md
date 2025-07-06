To visualize the project hierarchy as a **tree structure** using the dataframe you provided (with columns like `PROJECT_NAME`, `PROJECT_LUID`, and `PARENT_PROJECT_LUID`), we can use **Plotly's Treemap** in **Streamlit** for a rich interactive frontend.

---

### ✅ **Step-by-step Python Code Using Plotly + Streamlit**

```python
import pandas as pd
import plotly.express as px
import streamlit as st

# Sample data (replace with your actual df from pd.read_sql or CSV)
data = [
    {"PROJECT_NAME": "TacticalPublic Dashboard", "PROJECT_LUID": "0b1e4d15", "PARENT_PROJECT_LUID": "765b7fff"},
    {"PROJECT_NAME": "TacticalDatasources", "PROJECT_LUID": "b2229a3e", "PARENT_PROJECT_LUID": "765b7fff"},
    {"PROJECT_NAME": "Datasources", "PROJECT_LUID": "8c2a4963", "PARENT_PROJECT_LUID": "9aeaa8f9"},
    {"PROJECT_NAME": "Public Dashboard", "PROJECT_LUID": "c50b7ea7", "PARENT_PROJECT_LUID": "9aeaa8f9"},
    {"PROJECT_NAME": "O&T", "PROJECT_LUID": "7e8b3872", "PARENT_PROJECT_LUID": "765b7fff"},
    {"PROJECT_NAME": "Adhoc", "PROJECT_LUID": "c585fcb4", "PARENT_PROJECT_LUID": "9aeaa8f9"},
]

df = pd.DataFrame(data)

# Create a mapping from PROJECT_LUID to PROJECT_NAME for parent names
luid_to_name = df.set_index("PROJECT_LUID")["PROJECT_NAME"].to_dict()
df["PARENT_NAME"] = df["PARENT_PROJECT_LUID"].map(luid_to_name)
df["PARENT_NAME"] = df["PARENT_NAME"].fillna("ROOT")

# Plotly Treemap
fig = px.treemap(
    df,
    path=["PARENT_NAME", "PROJECT_NAME"],
    values=[1]*len(df),  # dummy value
    title="Tableau Project Hierarchy Tree",
)

# Streamlit App
st.set_page_config(layout="wide")
st.title("Tableau Project Tree Structure")
st.plotly_chart(fig, use_container_width=True)
```

---

### 🔁 How to Use with Your Data

If you're reading from SQL like in your screenshot:

```python
df = pd.read_sql(query, connection)  # where query contains your SELECT * FROM projects_table
```

Make sure to keep only relevant columns:

```python
df = df[["PROJECT_NAME", "PROJECT_LUID", "PARENT_PROJECT_LUID"]]
```

---

### 📦 Requirements

Install required packages if not already installed:

```bash
pip install streamlit plotly pandas
```

Then run:

```bash
streamlit run your_script_name.py
```

---

Would you prefer a **collapsible text tree** (like a `nested list`) or this **treemap visualization**? I can show both.
