Here's a **Streamlit UI** that allows users to:  
1. **Select a project** from a dropdown (based on `project_name`).  
2. **Select a view** from a dynamically updated dropdown (filtered based on `project_id`).  
3. **Load the view data into the session** for further interactions.  
4. **Ask questions about the view data** using an input field.  

---

### 📌 Steps:
- Load the `.json` file into a Pandas DataFrame.
- Create dropdowns for `project_name` and `view_name` using `st.selectbox`.
- Store selected `view_data` in `st.session_state`.
- Provide a text input for the user to ask questions about the selected view.

---

Here’s the **Streamlit app code**:  

```python
import streamlit as st
import pandas as pd
import json

# Load JSON file
@st.cache_data
def load_data(file_path):
    return pd.read_json(file_path)

# Load dataset (Replace with your actual JSON file path)
file_path = "views_data.json"  # Change this to your actual file
df = load_data(file_path)

# Sidebar: Select Project
st.sidebar.header("Select Project & View")

# Get unique project names
project_names = df["project_name"].unique()
selected_project = st.sidebar.selectbox("Select a Project", project_names)

# Filter views based on selected project
filtered_views = df[df["project_name"] == selected_project]
view_names = filtered_views["view_name"].unique()

# Sidebar: Select View
selected_view = st.sidebar.selectbox("Select a View", view_names)

# Load view data into session state
if selected_view:
    view_data = filtered_views[filtered_views["view_name"] == selected_view].to_dict(orient="records")
    st.session_state["view_data"] = view_data
    st.success(f"Loaded data for view: {selected_view}")

# User question input
st.header("Ask Questions About the Selected View")
user_question = st.text_input("Enter your question about the view data:")

if user_question:
    if "view_data" in st.session_state:
        # Placeholder for processing question with the loaded data
        st.write(f"🔍 You asked: '{user_question}'")
        st.write("📊 Here’s some data from your selected view:", st.session_state["view_data"])
    else:
        st.warning("Please select a view first.")
```

---

### 🎯 Features:
✅ **Dynamically updated view dropdown** based on selected project.  
✅ **Stores selected view data** in `st.session_state`.  
✅ **Allows users to ask questions** about the selected view.  

Would you like to integrate an AI model to answer questions based on the view data? 🚀
