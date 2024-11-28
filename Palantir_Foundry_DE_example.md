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
