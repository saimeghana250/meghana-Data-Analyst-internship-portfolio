# data-immersion-
A comprehensive data science project focused on deep-dive data exploration (Data Immersion) and intensive data cleaning, restructuring, and preprocessing (Data Wrangling) to transform raw, messy datasets into analysis-ready assets.

Step 1 — Data Access & Familiarization (data_dictionary.py)

Loaded the raw dataset with Pandas
Created a full Data Dictionary with: column name, data type, description, and business relevance
Saved as CSV and JSON

Step 2 — Data Quality Assessment (data_quality_assessment.py)

Checked for missing values → None found
Checked for duplicate rows → None found
Identified data type issues → order_date (string), returned (Yes/No string)
Inspected categorical value consistency
Detected outliers using the IQR method
Generated box plot visuals for all numeric columns

Step 3 — Data Cleaning & Transformation (data_cleaning.py)

Fixed data types (order_date → datetime, returned → boolean)
Standardized text casing in categorical columns
Validated numeric ranges (discount, age, price)
Removed duplicate rows

Tech Stack

1)Python 3.x
2)Pandas — data manipulation
3)NumPy — numerical operations
4)Matplotlib — visualizations
5)OpenPyXL — Excel export
