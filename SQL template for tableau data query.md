# Trying to create robust SQL templates that can map natural language questions about Tableau metadata (workbooks, views, data sources, and view keywords) into executable SQL queries.

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

Awesome — let’s put it all together in a simple Python implementation that:

1. Uses an LLM (e.g., OpenAI GPT) to classify a question.
2. Maps the output to a SQL template.
3. Fills in the placeholders to generate an executable SQL query.

We’ll assume you’re using OpenAI’s API (you can adapt it for LangChain/Semantic Kernel if needed).

---

## ✅ Prerequisites

Install `openai` if you haven’t already:

```bash
pip install openai
```

---

## 🧠 Python Code (LLM + Template Filler)

```python
import openai

# Set your OpenAI key
openai.api_key = "your-api-key"

# Define SQL templates
SQL_TEMPLATES = {
    "T1": {
        "sql": "SELECT view_name FROM views WHERE workbook_name = '{workbook_name}';"
    },
    "T2": {
        "sql": "SELECT DISTINCT workbook_name FROM workbooks WHERE data_source_name = '{data_source_name}';"
    },
    "T3": {
        "sql": """
            SELECT v.view_name
            FROM views v
            JOIN view_keywords vk ON v.view_id = vk.view_id
            WHERE vk.keyword = '{keyword}';
        """
    },
    "T4": {
        "sql": """
            SELECT keyword
            FROM view_keywords
            WHERE view_id = (
                SELECT view_id FROM views WHERE view_name = '{view_name}'
            );
        """
    },
    "T5": {
        "sql": "SELECT view_name FROM views WHERE data_source_name = '{data_source_name}';"
    },
    "T6": {
        "sql": "SELECT workbook_name FROM workbooks;"
    }
}

# LLM prompt
def build_prompt(user_question):
    return f"""
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

{{
  "template_id": "<template_id>",
  "placeholders": {{
    "<placeholder1>": "<value>"
  }}
}}

Now process the following question:
"{user_question}"
"""

# Use OpenAI to classify and extract placeholders
def classify_and_fill(user_question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "user", "content": build_prompt(user_question)}
        ]
    )
    
    import json
    classification = json.loads(response['choices'][0]['message']['content'])
    template_id = classification["template_id"]
    placeholders = classification.get("placeholders", {})

    template_sql = SQL_TEMPLATES[template_id]["sql"]
    
    for key, value in placeholders.items():
        template_sql = template_sql.replace(f"{{{key}}}", value)
    
    return template_sql.strip()

# Example usage
if __name__ == "__main__":
    question = "Show me all views from the Marketing Insights workbook"
    sql_query = classify_and_fill(question)
    print("Generated SQL:")
    print(sql_query)
```

---

## 🔄 Output for Example

**User Input:**
```text
Show me all views from the Marketing Insights workbook
```

**Output SQL:**
```sql
SELECT view_name FROM views WHERE workbook_name = 'Marketing Insights';
```

---



# fuzzy matching adds robustness when user questions contain slight variations or when the LLM misinterprets a placeholder.

We’ll enhance the pipeline to:

1. Fuzzy-match extracted placeholder values (like workbook names or data sources) against known metadata.
2. Replace the LLM’s placeholder values with the closest match.

---

### ✅ Updated Steps:

- Use `fuzzywuzzy` (or `rapidfuzz` — more performant) to do the fuzzy matching.
- Assume you have access to lists of known:
  - Workbook names
  - View names
  - Data source names
  - Keywords

---

### 📦 Install Dependencies

```bash
pip install rapidfuzz
```

---

### 🧠 Updated Python Code (with fuzzy matching)

```python
import openai
from rapidfuzz import process

# Set your OpenAI API key
openai.api_key = "your-api-key"

# Sample metadata (replace with your real data)
METADATA = {
    "workbook_name": [
        "Marketing Insights", "Sales Dashboard", "Executive Summary"
    ],
    "view_name": [
        "Monthly Revenue", "Profit Trends", "Churn Analysis"
    ],
    "data_source_name": [
        "Sales DB", "Customer Orders", "Finance Data"
    ],
    "keyword": [
        "revenue", "Q4", "churn"
    ]
}

# SQL Templates
SQL_TEMPLATES = {
    "T1": {
        "sql": "SELECT view_name FROM views WHERE workbook_name = '{workbook_name}';"
    },
    "T2": {
        "sql": "SELECT DISTINCT workbook_name FROM workbooks WHERE data_source_name = '{data_source_name}';"
    },
    "T3": {
        "sql": """
            SELECT v.view_name
            FROM views v
            JOIN view_keywords vk ON v.view_id = vk.view_id
            WHERE vk.keyword = '{keyword}';
        """
    },
    "T4": {
        "sql": """
            SELECT keyword
            FROM view_keywords
            WHERE view_id = (
                SELECT view_id FROM views WHERE view_name = '{view_name}'
            );
        """
    },
    "T5": {
        "sql": "SELECT view_name FROM views WHERE data_source_name = '{data_source_name}';"
    },
    "T6": {
        "sql": "SELECT workbook_name FROM workbooks;"
    }
}

# LLM prompt
def build_prompt(user_question):
    return f"""
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

{{
  "template_id": "<template_id>",
  "placeholders": {{
    "<placeholder1>": "<value>"
  }}
}}

Now process the following question:
"{user_question}"
"""

# Fuzzy match function
def fuzzy_match(value, field_type):
    choices = METADATA.get(field_type, [])
    match, score, _ = process.extractOne(value, choices, score_cutoff=70)
    return match if match else value

# LLM + Fuzzy Matching Pipeline
def classify_and_fill(user_question):
    import json

    # Step 1: Use LLM to classify and extract
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": build_prompt(user_question)}
        ]
    )
    result = json.loads(response['choices'][0]['message']['content'])

    template_id = result["template_id"]
    placeholders = result.get("placeholders", {})

    # Step 2: Fuzzy match placeholder values
    fuzzy_placeholders = {}
    for key, val in placeholders.items():
        fuzzy_val = fuzzy_match(val, key)
        fuzzy_placeholders[key] = fuzzy_val

    # Step 3: Fill the SQL template
    template_sql = SQL_TEMPLATES[template_id]["sql"]
    for key, value in fuzzy_placeholders.items():
        template_sql = template_sql.replace(f"{{{key}}}", value)

    return template_sql.strip()

# Example usage
if __name__ == "__main__":
    user_input = "What views are in the marketing insight workbook?"
    sql = classify_and_fill(user_input)
    print("Generated SQL:")
    print(sql)
```

---

### ✅ Sample Output

**Input:**  
`What views are in the marketing insight workbook?`

**Fuzzy matched:**  
`"marketing insight"` → `"Marketing Insights"`

**Output SQL:**
```sql
SELECT view_name FROM views WHERE workbook_name = 'Marketing Insights';
```
