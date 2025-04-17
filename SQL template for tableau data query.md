Ttrying to create robust SQL templates that can map natural language questions about Tableau metadata (workbooks, views, data sources, and view keywords) into executable SQL queries.

I'll outline some common categories of questions and provide SQL templates for each, along with:

- **Example user questions**
- **SQL template**
- **Fillable fields** (placeholders for values extracted from the question)

---

### **Template 1: List Views in a Workbook**
**Example Questions:**
- What views are in the "Sales Dashboard" workbook?
- Show me all views from the "Marketing Insights" workbook.
- Which views belong to the "Executive Summary"?

**SQL Template:**
```sql
SELECT view_name
FROM views
WHERE workbook_name = '{workbook_name}';
```

**Fields to Extract:**
- `{workbook_name}`

---

### **Template 2: List Workbooks by Data Source**
**Example Questions:**
- Which workbooks use the "Customer Orders" data source?
- Show me workbooks connected to "Sales DB".
- What workbooks are based on the "Finance Data" source?

**SQL Template:**
```sql
SELECT DISTINCT workbook_name
FROM workbooks
WHERE data_source_name = '{data_source_name}';
```

**Fields to Extract:**
- `{data_source_name}`

---

### **Template 3: Get Views by Keyword**
**Example Questions:**
- Find views with the keyword "revenue".
- Show me views tagged with "Q4".
- What views are related to "churn"?

**SQL Template:**
```sql
SELECT v.view_name
FROM views v
JOIN view_keywords vk ON v.view_id = vk.view_id
WHERE vk.keyword = '{keyword}';
```

**Fields to Extract:**
- `{keyword}`

---

### **Template 4: Get All Keywords for a View**
**Example Questions:**
- What keywords are associated with "Monthly Revenue"?
- Show me the tags for the "Profit Trends" view.
- Which keywords are linked to the "Churn Analysis" view?

**SQL Template:**
```sql
SELECT keyword
FROM view_keywords
WHERE view_id = (
    SELECT view_id
    FROM views
    WHERE view_name = '{view_name}'
);
```

**Fields to Extract:**
- `{view_name}`

---

### **Template 5: Find Views Using a Data Source**
**Example Questions:**
- What views use the "Sales DB" data source?
- Which views are built on "Customer Data"?
- List views connected to "Orders Source".

**SQL Template:**
```sql
SELECT view_name
FROM views
WHERE data_source_name = '{data_source_name}';
```

**Fields to Extract:**
- `{data_source_name}`

---

### **Template 6: List All Workbooks**
**Example Questions:**
- Show me all workbooks.
- List every workbook available.
- What are the workbooks in Tableau?

**SQL Template:**
```sql
SELECT workbook_name
FROM workbooks;
```

**Fields to Extract:**
- *(None)*

---



Perfect — we’ll use a **prompt-based classifier** using an LLM to choose the best SQL template for a given user question. The idea is to feed the LLM:

- The list of templates (with IDs and descriptions)
- The user’s question
- A request to pick the most suitable template ID and extract the values for placeholders

---

## 🔧 Setup: Template Catalog

Here's a structured version of the SQL templates we defined:

```json
[
  {
    "id": "T1",
    "description": "List views in a specific workbook",
    "placeholders": ["workbook_name"]
  },
  {
    "id": "T2",
    "description": "List workbooks that use a specific data source",
    "placeholders": ["data_source_name"]
  },
  {
    "id": "T3",
    "description": "Get views by a specific keyword",
    "placeholders": ["keyword"]
  },
  {
    "id": "T4",
    "description": "Get keywords associated with a specific view",
    "placeholders": ["view_name"]
  },
  {
    "id": "T5",
    "description": "Find views using a specific data source",
    "placeholders": ["data_source_name"]
  },
  {
    "id": "T6",
    "description": "List all workbooks",
    "placeholders": []
  }
]
```

---

## 🧠 Prompt Template for Classification

Here’s a prompt you can use with an LLM (e.g., via LangChain or OpenAI directly):

```text
You are an AI assistant that maps natural language questions to SQL templates.

Available SQL templates:
T1 - List views in a specific workbook
T2 - List workbooks that use a specific data source
T3 - Get views by a specific keyword
T4 - Get keywords associated with a specific view
T5 - Find views using a specific data source
T6 - List all workbooks

Given a user question, do the following:
1. Select the best matching template ID from the list (e.g., T1, T2, etc.)
2. Extract values for any placeholders needed by that template.

Respond in the following JSON format:

{
  "template_id": "<template_id>",
  "placeholders": {
    "<placeholder1>": "<value>",
    ...
  }
}

Example:

User Question: "Which workbooks use the Sales DB data source?"

Output:
{
  "template_id": "T2",
  "placeholders": {
    "data_source_name": "Sales DB"
  }
}

Now process the following question:
"{user_question}"
```

Replace `{user_question}` with the actual user input.

---

## ✅ Example Output

For the input:  
**"Show me all views from the Marketing Insights workbook."**

The LLM should return:

```json
{
  "template_id": "T1",
  "placeholders": {
    "workbook_name": "Marketing Insights"
  }
}
```

---

Would you like me to help you implement this using LangChain or Semantic Kernel? Or are you planning to use OpenAI’s API directly for classification?
