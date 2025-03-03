### **SQL Interview Question**  

You have a sales table with the following schema:  

```sql
CREATE TABLE sales (
    customer_id INT,
    sales_date DATE,
    volume INT
);
```

#### **Question:**  
Find the **top 3 customers** who had the **highest total sales volume** in **each month**. If two customers have the same sales volume, rank them by `customer_id` in ascending order.  

#### **Expected Output:**
| month  | customer_id | total_volume | rank |
|--------|------------|--------------|------|
| 2024-01 | 101        | 500          | 1    |
| 2024-01 | 203        | 450          | 2    |
| 2024-01 | 305        | 400          | 3    |
| 2024-02 | 102        | 600          | 1    |
| 2024-02 | 201        | 550          | 2    |
| 2024-02 | 103        | 500          | 3    |

---

### **SQL Solution (Using `DENSE_RANK()`)**

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', sales_date) AS month,
        customer_id,
        SUM(volume) AS total_volume
    FROM sales
    GROUP BY month, customer_id
),
ranked_sales AS (
    SELECT 
        month,
        customer_id,
        total_volume,
        DENSE_RANK() OVER (PARTITION BY month ORDER BY total_volume DESC, customer_id ASC) AS rank
    FROM monthly_sales
)
SELECT month, customer_id, total_volume, rank
FROM ranked_sales
WHERE rank <= 3
ORDER BY month, rank;
```

---

### **Explanation:**
1. **Aggregate Sales Volume per Customer per Month**  
   - Use `DATE_TRUNC('month', sales_date)` to extract the month from `sales_date`.  
   - Sum the `volume` for each `customer_id` per month.  

2. **Rank Customers Within Each Month**  
   - Use `DENSE_RANK()` to rank customers by `total_volume` within each month.  
   - If two customers have the same volume, they are ranked based on `customer_id` (ascending).  

3. **Filter the Top 3 Customers per Month**  
   - Use `WHERE rank <= 3` to keep only the top 3 customers.  
