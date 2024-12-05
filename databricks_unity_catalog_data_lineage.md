# **Exploring Data Lineage with Databricks Unity Catalog**

### **Introduction**
Data lineage is a critical component of data governance, enabling organizations to understand and visualize the flow of data across systems. It tracks the origins, transformations, and usage of data, providing transparency, ensuring data quality, and supporting compliance with regulatory requirements.

With **Databricks Unity Catalog**, you can easily capture and visualize data lineage for tables, views, and columns, simplifying data governance and aiding in impact analysis and auditing.

---

### **What is Data Lineage?**

**Data Lineage** refers to the lifecycle of data:  
- **Where it originates**: Data sources (e.g., files, databases).  
- **How it is transformed**: ETL/ELT processes, calculations, or aggregations.  
- **Where it is used**: Reports, dashboards, or machine learning models.

#### **Why is Data Lineage Important?**
1. **Traceability**: Identify the source of data anomalies.
2. **Compliance**: Support regulatory audits (e.g., GDPR, HIPAA).
3. **Impact Analysis**: Understand dependencies before making schema changes.

---

### **Unity Catalog and Data Lineage**

Databricks Unity Catalog provides automated data lineage tracking for both **upstream** and **downstream** data flows, including the column-level granularity. This simplifies governance by visualizing the transformations and usage across your data ecosystem.

---

### **Example: Implementing Data Lineage in Unity Catalog**

Let’s walk through an example of setting up and viewing data lineage in Databricks Unity Catalog.

#### **Objective**
Track the lineage of data as it flows from a raw file into a transformed table and subsequently into a report view.

---

#### **Step 1: Load Raw Data**

1. Save the raw data (`sales_raw.csv`) to an object storage (e.g., AWS S3).

   **Sample Data (sales_raw.csv):**
   ```csv
   sales_id,customer_name,amount,date
   1,John Doe,100,2023-11-01
   2,Jane Smith,200,2023-11-02
   ```

2. Mount the storage in Databricks:
   ```python
   dbutils.fs.mount(
       source="s3a://your-bucket/sales-data/",
       mount_point="/mnt/sales-data",
       extra_configs={"fs.s3a.access.key": "your-access-key", "fs.s3a.secret.key": "your-secret-key"}
   )
   ```

3. Load the raw data into a Delta table:
   ```python
   from pyspark.sql import SparkSession

   spark = SparkSession.builder.getOrCreate()

   # Load the CSV file
   raw_data = spark.read.csv("/mnt/sales-data/sales_raw.csv", header=True, inferSchema=True)

   # Save to Unity Catalog
   raw_data.write.format("delta").saveAsTable("sales_catalog.raw_sales_data")
   ```

---

#### **Step 2: Transform Data**

1. Perform a transformation on the raw data:
   ```python
   transformed_data = spark.sql("""
       SELECT
           sales_id,
           customer_name,
           amount * 1.1 AS amount_with_tax,
           date
       FROM sales_catalog.raw_sales_data
   """)

   # Save the transformed data
   transformed_data.write.format("delta").saveAsTable("sales_catalog.transformed_sales_data")
   ```

---

#### **Step 3: Create a Report View**

1. Create a SQL view for reporting purposes:
   ```sql
   CREATE VIEW sales_catalog.sales_report AS
   SELECT
       customer_name,
       SUM(amount_with_tax) AS total_sales
   FROM sales_catalog.transformed_sales_data
   GROUP BY customer_name;
   ```

---

#### **Step 4: Visualize Data Lineage**

Unity Catalog automatically tracks lineage. To view it:

1. Open the **Unity Catalog UI** in Databricks.
2. Navigate to the **"Data"** tab and select `sales_catalog`.
3. Click on **"Lineage"** for:
   - **Table Lineage**: View how `sales_catalog.transformed_sales_data` and `sales_catalog.sales_report` depend on `sales_catalog.raw_sales_data`.
   - **Column Lineage**: Drill down to column-level transformations, e.g., `amount` transformed into `amount_with_tax`.

---

#### **Step 5: Verify Lineage with API**

Databricks provides an API for querying lineage programmatically.

```python
from databricks.sdk import WorkspaceClient

client = WorkspaceClient()

# Fetch lineage for a table
lineage = client.lineage.get_table_lineage(
    catalog_name="sales_catalog",
    schema_name="default",
    table_name="transformed_sales_data"
)

print(lineage)
```

**Output:**
```json
{
  "upstream": [
    {"table": "sales_catalog.raw_sales_data", "columns": ["amount", "sales_id"]}
  ],
  "downstream": [
    {"table": "sales_catalog.sales_report", "columns": ["total_sales"]}
  ]
}
```

---

### **Results and Insights**

By following this workflow:
- **Upstream Lineage**: We see that `transformed_sales_data` depends on `raw_sales_data`.
- **Downstream Lineage**: We observe that `sales_report` depends on `transformed_sales_data`.
- **Column Lineage**: We can trace how `amount` is transformed into `amount_with_tax`.

---

### **Conclusion**

Data lineage with Databricks Unity Catalog provides:
- **Transparency**: Easy-to-understand visuals of data dependencies.
- **Compliance**: Ensures regulatory and audit requirements are met.
- **Impact Analysis**: Allows safe schema updates by understanding dependencies.

With its integration of automated lineage tracking and API access, Unity Catalog makes it simpler to govern data in modern, large-scale environments.

---

### **Call to Action**

Ready to implement data lineage in your organization? Start by enabling Unity Catalog in your Databricks workspace and automate lineage tracking for all your data assets. Explore more features like column-level lineage and lineage APIs to optimize your data governance strategy.
