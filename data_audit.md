### What is Data Audit in Data Engineering?
A **data audit** in data engineering is a systematic process of assessing and ensuring the quality, accuracy, consistency, and security of data in a system. It helps identify anomalies, missing values, incorrect data formats, duplicate records, or compliance issues, ensuring the data meets organizational and legal standards.

### Objectives of a Data Audit:
- Ensure data integrity and quality.
- Identify and rectify data anomalies.
- Validate data consistency across systems.
- Monitor compliance with data governance policies.

### Popular Data Audit Tools
1. **Great Expectations**: An open-source tool for validating, documenting, and profiling data.
2. **Apache Griffin**: A data quality solution for data integrity and accuracy checks.
3. **Talend Data Quality**: Provides a comprehensive suite for data profiling, cleansing, and monitoring.
4. **Pandas Profiling** (Python library): A lightweight tool for generating detailed data quality reports.

Among these, **Great Expectations** is one of the most popular for modern data engineering workflows.

---

### Example of a Data Audit Project
**Objective**: Audit a sales dataset to ensure data quality before ingestion into a data warehouse.

#### Steps:
1. **Set Up the Environment**
   Install required tools and libraries:
   ```bash
   pip install great_expectations pandas sqlalchemy
   ```

2. **Load Data**
   Use Python to load a sample sales dataset:
   ```python
   import pandas as pd

   # Load the dataset
   data = pd.read_csv('sales_data.csv')

   # Display a sample
   print(data.head())
   ```

3. **Initialize Great Expectations**
   Set up a project:
   ```bash
   great_expectations init
   ```

4. **Profile the Data**
   Create a data context and generate a profiling report:
   ```python
   from great_expectations.profile import BasicDatasetProfiler
   from great_expectations.data_context import DataContext
   from great_expectations.dataset import PandasDataset

   # Create a Great Expectations DataContext
   context = DataContext()

   # Wrap the dataset with Great Expectations
   dataset = PandasDataset(data)

   # Profile the dataset
   profiling_results = BasicDatasetProfiler.profile(dataset)
   print(profiling_results)
   ```

5. **Define Expectations**
   Define expectations for the data quality:
   ```python
   dataset.expect_column_to_exist("sales_amount")
   dataset.expect_column_values_to_be_of_type("sales_amount", "float")
   dataset.expect_column_values_to_not_be_null("sales_amount")
   dataset.expect_column_values_to_be_between("sales_amount", 0, 10000)
   ```

6. **Validate the Data**
   Validate the dataset against expectations:
   ```python
   results = dataset.validate()
   print(results)
   ```

7. **Handle Anomalies**
   Export rows that fail validation for review:
   ```python
   failed_data = data[~dataset.get_expectation_suite().validate().success]
   failed_data.to_csv("failed_data.csv", index=False)
   ```

8. **Integrate with ETL**
   Only move valid data to the next stage:
   ```python
   valid_data = data[dataset.get_expectation_suite().validate().success]

   # Connect to a database (e.g., Snowflake)
   from sqlalchemy import create_engine
   engine = create_engine('snowflake://user:password@snowflake_url/db')

   # Load data into the warehouse
   valid_data.to_sql('sales_data_cleaned', con=engine, if_exists='replace', index=False)
   ```

9. **Automate the Audit**
   Automate the process with a CI/CD pipeline or scheduled script using tools like **Apache Airflow**.

10. **Monitor and Report**
    Continuously monitor data quality and generate reports:
    ```python
    context.run_validation_operator(
        "action_list_operator", assets_to_validate=[dataset]
    )
    ```

---

### Benefits of a Data Audit Project
- Ensures only clean and valid data is processed.
- Reduces downstream errors and data inconsistencies.
- Supports compliance with data governance frameworks.
