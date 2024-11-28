Here's an **end-to-end example** of building a **data engineering pipeline** in **Palantir Foundry**. This example demonstrates how to ingest raw data, transform it, and prepare it for analysis while leveraging Foundry’s tools like **Code Workbook**, **Transforms**, and **Pipelines**.

---

### **Use Case: Building a Sales Data Pipeline**

#### **1. Data Ingestion**

**Action**: Import raw CSV files containing sales data into Foundry.

**Steps**:
1. Navigate to the **Foundry Files** workspace.
2. Upload `sales_data.csv` (example file with columns: `OrderDate`, `Product`, `Category`, `SalesAmount`, `CostAmount`).
3. Register the file in Foundry's data catalog.

Here’s an example of the content of `sales_data.csv`, which we use as input to the Palantir Foundry pipeline:

### **sales_data.csv**
```csv
OrderDate,Product,Category,SalesAmount,CostAmount
2024-01-01,Widget A,Category 1,100,60
2024-01-01,Widget B,Category 2,200,120
2024-01-02,Widget C,Category 1,150,90
2024-01-02,Widget D,Category 3,300,250
2024-01-03,Widget E,Category 2,-50,40
```

### **Explanation of Fields**
- `OrderDate`: The date when the sale occurred.
- `Product`: Name of the product sold.
- `Category`: The category of the product.
- `SalesAmount`: The total amount for the sale (may include negative values for returns).
- `CostAmount`: The cost associated with the sale.


---

#### **2. Data Transformation (Python Transform)**

**Goal**: Clean the data and calculate new fields (e.g., Profit).

1. **Create a new Code Workbook** in Foundry.
2. Add a **Transform** block and write Python code.

**Python Code Example**:
```python
from transforms.api import transform, Input, Output

@transform(
    output=Output("/foundry/data/cleaned_sales_data"),
    input=Input("/foundry/data/raw_sales_data"),
)
def clean_sales_data(input, output):
    import pandas as pd

    # Load data
    df = input.dataframe()

    # Data cleaning
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Profit'] = df['SalesAmount'] - df['CostAmount']

    # Filter out negative sales amounts
    df = df[df['SalesAmount'] > 0]

    # Save cleaned data
    output.write_dataframe(df)
```

---

#### **3. Aggregation and Analysis**

**Goal**: Aggregate sales data by category and calculate total sales, average profit, and profit margin.

1. Add another Transform block for aggregation.

**Python Code Example**:
```python
@transform(
    output=Output("/foundry/data/aggregated_sales_data"),
    input=Input("/foundry/data/cleaned_sales_data"),
)
def aggregate_sales_data(input, output):
    import pandas as pd

    # Load cleaned data
    df = input.dataframe()

    # Aggregation
    summary = df.groupby('Category').agg(
        TotalSales=pd.NamedAgg(column='SalesAmount', aggfunc='sum'),
        AverageProfit=pd.NamedAgg(column='Profit', aggfunc='mean'),
        ProfitMargin=pd.NamedAgg(column='Profit', aggfunc=lambda x: x.sum() / df['SalesAmount'].sum())
    ).reset_index()

    # Save aggregated data
    output.write_dataframe(summary)
```

---

#### **4. Automation with Pipelines**

**Goal**: Automate the transformations into a repeatable pipeline.

1. **Create a pipeline** in Foundry.
2. Add the following steps:
   - Data Ingestion (raw CSV).
   - Data Cleaning Transform (`clean_sales_data`).
   - Aggregation Transform (`aggregate_sales_data`).
3. Schedule the pipeline to run daily.

---

#### **5. Visualization**

**Goal**: Use Palantir's integrated dashboards to visualize the aggregated data.

1. Create a **Workbook**.
2. Connect to the `/foundry/data/aggregated_sales_data` dataset.
3. Add visualizations:
   - Bar chart: Total sales by category.
   - Line chart: Profit margin over time.

---

### **How These Components Are Connected**

- **Raw Data**: Uploaded as a file and cataloged.
- **Transforms**: Process raw data using Python for cleaning and aggregation.
- **Pipeline**: Automates the sequence of data preparation steps.
- **Dataset**: Output from the pipeline is ready for analytics and visualization.
- **Visualization**: Insights presented in a dashboard.

---

### **Outcome**

You now have a fully automated pipeline in Foundry that:
- Cleanses raw sales data.
- Computes advanced metrics like profit margin.
- Prepares data for visualization and analysis.

This approach showcases the modularity and scalability of Palantir Foundry for data engineering tasks.



---

### **Pipeline Outcome**

After processing the data:
1. **Cleaned Sales Data**:
   - Removes rows with negative `SalesAmount` values.
   - Adds a `Profit` column.

```csv
OrderDate,Product,Category,SalesAmount,CostAmount,Profit
2024-01-01,Widget A,Category 1,100,60,40
2024-01-01,Widget B,Category 2,200,120,80
2024-01-02,Widget C,Category 1,150,90,60
2024-01-02,Widget D,Category 3,300,250,50
```

2. **Aggregated Sales Data**:
   - Groups data by `Category`.
   - Computes `TotalSales`, `AverageProfit`, and `ProfitMargin`.

```csv
Category,TotalSales,AverageProfit,ProfitMargin
Category 1,250,50,0.2
Category 2,200,80,0.16
Category 3,300,50,0.24
```

---

This data becomes available for visualization in Palantir Foundry dashboards or export for external analytics tools.
