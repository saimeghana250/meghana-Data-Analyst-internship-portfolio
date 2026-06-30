# interactive-dashboard
An interactive Data Analytics and Business Intelligence pipeline built with Python, Pandas, and Seaborn to perform data ingestion, data quality cleaning, and exploratory data analysis (EDA) on a large e-commerce sales dataset

Project Architecture & Step-Wise Execution

Step 1: Data Ingestion & Schema Immersion
Systemic Loading: Programmatically ingests the primary relational database file (ecommerce_sales_34500.csv) containing 34,500 individual transactional observations.
Structural Profiling: Maps data attributes, records column metadata schemas, verifies data type arrays, and evaluates the matrix dimensions before executing transformation sequences.

Step 2: Data Wrangling & Quality Auditing
Null Identification Scan: Systematically monitors all structural feature arrays to identify missing, blank, or unassigned data entries.
Deduplication Audit: Executes exact row verification sweeps across the data frame indices to isolate and drop overlapping records.
Pipeline Standardization: Sanitizes dataset formatting to guarantee baseline numerical integrity and structural consistency.

Step 3: Exploratory Data Analysis (EDA) & Business KPIs
Financial Topline Tracking: Automatically computes critical operational targets, including Cumulative Network Sales Revenue and Total Net Realized Profits.
Granular Data Aggregations: Groups data across key categories to extract performance variables:
Product Category Matrix: Measures the exact revenue generation of item classifications.
Geographical Density Maps: Pinpoints sales volume concentration boundaries across operational regions.
Logistical Overheads: Examines average shipping cost burdens applied across retail channels.

Step 4: Presentation Layer Dashboard Engineering
Dynamic BI Display: Employs matplotlib and seaborn plotting mechanics to render a clean, cohesive data presentation interface.
Automated Asset Generation: Automatically builds and saves a high-definition 4-panel visual dashboard sheet (apexplanet_executive_dashboard.png) breaking down sales trends, regional distribution, profit margins, and payment instrument channel splits.

Technological Stack

Language Runtime: Python 3.x

Core Analytics Framework: Pandas

Data Visualization Canvas: Matplotlib & Seaborn
