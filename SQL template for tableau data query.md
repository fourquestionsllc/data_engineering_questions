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
