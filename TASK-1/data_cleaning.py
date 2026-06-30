
import pandas as pd
import numpy as np

print("=" * 60)
print("  DATA CLEANING & TRANSFORMATION PIPELINE")
print("=" * 60)

#  2. Load Raw Dataset

df = pd.read_csv("ecommerce_sales_34500.csv")
print(f"\nRaw dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
original_shape = df.shape
print("STEP 1: Fixing Data Types")

#     This enables time-based operations like extracting year, month, weekday
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')
print(f"'order_date' converted to datetime. Sample: {df['order_date'].iloc[0]}")

# 1b. Convert 'returned' from Yes/No string → boolean True/False
df['returned'] = df['returned'].map({'Yes': True, 'No': False})
print(f"'returned' converted to boolean. Unique values: {df['returned'].unique()}")


# STEP 2 — Handle Missing Values (none found, but keeping
#           this block as best practice for robust pipelines)

print("\n--- STEP 2: Handling Missing Values ---")

missing_count = df.isnull().sum().sum()
print(f"   Total missing values detected: {missing_count}")

if missing_count == 0:
    print("No missing values to handle.")
else:
    # Fill numeric columns with their median (robust to outliers)
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"   Filled '{col}' nulls with median: {median_val}")

    # Fill categorical columns with mode (most frequent value)
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"   Filled '{col}' nulls with mode: {mode_val}")


# STEP 3 — Remove Duplicate Rows

print("\n--- STEP 3: Removing Duplicate Rows ---")

before = len(df)
df.drop_duplicates(inplace=True)           # Drop fully duplicate rows
df.drop_duplicates(subset='order_id', keep='first', inplace=True)  # Drop duplicate order IDs
after = len(df)

print(f"Removed {before - after} duplicate row(s). Remaining rows: {after}")

# STEP 4 — Standardize Text Columns

print("\nSTEP 4: Standardizing Text Columns")
text_cols = ['category', 'payment_method', 'region', 'customer_gender']

for col in text_cols:
    df[col] = df[col].str.strip().str.title()  # e.g., "  north " → "North"

print(f" Standardized columns: {text_cols}")
print(f"   'region' values: {df['region'].unique()}")
print(f"   'category' values: {df['category'].unique()}")


# STEP 5 — Validate & Fix Numeric Ranges

print("\n--- STEP 5: Validating Numeric Ranges ---")

# Discount must be between 0 and 1
invalid_discount = df[(df['discount'] < 0) | (df['discount'] > 1)]
print(f"   Invalid discount values: {len(invalid_discount)}")
df['discount'] = df['discount'].clip(lower=0.0, upper=1.0)  # Clamp to valid range

# Customer age must be realistic (e.g., 18–100)
invalid_age = df[(df['customer_age'] < 18) | (df['customer_age'] > 100)]
print(f"   Invalid customer_age values (outside 18-100): {len(invalid_age)}")
df = df[(df['customer_age'] >= 18) & (df['customer_age'] <= 100)]

# Price and total_amount must be positive
df = df[df['price'] > 0]
df = df[df['total_amount'] > 0]

print(f"Numeric validation complete. Rows after cleaning: {len(df)}")

# STEP 6 — Feature Engineering (Create New Useful Columns)
print("\n--- STEP 6: Feature Engineering ---")

# 6a. Extract date parts from 'order_date'
df['order_year']    = df['order_date'].dt.year
df['order_month']   = df['order_date'].dt.month
df['order_month_name'] = df['order_date'].dt.strftime('%B')  
df['order_day_of_week'] = df['order_date'].dt.day_name()      
df['order_quarter'] = df['order_date'].dt.quarter              
print("Extracted: order_year, order_month, order_month_name, order_day_of_week, order_quarter")

# 6b. Age Group — bin customer_age into demographic segments
age_bins   = [17, 25, 35, 45, 60, 100]
age_labels = ['18-25', '26-35', '36-45', '46-60', '60+']
df['age_group'] = pd.cut(df['customer_age'], bins=age_bins, labels=age_labels)
print(f"Created 'age_group'. Distribution:\n{df['age_group'].value_counts().sort_index()}")

# 6c. Revenue per Unit — how much revenue each unit generated
df['revenue_per_unit'] = (df['total_amount'] / df['quantity']).round(2)
print("Created 'revenue_per_unit'")

# 6d. Net Profit — actual profit after subtracting shipping cost
#     profit_margin is in %, so: net_profit = total_amount × (profit_margin/100) - shipping_cost
df['net_profit'] = ((df['total_amount'] * df['profit_margin'] / 100) - df['shipping_cost']).round(2)
print("Created 'net_profit'")

# 6e. Is Discounted — boolean flag for whether a discount was applied
df['is_discounted'] = df['discount'] > 0
print("Created 'is_discounted' (True if discount > 0)")

# 6f. Delivery Speed Category
#     Fast: ≤3 days | Standard: 4-7 days | Slow: >7 days
delivery_bins   = [0, 3, 7, 100]
delivery_labels = ['Fast', 'Standard', 'Slow']
df['delivery_speed'] = pd.cut(df['delivery_time_days'], bins=delivery_bins, labels=delivery_labels)
print("Created 'delivery_speed' (Fast / Standard / Slow)")

# STEP 7 — Final Validation Check

print("STEP 7: Final Validation")
print(f"   Remaining missing values : {df.isnull().sum().sum()}")
print(f"   Remaining duplicate rows : {df.duplicated().sum()}")
print(f"   Final shape              : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Columns added            : {df.shape[1] - original_shape[1]} new columns")

# STEP 8 — Export the Cleaned Dataset
print("\nSTEP 8: Exporting Cleaned Dataset ")

# Save as CSV (universal format)
df.to_csv("cleaned_ecommerce_sales.csv", index=False)
print("Cleaned dataset saved as 'cleaned_ecommerce_sales.csv'")

# Save as Excel (for easy viewing in spreadsheet tools)
df.to_excel("cleaned_ecommerce_sales.xlsx", index=False)
print("Cleaned dataset saved as 'cleaned_ecommerce_sales.xlsx'")


print("\n" + "=" * 60)
print(" CLEANING PIPELINE COMPLETE — SUMMARY")
print("=" * 60)
print(f"  Original shape  : {original_shape[0]} rows × {original_shape[1]} cols")
print(f"  Cleaned shape   : {df.shape[0]} rows × {df.shape[1]} cols")
print(f"  New features    : order_year, order_month, order_month_name,")
print(f"                    order_day_of_week, order_quarter, age_group,")
print(f"                    revenue_per_unit, net_profit, is_discounted,")
print(f"                    delivery_speed")
print(f"  Output files    : cleaned_ecommerce_sales.csv")
print(f"                    cleaned_ecommerce_sales.xlsx")
print("=" * 60)
print("\nNew columns preview:")
print(df[['order_id', 'order_year', 'order_month_name', 'age_group',
          'net_profit', 'is_discounted', 'delivery_speed']].head(5).to_string(index=False))
