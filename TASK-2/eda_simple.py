

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from matplotlib.backends.backend_pdf import PdfPages


# STEP 0: LOAD AND CLEAN THE DATA

# pd.read_excel() imports the Excel file into a DataFrame (a table).
df = pd.read_excel("ApexPlanet_DataAnalytics_Dataset.xlsx", sheet_name="Sales_Dataset")

print("Data loaded:", df.shape, "rows x columns")

# Fill missing Age with the median (a safe, simple default)
df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill missing City with a clear label instead of dropping the row
df["City"] = df["City"].fillna("Unknown")

# Make sure Order_Date is a real date (not text) so we can group by month
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)  # e.g. "2025-01"

print("Missing values after cleaning:\n", df.isnull().sum().to_string())

numeric_cols = ["Age", "Quantity", "Unit_Price", "Total_Sales"]
categorical_cols = ["Gender", "City", "Product", "Category"]

# STEP 1: DESCRIPTIVE STATISTICS & UNIVARIATE ANALYSIS

desc_stats = df[numeric_cols].describe().round(2)
print("\nDescriptive statistics:\n", desc_stats)

# value_counts() for each categorical column (saved for printing/Excel later)
cat_counts = {col: df[col].value_counts() for col in categorical_cols}

# STEP 2: SQL FOR BUSINESS QUESTIONS

conn = sqlite3.connect(":memory:")

orders = df[["Order_ID", "Order_Date", "Customer_ID", "Product",
             "Quantity", "Unit_Price", "Total_Sales"]].copy()
orders.insert(0, "Order_PK", range(1, len(orders) + 1))
orders.to_sql("orders", conn, index=False, if_exists="replace")

# Dimension table: one row per customer (keep first record per ID)
customers = df[["Customer_ID", "Customer_Name", "Age", "Gender", "City"]] \
    .drop_duplicates(subset="Customer_ID", keep="first")
customers.to_sql("customers", conn, index=False, if_exists="replace")

# Dimension table: one row per product (Product -> Category mapping)
products = df[["Product", "Category"]].drop_duplicates(subset="Product")
products.to_sql("products", conn, index=False, if_exists="replace")

# Dictionary of {question_name: SQL query}. Each demonstrates filtering,
# aggregation, and/or a multi-table JOIN.
queries = {
    "Top5_Products_Revenue": """
        SELECT Product, SUM(Total_Sales) AS Total_Revenue, COUNT(*) AS Orders
        FROM orders
        GROUP BY Product
        ORDER BY Total_Revenue DESC
        LIMIT 5;
    """,
    "Monthly_Revenue_Trend": """
        SELECT strftime('%Y-%m', Order_Date) AS Month, SUM(Total_Sales) AS Revenue
        FROM orders
        GROUP BY Month
        ORDER BY Month;
    """,
    "Revenue_By_City": """
        SELECT c.City, SUM(o.Total_Sales) AS Revenue, COUNT(*) AS Orders
        FROM orders AS o
        JOIN customers AS c ON o.Customer_ID = c.Customer_ID
        WHERE c.City <> 'Unknown'
        GROUP BY c.City
        ORDER BY Revenue DESC;
    """,
    "AOV_By_Category": """
        SELECT p.Category, ROUND(AVG(o.Total_Sales), 2) AS Avg_Order_Value,
               SUM(o.Total_Sales) AS Revenue
        FROM orders AS o
        JOIN products AS p ON o.Product = p.Product
        GROUP BY p.Category
        ORDER BY Revenue DESC;
    """,
    "Top10_Customers": """
        SELECT c.Customer_ID, c.Customer_Name, c.City,
               COUNT(*) AS Orders, SUM(o.Total_Sales) AS Spend
        FROM orders AS o
        JOIN customers AS c ON o.Customer_ID = c.Customer_ID
        GROUP BY c.Customer_ID
        ORDER BY Spend DESC
        LIMIT 10;
    """,
    "Revenue_By_Gender_Age": """
        SELECT c.Gender,
               CASE WHEN c.Age < 25 THEN '18-24'
                    WHEN c.Age < 35 THEN '25-34'
                    WHEN c.Age < 45 THEN '35-44'
                    WHEN c.Age < 55 THEN '45-54'
                    ELSE '55-65' END AS Age_Group,
               SUM(o.Total_Sales) AS Revenue
        FROM orders AS o
        JOIN customers AS c ON o.Customer_ID = c.Customer_ID
        GROUP BY c.Gender, Age_Group
        ORDER BY c.Gender, Age_Group;
    """,
    "Bulk_Orders_By_Category": """
        SELECT p.Category, ROUND(AVG(o.Unit_Price), 2) AS Avg_Unit_Price,
               SUM(o.Quantity) AS Units_Sold
        FROM orders AS o
        JOIN products AS p ON o.Product = p.Product
        WHERE o.Quantity >= 5
        GROUP BY p.Category
        ORDER BY Avg_Unit_Price DESC;
    """,
}

# Run every query and keep the results in a dictionary of DataFrames
query_results = {}
for name, sql in queries.items():
    result = pd.read_sql_query(sql, conn)
    query_results[name] = result
    print(f"\n--- {name} ---")
    print(result.to_string(index=False))

conn.close()


# STEP 3: MULTIVARIATE ANALYSIS & CORRELATION

correlation_matrix = df[numeric_cols].corr()
print("\nCorrelation matrix:\n", correlation_matrix.round(2))


# STEP 4: KPI DASHBOARD SUMMARY (the numbers behind the mock-up)

kpi_summary = pd.DataFrame({
    "KPI": ["Total Revenue", "Total Orders", "Avg Order Value",
            "Total Units Sold", "Unique Customers", "Avg Customer Age"],
    "Value": [
        df["Total_Sales"].sum(),
        len(df),
        df["Total_Sales"].mean(),
        df["Quantity"].sum(),
        df["Customer_ID"].nunique(),
        df["Age"].mean(),
    ],
})
print("\nKPI summary:\n", kpi_summary.to_string(index=False))


# OUTPUT FILE 1: EDA_Results.xlsx

# Every table above gets its own sheet in one Excel workbook.
with pd.ExcelWriter("EDA_Results.xlsx", engine="openpyxl") as writer:
    desc_stats.to_excel(writer, sheet_name="Descriptive_Stats")
    kpi_summary.to_excel(writer, sheet_name="KPI_Dashboard", index=False)
    correlation_matrix.to_excel(writer, sheet_name="Correlation_Matrix")
    for col, counts in cat_counts.items():
        counts.to_frame("Count").to_excel(writer, sheet_name=f"Counts_{col}")
    for name, result in query_results.items():
        result.to_excel(writer, sheet_name=name[:31], index=False)  # Excel sheet names max 31 chars

print("\nSaved: EDA_Results.xlsx")

# OUTPUT FILE 2: EDA_Charts.pdf

sns.set_style("whitegrid")

with PdfPages("EDA_Charts.pdf") as pdf:

    # --- Univariate: histograms for each numeric column ---
    for col in numeric_cols:
        plt.figure(figsize=(7, 4.5))
        sns.histplot(df[col], bins=20, kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    # --- Univariate: bar charts for each categorical column ---
    for col in categorical_cols:
        plt.figure(figsize=(7, 4.5))
        order = df[col].value_counts().index
        sns.countplot(data=df, x=col, order=order, hue=col, legend=False)
        plt.title(f"Orders by {col}")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    # --- Multivariate: Age vs Total_Sales scatter plot ---
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x="Age", y="Total_Sales", hue="Category", alpha=0.6)
    plt.title("Age vs Total Sales (by Category)")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --- Multivariate: Unit_Price vs Quantity scatter plot ---
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x="Unit_Price", y="Quantity", hue="Category", alpha=0.6)
    plt.title("Unit Price vs Quantity (by Category)")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --- Correlation heatmap ---
    plt.figure(figsize=(6, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --- Pair plot of all numeric fields, split by Gender ---
    pair_fig = sns.pairplot(df[numeric_cols + ["Gender"]], hue="Gender", diag_kind="kde")
    pair_fig.fig.suptitle("Pair Plot of Numeric Fields", y=1.02)
    pdf.savefig(pair_fig.fig)
    plt.close("all")

    # --- Box plot: Total_Sales spread by Category ---
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=df, x="Category", y="Total_Sales", hue="Category", legend=False)
    plt.title("Total Sales Distribution by Category")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

print("Saved: EDA_Charts.pdf")

print("\nDone! 2 output files created:")
print("  1. EDA_Results.xlsx  -> stats, SQL results, KPI dashboard")
print("  2. EDA_Charts.pdf    -> all charts, one per page")
