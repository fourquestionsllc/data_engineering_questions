### **Interview Coding Question: Sales Forecasting Using Machine Learning**  

#### **Problem Statement:**  
You are given a dataset containing historical sales data for a set of products across multiple stores. Your task is to build a machine learning model to predict future sales for each product-store combination.  

#### **Dataset Schema:**  

| date       | store_id | product_id | sales_units | price | competitor_price | holiday | temperature | promotion |  
|------------|----------|------------|--------------|--------|------------------|---------|-------------|-----------|  
| 2024-01-01 | 1        | 101        | 50           | 10.0   | 9.5              | 0       | 32          | 1         |  
| 2024-01-02 | 1        | 101        | 45           | 10.0   | 9.5              | 0       | 34          | 0         |  
| 2024-01-03 | 1        | 101        | 55           | 10.0   | 9.5              | 1       | 30          | 1         |  
| 2024-01-04 | 2        | 102        | 40           | 12.0   | 11.8             | 0       | 29          | 1         |  
| 2024-01-05 | 2        | 102        | 35           | 12.5   | 11.9             | 0       | 31          | 0         |  

#### **Tasks:**  
1. Perform basic feature engineering on the dataset, including lag features and moving averages.  
2. Train a machine learning model (e.g., XGBoost or Random Forest) to predict `sales_units`.  
3. Evaluate the model using RMSE (Root Mean Squared Error) on a validation set.  

---

### **Solution**  

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Step 1: Load the dataset
data = pd.DataFrame({
    "date": pd.date_range(start="2024-01-01", periods=10),
    "store_id": [1, 1, 1, 2, 2, 2, 1, 2, 1, 2],
    "product_id": [101, 101, 101, 102, 102, 102, 101, 102, 101, 102],
    "sales_units": [50, 45, 55, 40, 35, 38, 52, 41, 48, 39],
    "price": [10.0, 10.0, 10.0, 12.0, 12.5, 12.2, 9.8, 12.1, 9.9, 12.3],
    "competitor_price": [9.5, 9.5, 9.5, 11.8, 11.9, 11.7, 9.4, 11.8, 9.6, 11.7],
    "holiday": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    "temperature": [32, 34, 30, 29, 31, 28, 33, 30, 31, 29],
    "promotion": [1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
})

# Step 2: Feature Engineering
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values(["store_id", "product_id", "date"])

# Lag Features
data["sales_lag_1"] = data.groupby(["store_id", "product_id"])["sales_units"].shift(1)
data["sales_lag_2"] = data.groupby(["store_id", "product_id"])["sales_units"].shift(2)

# Moving Average Features
data["sales_ma_3"] = data.groupby(["store_id", "product_id"])["sales_units"].transform(lambda x: x.rolling(3, min_periods=1).mean())

# Drop NaN values after feature creation
data = data.dropna()

# Step 3: Train-Test Split
features = ["price", "competitor_price", "holiday", "temperature", "promotion", "sales_lag_1", "sales_lag_2", "sales_ma_3"]
X = data[features]
y = data["sales_units"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Model Training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Model Evaluation
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:.2f}")
```

---

### **Explanation of the Solution:**
1. **Feature Engineering:**
   - **Lag Features:** Added `sales_lag_1` and `sales_lag_2`, which capture past sales trends.
   - **Moving Averages:** Added `sales_ma_3` as a rolling mean of the last 3 days.
2. **Model Training:**
   - Used `RandomForestRegressor` for predicting sales based on engineered features.
3. **Model Evaluation:**
   - Used RMSE to evaluate the prediction error.

This solution captures seasonality, price effects, and promotions, making it useful for sales forecasting tasks.
