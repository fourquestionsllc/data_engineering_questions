# **Role-Based Access Control (RBAC) in Data Engineering**

### **What is Role-Based Access Control (RBAC)?**

Role-Based Access Control (RBAC) is a security mechanism that restricts system access to users based on their roles within an organization. In the context of data engineering, RBAC ensures that users can only access the data and resources necessary for their job functions. This approach simplifies permissions management, enhances security, and supports compliance with regulatory requirements.

---

### **Benefits of RBAC**
1. **Granular Access Control**: Assign permissions at the table, column, or catalog level.
2. **Simplified Management**: Manage access by roles instead of individual users.
3. **Enhanced Security**: Reduce the risk of unauthorized data access.
4. **Regulatory Compliance**: Enforce policies aligned with data protection regulations.

---

### **Implementing RBAC with Databricks Unity Catalog**

Databricks Unity Catalog enables centralized RBAC for all data assets, such as tables, views, and catalogs. Here’s how you can implement RBAC with Unity Catalog step by step.

---

### **Example: End-to-End Implementation of RBAC**

#### **Objective**
Create a setup where:
1. **Data Scientists** can only query specific columns.
2. **Data Engineers** can access full tables.
3. **Managers** can access aggregated reports only.

#### **Step 1: Prerequisites**
Ensure Unity Catalog is enabled in your Databricks workspace.

- Unity Catalog Admin privileges.
- A configured catalog and schema.

---

#### **Step 2: Create Catalogs and Schemas**

1. Create a catalog for organizing data:
   ```sql
   CREATE CATALOG company_data;
   ```

2. Create a schema within the catalog:
   ```sql
   CREATE SCHEMA company_data.sales_data;
   ```

---

#### **Step 3: Load Sample Data**

1. Load a sample sales data table:
   ```python
   from pyspark.sql import SparkSession

   spark = SparkSession.builder.getOrCreate()

   # Sample data
   data = [
       ("John Doe", "Product A", 100, "2023-12-01"),
       ("Jane Smith", "Product B", 200, "2023-12-02"),
   ]
   columns = ["customer_name", "product", "amount", "date"]

   # Create DataFrame and save to Unity Catalog
   df = spark.createDataFrame(data, columns)
   df.write.format("delta").saveAsTable("company_data.sales_data.sales_transactions")
   ```

---

#### **Step 4: Define Roles**

1. Define roles for **Data Scientists**, **Data Engineers**, and **Managers**:
   ```sql
   -- Create roles
   CREATE ROLE data_scientist_role;
   CREATE ROLE data_engineer_role;
   CREATE ROLE manager_role;
   ```

---

#### **Step 5: Grant Permissions**

1. Grant permissions to **Data Scientists**:
   - Restrict access to the `amount` column only:
   ```sql
   GRANT SELECT (amount) ON TABLE company_data.sales_data.sales_transactions TO ROLE data_scientist_role;
   ```

2. Grant permissions to **Data Engineers**:
   - Full access to the entire table:
   ```sql
   GRANT SELECT ON TABLE company_data.sales_data.sales_transactions TO ROLE data_engineer_role;
   ```

3. Grant permissions to **Managers**:
   - Allow access to an aggregated report only:
   ```sql
   CREATE VIEW company_data.sales_data.sales_summary AS
   SELECT product, SUM(amount) AS total_sales
   FROM company_data.sales_data.sales_transactions
   GROUP BY product;

   GRANT SELECT ON VIEW company_data.sales_data.sales_summary TO ROLE manager_role;
   ```

---

#### **Step 6: Assign Roles to Users**

Assign roles to users using Unity Catalog.

1. Assign the **data_scientist_role** to a user:
   ```sql
   GRANT ROLE data_scientist_role TO USER 'data_scientist@example.com';
   ```

2. Assign the **data_engineer_role** to a user:
   ```sql
   GRANT ROLE data_engineer_role TO USER 'data_engineer@example.com';
   ```

3. Assign the **manager_role** to a user:
   ```sql
   GRANT ROLE manager_role TO USER 'manager@example.com';
   ```

---

#### **Step 7: Validate Access**

1. **Data Scientist**:
   Run a query to validate column-level access:
   ```sql
   SELECT amount FROM company_data.sales_data.sales_transactions;
   ```
   Result: Only the `amount` column is accessible.

2. **Data Engineer**:
   Run a query to validate full-table access:
   ```sql
   SELECT * FROM company_data.sales_data.sales_transactions;
   ```
   Result: Full table is accessible.

3. **Manager**:
   Run a query to validate view-level access:
   ```sql
   SELECT * FROM company_data.sales_data.sales_summary;
   ```
   Result: Only the aggregated summary is accessible.

---

### **Results**

1. **Data Scientists** can only access sensitive data (e.g., sales amounts).
2. **Data Engineers** have complete visibility into the transactional data.
3. **Managers** see high-level insights for decision-making.

---

### **Monitoring and Auditing**

Unity Catalog provides built-in auditing to monitor access:
```sql
SELECT *
FROM information_schema.access_audit_logs
WHERE catalog_name = 'company_data';
```

---

### **Conclusion**

RBAC with Unity Catalog simplifies the process of managing permissions in Databricks, ensuring secure, compliant, and efficient access to data assets. By defining roles and assigning granular permissions, organizations can enforce strict data governance while empowering users with the access they need.
